# Estate Corruption – Europa Universalis V

**v0.1.0-rc1 (Quellcode)** · Ziel: EU5 1.4.9 · Stand: technisch vorbereitet, **noch nicht im Spiel verifiziert**.

Die Mod ersetzt die harte Estate-Max-Tax-Grenze durch eine akzeptierte Steuergrenze. Jeder Estate besitzt einen separaten, gespeicherten Korruptionswert 0–100. Überbesteuerung erhöht die Korruption monatlich; Loyalität funktioniert weiterhin nach Vanilla. Jedem Stand ist ein linear skalierender Country-Malus zugeordnet.

## Enthalten

- Monatlicher Country-Pulse zur Berechnung von acht Estate-Korruptionswerten, einschließlich Crown.
- Neue akzeptierte Steuer-Modifier je steuerpflichtigem Estate und ein globaler Modifier.
- Acht dynamische Korruptionsfolgen mit Skalierung von 0 bis 100.
- Deutsche und englische Übersetzungen, automatisierter Audit und Buildgenerator.
- Unit-Tests und GitHub Actions für die Entwicklung.

## Benötigter lokaler Build

Eine vollständige EU5-1.4.9-Installation wird benötigt, damit Max-Tax-Zuweisungen aus aktuellen Vanilla-Dateien migriert und die echten Steuergrenzen anschließend auf 100 % gestellt werden können.

1. Unit-Tests: python -m unittest discover -s tests -v
2. Release Candidate: python tools/build_release.py --game /pfad/zur/EU5/game --game-version 1.4.9 --out dist/EstateCorruption
3. Die Reports in dist/ prüfen und den erzeugten Mod-Ordner in EU5 laden.

Nur der generierte Ordner dist/EstateCorruption ist für einen lokalen Mod-/Workshop-Test gedacht. Keine vollständigen Gamefiles werden im GitHub-Repository verteilt.

**Wichtig:** Die eingegebene Versionsnummer wird nicht gegen den laufenden EU5-Prozess geprüft. Der Release Candidate muss vor einem Steam-Workshop-Upload mit EU5 1.4.9 getestet werden.

Weitere Details: docs/PLAN.md, docs/IMPLEMENTATION.md, docs/TESTPLAN.md und docs/WORKSHOP.md.
