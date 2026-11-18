# Technischer Status und geplante Implementierung

## Verifikation und Grenzen

Die derzeit **verifizierte** öffentliche Spielversion ist EU5 **1.4.9** (18.11.2026). Das verfügbare GitHub-Textarchiv `HLJSXK/eu5-modding-base` hat Gamefiles aus **1.4.3 beta**, letzter Gamefile-Sync: Commit `9e941ced` vom 23.10.2026. Die öffentliche EU5DB ist eine extrahierte Sekundärdatenbank, kein vollständiger 1.4.9-Dump. Die erste Entwicklungsfassung entstand lokal und wird in `Kevni92/eu5-corruption` versioniert.

### Bestätigte ältere Spiel-Referenzen (1.4.3 beta, **nicht** 1.4.9-Syntaxbeleg)

- `game/in_game/common/estates/00_default.txt`: u. a. `nobles_estate_max_tax`, `global_estate_max_tax`, `levy_combat_efficiency_modifier`.
- `game/in_game/common/laws/03_estate_laws.txt`: Policy `curtail_nobles_policy` mit `nobles_estate_max_tax = 0.1`.
- `game/in_game/common/estate_privileges/nobles_estate.txt` und `peasants_estate.txt`: Max-Tax-Werte.
- `game/in_game/common/cabinet_actions/taluqdar_tax_collection.txt`: `peasants_estate_max_tax`.
- `game/in_game/common/auto_modifiers/country.txt`: `country_base_values`.
- `game/main_menu/common/modifier_type_definitions/00_modifier_types.txt`: Typdefinitionen (`percent`, `color`, `game_data/category`).
- `game/main_menu/common/static_modifiers/`: statische Ländermodifikatoren mit Country-Scope.
- `monthly_country_pulse` laut altem `on_actions.log` mit Country-Scope; aktuelle 1.4.9-Semantik offen.

## Paket-Dateien

- `main_menu/common/modifier_type_definitions/ec_modifier_types.txt`: neue **Definitionen** für akzeptierte Besteuerung, monatliche Korruptionsrate und Anzeige der Korruptionswerte.
- `main_menu/common/static_modifiers/ec_corruption_impact.txt`: vorbereitete Country-Malusse auf Basis von 100 Korruption. **Die Datei alleine wendet sie noch nicht an.**
- `in_game/common/auto_modifiers/ec_tax_ceiling_experimental.txt`: aus Sicherheitsgründen auskommentierter Entwurf für die 100%-Grenze; keine aktive Steueränderung.
- `tools/build_overrides.py`: findet alle direkten Max-Tax-Zuweisungen in der aktuellen Vanilla und erstellt im Build-Verzeichnis Overlay-Dateien. **Muss von einem Menschen auf Vollständigkeit und Semantik geprüft werden.**
- `docs/PLAN.md`: Berechnungs- und Balancingziel.

## Kritische noch ausstehende technische Arbeiten

1. Vollständigen 1.4.9-`game/`-Ordner lokal scannen, `script_docs` und `dump_data_types` dazu erzeugen.
2. Max-Tax-Quellen nach Typ klassifizieren: Vanilla-Estate high/low-power, Base/Auto, Policies, Privileges, Advances, scripted modifiers, GUI, Trigger, DLC, DLC-Overrides, sonstige Datentypen. `global_estate_max_tax` nicht übersehen.
3. Den tatsächlichen Max-Tax-Algorithmus der Engine und GUI prüfen (100 % Slider gegen 100 % nominelle Estate-Besteuerung abgrenzen).
4. Alle Werte auf neue Country-Modifier umhängen. **Globaler Modifier** bleibt global und wirkt auf die Akzeptanz aller steuerpflichtigen Estates. Vorherige Basisteile und Skalierungen erhalten.
5. Per Country/Stand persistente `ec_<estate>_corruption`-Variablen anlegen; Monthly-Update an den aktuell nachgewiesenen Country-Monthly-Hook anbinden; Initialisierung und Savegame-Restore testen.
6. Prüfen, wie der Engine-Scriptwert eines neu definierten Country-Modifiers gelesen werden kann und ob der Estate-Tax-Rate-Getter die maßgebliche 0–100-%-Steuer widerspiegelt.
7. Effects dynamisch mit `add_country_modifier(... size = corruption / 100)` oder verifizierter `auto_modifier`-Skalierung aktualisieren. Keine unbewiesene Syntax übernehmen.
8. GUI- und Localization-Hook einbauen; zusätzliche Multiplayer-/KI-/Performance-Tests.

## Override-Konflikte

Der Generator erzeugt **Whole-file-Overlays**. Diese sind besonders konfliktanfällig und dürfen nicht als allgemeine finale Workshop-Lösung gelten. `INJECT`, `REPLACE` und Listenoperationen sind **datenbankabhängig** und müssen mit 1.4.9 geprüft werden. Für eine Workshop-Veröffentlichung bevorzugt minimalinvasive Objektoperationen einsetzen, soweit exakt verifiziert.

## Datenrechte

Kein mit Drittanbieter-Gamefiles gefülltes GitHub-Repository anlegen. Versionstreue Vanilla-Scans und generierte Overrides bleiben zunächst lokal. Bei Steam-Uploads die Lizenz-/Moddingregeln von Paradox und die Rechte an enthaltenen Originaldateien prüfen.
