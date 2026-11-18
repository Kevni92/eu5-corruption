# 1.4.9 Vanilla-Fundstellen-Audit

Die aktuelle öffentliche Version ist 1.4.9. Eine **vollständige** 1.4.9-Quellkopie liegt in diesem Projekt nicht vor. Darum ist dies ein **Arbeitsprotokoll**, kein erschöpfender Fundstellenindex.

## Bereits nachgewiesene Key-Familien

- `nobles_estate_max_tax`
- `clergy_estate_max_tax`
- `burghers_estate_max_tax`
- `peasants_estate_max_tax`
- `tribes_estate_max_tax`
- `cossacks_estate_max_tax`
- `dhimmi_estate_max_tax`
- `global_estate_max_tax`

Die sieben genannten Estates sind steuerpflichtig. Die Krone ist Sonderfall, `tax_per_pop = 0` im älteren Stand. Bei 1.4.9 alle Estate-Definitionen und eventuelle DLC-Sonderstände erneut scannen.

## Konkrete Vanilla-Beispiele (nur 1.4.3 beta)

| Quellpfad im Gamefile-Spiegel | Gefundener Bezug | Anmerkung |
|---|---|---|
| `in_game/common/estates/00_default.txt` | `nobles_estate_max_tax = -1.0` (high power), `= 0.5` (low power); `global_estate_max_tax` | Direkte Estate-Power-Skalierung; **Vorzeichen und Engine-Semantik beibehalten** |
| `in_game/common/laws/03_estate_laws.txt` | `curtail_nobles_policy`: `nobles_estate_max_tax = 0.1` | Policy-Wirkung |
| `in_game/common/estate_privileges/nobles_estate.txt` | mehrere negative `nobles_estate_max_tax`-Werte | Privilegien |
| `in_game/common/estate_privileges/peasants_estate.txt` | `peasants_estate_max_tax = -0.25` und `-0.2` | Privilegien |
| `in_game/common/cabinet_actions/taluqdar_tax_collection.txt` | `peasants_estate_max_tax = 0.15` | Kabinettsaktion |
| `in_game/common/advances/country_HUN.txt` | `peasants_estate_max_tax = 0.1` | Advance |

Die Zeilen sind im GitHub-Snapshot `9e941ced` des externen Repos `HLJSXK/eu5-modding-base` nachzuprüfen, und bei 1.4.9 neu zu lokalisieren. Nicht als 1.4.9 bezeichnen.

## Lokale vollständigere Erhebung

`python tools/build_overrides.py --game <EU5-Installation>/game --out build`

Der Scanner nimmt alle `.txt`-Dateien unter `game/` auf, einschließlich DLC-Dateien. Die JSON-Liste unterscheidet Kandidaten, kommentierte Erwähnungen, ausgeschlossene Kategorien, unbekannte Keys und manuell zu prüfende Kontexte. Automatische Änderungen sind **bloße Textkandidaten**, keine sicheren Parser-/Engine-Overwrites.

Ergebnis: `build/max_tax_audit.json` + `build/overrides/`. Unter `build/overrides/` liegt für jeden candidate die *vollständige* transformierte Vanilla-Quelldatei. Diese bleiben **außerhalb** des Mod-Stamms, bis ein 1.4.9-Review ihre Kompatibilität und Syntax bestätigt.

## Pflicht bei Abschluss

Versionsnummer, Steam-Build, Quellen-Hash, Dateizahl, gefundenen und migrierten Key-Counts, Resttreffer, Konflikte, Parser-Logs sowie Steuer-/KI-/GUI-Verhalten dokumentieren. Niemals "0 Fehler" als Erfolg ausgeben, wenn der Scan keine Quelldateien gefunden hat.
