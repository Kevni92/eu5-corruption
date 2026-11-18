# Estate Corruption (EU5)

**Version:** 0.1.0-dev · **Ziel:** Europa Universalis V 1.4.9 (18.11.2026) · **Status:** Entwicklungsprototyp, **nicht Workshop-freigegeben**.

Eine Mod zur Umdeutung der bisherigen harten Estate-Steuerobergrenzen in akzeptierte Steuersätze und Einführung eines eigenständigen Korruptionswerts für jeden Stand.

## Was bereits enthalten ist

- EU5-Mod-Metadaten (`.metadata/metadata.json`) und deutsche/englische Localization.
- Definitionen für neue Acceptable-Tax-, Monthly-Corruption- und Corruption-Anzeigemodifier.
- Acht vorbereitete statische Malus-Modifier (100%-Basiswerte); **noch nicht aktiv angewendet**.
- Abschaltbarer Prototyp eines 100%-Steuerlimits unter `in_game/common/auto_modifiers/`.
- Versionsgebundener Scanner/Override-Generator in `tools/`.
- Fachkonzept, Testspezifikation, Fundstellen und Workshop-Hinweise in `docs/`.

## Nicht implementiert

Die Engine-Anbindung zur monatlichen Speicherung/Berechnung der Korruption und die mit ihrem Wert stufenlos skalierten Effekte, die garantierte 100%-Besteuerbarkeit und sämtliche 1.4.9-Vanilla-Overrides. **Es wäre falsch, diesen Stand als funktionsfähige v0.1 oder veröffentlichungsreife Mod auszugeben.**

## Lokale Vanilla-Dateien prüfen

```bash
python tools/build_overrides.py --game "<Pfad zur EU5-Installation>/game" --out "build/overrides"
```

Dies erstellt unter `build/overrides/` die umgeschriebenen Kopien aller Originaldateien mit Max-Tax-Verwendungen und `max_tax_audit.json`. Keine Originaldateien werden verändert. **Noch nicht automatisch ins Mod-Verzeichnis kopieren:** Die generierten Dateien müssen zunächst versionstreu, auf Override-Konflikte und im laufenden Spiel geprüft werden.

## EU5-Launcher / Steam Workshop

Der Launcher erwartet `.metadata/metadata.json` im Mod-Stammverzeichnis. Der Ordner `docs/` und `tools/` gehört nicht in den Workshop-Upload. Siehe [docs/WORKSHOP.md](docs/WORKSHOP.md).

Pläne und technische Entscheidungen: [docs/PLAN.md](docs/PLAN.md), [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md).
