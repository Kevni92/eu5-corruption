#!/usr/bin/env python3
"""Build a locally installable Estate Corruption mod from a licensed EU5 installation.

Requires an actual full game/ tree for the target patch. Never edits game files
or commits their contents to Git. Exits on uncertain modifier references.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from build_overrides import build as audit_and_migrate

TARGET_VERSION = "1.4.9"
CONTENT_DIRS = (".metadata", "in_game", "main_menu")
IGNORE = {"__pycache__", "build", ".git"}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def release(project: Path, game: Path, destination: Path, declared_version: str):
    project, game, destination = (x.expanduser().resolve() for x in (project, game, destination))
    if declared_version != TARGET_VERSION:
        raise ValueError(f"Build is gated to EU5 {TARGET_VERSION}, got {declared_version!r}.")
    if destination == project or destination == game or project in destination.parents and destination.name == "game":
        raise ValueError("Output must not overwrite the source or game directory.")
    if not (project / ".metadata" / "metadata.json").is_file():
        raise ValueError("Missing mod metadata in source repository.")
    if not (project / "in_game" / "common" / "scripted_effects" / "ec_corruption_monthly.txt").is_file():
        raise ValueError("Monthly corruption implementation is missing.")
    # Build to a temporary dir first. Never publish a partial or failed build.
    with tempfile.TemporaryDirectory(prefix="ec_assembly_") as td:
        work = Path(td)
        audit = audit_and_migrate(game, work / "audit", write_overrides=True)
        statuses = audit["status_counts"]
        if statuses.get("unknown_modifier", 0) or statuses.get("manual_review", 0):
            raise RuntimeError("Vanilla audit has unknown modifier keys or ambiguous references; inspect max_tax_audit.json before release.")
        if audit["candidate_assignments"] == 0:
            raise RuntimeError("No max-tax assignments migrated. Wrong game tree?")
        hits = [x for x in audit["findings"] if x["status"] == "candidate"]
        expected = Path("in_game/common/auto_modifiers/country.txt")
        if not any(x["file"] == expected.as_posix() and
                   x["modifier"] == "global_estate_max_tax" for x in hits):
            raise RuntimeError("Vanilla base global_estate_max_tax not identified: 100% cap cannot be guaranteed.")
        payload = work / "EstateCorruption"
        for dirname in CONTENT_DIRS:
            source = project / dirname
            if not source.is_dir():
                raise RuntimeError(f"Missing required source tree: {source}")
            shutil.copytree(source, payload / dirname,
                            ignore=shutil.ignore_patterns(*IGNORE, "*.pyc"))
        for file in (work / "audit" / "overrides").rglob("*.txt"):
            rel = file.relative_to(work / "audit" / "overrides")
            target = payload / rel
            if target.exists():
                raise RuntimeError(f"Collision between bundled mod and generated Vanilla override: {rel}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
        metadata_file = payload / ".metadata" / "metadata.json"
        metadata = json.loads(metadata_file.read_text(encoding="utf-8-sig"))
        metadata["version"] = "0.1.0-rc1"
        metadata["supported_game_version"] = "1.4.*"
        metadata["short_description"] = "Tax tolerance and estate corruption (0.1.0 release candidate)"
        metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        report = {
            "target_version_declared": declared_version,
            "version_verified_by_engine": False,
            "files_scanned": audit["files_scanned"],
            "assignments_migrated": audit["candidate_assignments"],
            "files_overridden": audit["files_with_candidate_changes"],
            "source_country_sha256": sha256(game / expected),
            "notes": [
                "Build uses user's local vanilla game files, not third-party snapshots.",
                "Build has not been executed in the EU5 engine. Workshop publishing requires an in-game acceptance test.",
                "Whole-file overrides are compatibility-sensitive."
            ],
            "files": sorted(str(x.relative_to(payload)).replace("\\", "/")
                            for x in payload.rglob("*") if x.is_file())
        }
        if destination.exists():
            if any(destination.iterdir()):
                raise FileExistsError(f"Refusing to overwrite non-empty output directory {destination}.")
            destination.rmdir()
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(payload), str(destination))
        report_path = destination.parent / (destination.name + "_build_report.json")
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        audit_path = destination.parent / (destination.name + "_max_tax_audit.json")
        shutil.copy2(work / "audit" / "max_tax_audit.json", audit_path)
        return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", type=Path, required=True, help="Full installed game/ directory")
    parser.add_argument("--game-version", required=True, help="Declared version from the running game")
    parser.add_argument("--out", type=Path, default=Path("dist/EstateCorruption"))
    args = parser.parse_args()
    result = release(Path(__file__).resolve().parents[1], args.game, args.out, args.game_version)
    print(f"RC build created: {args.out}")
    print(f"{result['assignments_migrated']} max-tax entries migrated in {result['files_overridden']} files.")
    print("NOT engine-verified; launch EU5 and run docs/TESTPLAN.md before Workshop publishing.")

if __name__ == "__main__":
    main()
