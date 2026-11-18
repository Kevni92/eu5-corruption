#!/usr/bin/env python3
"""Audit exact local EU5 max-tax assignments and generate REVIEW-ONLY overlays.

This is a build-time scanner, NOT gameplay scripting. Never publishes files.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

TAXABLE = ('nobles', 'clergy', 'burghers', 'peasants', 'tribes', 'cossacks', 'dhimmi')
KEY_MAP = {f'{estate}_estate_max_tax': f'ec_{estate}_acceptable_max_tax' for estate in TAXABLE}
KEY_MAP['global_estate_max_tax'] = 'ec_global_acceptable_max_tax'
# Detect ALL tax modifier names, including future/changed estates, before rewriting.
FIND = re.compile(r'\b(?:[a-z][a-z_]*_estate_max_tax|global_estate_max_tax)\b')
# Only isolated, line-leading key assignments are automatically migratable.
ASSIGN = re.compile(r'^(?P<leading>[ \t]*)(?P<key>[a-z][a-z_]*_estate_max_tax|global_estate_max_tax)(?P<eq>[ \t]*=[ \t]*)', re.M)

def is_skipped(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & {'localization', 'gui', 'modifier_type_definitions', 'gfx', 'map_data'})

def scan_one(file: Path, relative: Path):
    raw = file.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    findings = []
    offsets = []
    position = 0
    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        for m in FIND.finditer(line):
            key = m.group(0)
            if line.lstrip().startswith('#'):
                status = 'comment'
            elif is_skipped(relative):
                status = 'excluded_category'
            elif key not in KEY_MAP:
                status = 'unknown_modifier'
            elif not (a := ASSIGN.match(line)) or a.group('key') != key or a.start('key') != m.start():
                status = 'manual_review'
            else:
                # The assignment may be a trigger instead of a modifier. Always review the output.
                status = 'candidate'
                offsets.append((position + a.start('key'), position + a.end('key'), KEY_MAP[key]))
            findings.append({'file': str(relative).replace('\\', '/'), 'line': line_number,
                             'modifier': key, 'status': status,
                             'replacement': KEY_MAP.get(key), 'excerpt': line.strip()[:280]})
        position += len(line)
    generated = text
    for start, end, replacement in reversed(offsets):
        generated = generated[:start] + replacement + generated[end:]
    return findings, generated.encode('utf-8-sig' if bom else 'utf-8'), len(offsets)

def build(game: Path, out: Path, write_overrides: bool = True):
    game = game.expanduser().resolve()
    out = out.expanduser().resolve()
    if not game.is_dir() or not (game / 'in_game').is_dir() or not (game / 'main_menu').is_dir():
        raise ValueError('Expected the installed EU5 game/ directory with both in_game/ and main_menu/.')
    # prevent scanning and writing inside the same tree
    if out == game or game in out.parents:
        raise ValueError('Output must be outside the original game directory.')
    sources = sorted(p for p in game.rglob('*.txt') if p.is_file() and 'mod' not in p.relative_to(game).parts)
    if len(sources) < 50:
        raise ValueError(f'Only {len(sources)} text files were found; this is not a plausible full EU5 game snapshot.')
    findings=[]; changes=[]
    for file in sources:
        rel=file.relative_to(game)
        hits, updated, count = scan_one(file, rel)
        findings.extend(hits)
        if count:
            changes.append((rel, updated, count))
    if not findings:
        raise RuntimeError('ZERO max-tax references found. Wrong game path, version or scan?')
    summary=Counter(a['status'] for a in findings)
    manifest={
        'input_path': str(game), 'files_scanned': len(sources),
        'files_with_candidate_changes': len(changes),
        'candidate_assignments': sum(n for _,_,n in changes),
        'status_counts': dict(summary),
        'warning': 'This is a text-level candidate migration, NOT engine-validated or Workshop-ready.',
        'findings': findings
    }
    out.mkdir(parents=True,exist_ok=True)
    (out / 'max_tax_audit.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    if write_overrides:
        for rel, raw, _ in changes:
            target=out/'overrides'/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():
                raise FileExistsError(f'Refusing to overwrite existing generated file: {target}')
            target.write_bytes(raw)
    return manifest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--game',type=Path,required=True,help='Installed EU5 game/ directory')
    ap.add_argument('--out',type=Path,default=Path('build'),help='Write review-only overrides and audit here')
    ap.add_argument('--audit-only',action='store_true',help='Write JSON report but no overlays')
    ns=ap.parse_args()
    m=build(ns.game,ns.out,not ns.audit_only)
    print(f"Scanned {m['files_scanned']} files, {len(m['findings'])} references, "
          f"{m['candidate_assignments']} candidate edits in {m['files_with_candidate_changes']} files")
    print(f"Review the report in: {ns.out / 'max_tax_audit.json'}")
    blockers=[(k,v) for k,v in m['status_counts'].items() if k in ('unknown_modifier','manual_review','excluded_category') and v]
    if blockers:
        print('Manual verification required:',blockers)
    print('NOT READY for use as Steam Workshop payload without 1.4.9 engine tests.')

if __name__ == '__main__':
    main()
