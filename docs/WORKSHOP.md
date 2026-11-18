# Steam Workshop – Freigabeplan v0.1

Der Entwicklungsstand 0.1.0-rc1 ist **noch nicht Workshop-freigegeben**.

1. EU5 1.4.9 installieren. Die tatsächliche Buildnummer und Checksum dokumentieren.
2. python -m unittest discover -s tests -v ausführen.
3. python tools/build_release.py --game /pfad/zur/EU5/game --game-version 1.4.9 --out dist/EstateCorruption ausführen.
4. Audit- und Buildreport in dist/ vollständig prüfen. Nicht erkannte Estate-Max-Tax-Quellen blockieren den Build.
5. Nur den generierten Ordner dist/EstateCorruption als lokale Mod aktivieren. Quellcode, Docs und Vanilla-Referenzen gehören nicht in den Workshop-Upload.
6. Alle Fälle in docs/TESTPLAN.md auf der echten Spielversion testen und Logfehler beheben.
7. Erst danach Metadaten auf v0.1.0 setzen, ein eigenes Thumbnail anlegen und über EU5/Steam Launcher hochladen.

**Risiken:** Der Build verwendet Whole-file-Overrides für die migrierten Vanilla-Quellen. Das kann Modkonflikte auslösen. Eine lokal angegebene Version ist keine technisch verifizierte Engine-Version. Unit-Tests ersetzen keinen Spieltest.
