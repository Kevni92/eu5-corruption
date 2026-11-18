# Codex-/AI-Anweisungen: Estate Corruption

- EU5/Jomini **nicht** mit EU4/CK3-Syntax verwechseln.
- Zielpatch ist EU5 **1.4.9 (18.11.2026)**. Die online geprüften 1.4.3-beta-Gamefiles sind *nur historische Referenz*.
- Vor jeder Runtime-Änderung: gleiche lokale Vanilla-Version, `script_docs`, `dump_data_types`, Fundstellen, Scopes und tatsächlich laufenden Test nachweisen.
- Jede Mod-Funktion muss ihren Status haben: `DESIGN`, `PROTOTYP`, `VERIFIZIERT_1.4.9`, `GETESTET_1.4.9`.
- Bei Fundstellenmigration nie nur die ersten Suchergebnisse nehmen. `tools/build_overrides.py` auf **vollständigem** lokalem Gamefile-Baum ausführen, DLCs berücksichtigen, Testreport führen.
- Whole-file-Overrides sind konfliktreich; kein blindes `zz_`, keine Annahme, dass `INJECT` rekursiv merged.
- Erst Audit (read-only), danach Implementation, danach positive Kontrolltests, `error.log`, Ingame-Verhaltensprüfung und Savegame-Restart.
- Ursprung von Aussagen in `docs/SOURCES.md`, neue Erkenntnisse und Versionstests in `docs/IMPLEMENTATION.md` dokumentieren.
- Keine urheberrechtlich geschützten Vanilla-Gamefiles in Git synchronisieren.
- Featurekonzept und Tests: `docs/PLAN.md`, `docs/TESTPLAN.md`.
