# Steam-Workshop-Checkliste

Der Stand `0.1.0-dev` ist **nicht** veröffentlichungsbereit.

## Vorbereitung

1. EU5 1.4.9 und Version des Gamefile-Snapshots nachweisen.
2. V0.1-Abnahmekriterien aus `PLAN.md` vollständig erfüllen und im Spiel testen.
3. Nur `.metadata/`, `in_game/`, `main_menu/` und benötigte Assets in den Release-Ordner übernehmen. `docs/`, `tools/`, `build/` und den kompletten Vanilla-Spielbaum nicht in den Workshop hochladen.
4. Ein eigenständiges Vorschaubild `thumbnail.png` anlegen (empfohlen 512×512). Lizenz und Dateigröße prüfen.
5. `.metadata/metadata.json` nach tatsächlicher Testfreigabe auf `0.1.0` setzen und `short_description` überarbeiten.
6. Über den EU5-Launcher als lokale Mod aktivieren und anschließend mit Steam-Workshop-Funktion hochladen.
7. Workshop-Titel/Beschreibung, Changelog, benötigte Spielversion und Inkompatibilitäten angeben.

## QA-Freigabe

- 0 Parserfehler aus Mod-Dateien, Test im Spiel statt nur Log-Suche.
- Tax-Cap 100 % für alle sieben steuerpflichtigen Vanilla-Estates in mehreren Länder-/Regierungs-/DLC-Konstellationen.
- Korrektes Verhalten von Crown Estate ohne eigene Steuer.
- Korruptionswerte unabhängig, begrenzt und savegame-persistent.
- Nichtlineare Gameplay-Effekte nur falls bewusst vorgesehen; v0.1 fordert lineare Skalierung.
- Keine stillen Kompatibilitätsprobleme mit bekannten UI/Tax-Mods.
- Multiplayer-Synchronisierung prüfen, falls gewünscht.
