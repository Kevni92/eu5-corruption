# Implementierungsstand v0.1.0-rc1

**Ziel:** EU5 1.4.9 (18.11.2026). **Quellen:** vollständige Gamefile-/Engine-Referenzen sind nur für 1.4.3 Beta nachgewiesen. Dies ist noch **kein 1.4.9-Laufzeitnachweis**.

## Implementiert

- Acht persistente Country-Korruptionsvariablen von 0–100.
- Monatliche Berechnung über monthly_country_pulse, Estate-Tax-Rate und akzeptierte Steuer-Modifier.
- Berechnungsregel: +10 Korruptionspunkte pro Monat bei 100 Prozentpunkten Überbesteuerung, zusätzlich zum jeweiligen Monthly-Corruption-Modifier; natürliche Erholung −0,1/Monat. Jeder Wert wird nach Änderung auf [0, 100] begrenzt. Balancing noch vorläufig.
- Acht eigene statische Country-Malusse, deren tatsächliche Stärke monatlich auf Korruption/100 gesetzt wird. Jeder dieser Modifier enthält zugleich den sichtbaren Wert ec_<estate>_corruption = 100, wodurch er bei dynamischer Skalierung die tatsächliche Korruption von 0 bis 100 anzeigt.
- Neue akzeptierte Tax- und monatliche Corruption-Modifier, deutsche und englische Localization.
- Build aus lokaler Vanilla: ersetzt aktuelle Max-Tax-Zuweisungen durch akzeptierte Max-Tax-Modifier und fügt anschließend den globalen Max-Tax-Cap 1.0 über INJECT:country_base_values hinzu.
- Vanilla-Auswirkungen auf Estate-Loyalität werden nicht geändert.

## Noch offen

1. Tatsächlich installierten Patch 1.4.9 und identische lokale Gamefiles/Engine-Dumps beschaffen.
2. Build und Script-Verhalten in EU5 testen, insbesondere monatlichen Hook, Skriptwerte, Variable-Persistenz und dynamische Modifier-Skalierung.
3. Vollständigen Audit der betroffenen Vanilla-Dateitypen, der GUI und der DLC-Interaktionen durchführen. Whole-file-Overrides sind nicht universell kompatibel.
4. Prüfen, ob der Slider nach Cap-Anhebung tatsächlich 100 % des Estate-Tax-Maximums darstellt.
5. KI-, Savegame-, Localization-, Multiplayer- und Performance-Tests abschließen.
6. Erst danach Version 0.1.0 für den Steam Workshop freigeben.

## Verifizierte Muster aus dem älteren Snapshot

HLJSXK/eu5-modding-base, Gamefile-Sync 9e941ced (1.4.3 Beta):
- in_game/common/auto_modifiers/country.txt: country_base_values, global_estate_max_tax = 0.35.
- in_game/common/on_action/country_monthly.txt: monthly_country_pulse.
- in_game/common/estates/00_default.txt: Estate-Power-Skalierung für max_tax.
- reference_official_defines/docs/effects.log: add_country_modifier und change_country_modifier_size.
- reference_official_defines/docs/triggers.log: estate_tax_rate und estate_max_tax.
- in_game/common/generic_actions/holy_war_war_actions.txt: clamp_variable.

Diese alten Referenzen sind **kein** Beweis der Syntaxgültigkeit im Patch 1.4.9.
