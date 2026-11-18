# Estate Corruption – Fachkonzept v0.1

Stand: 18.11.2026 · Zielpatch: EU5 1.4.9. **Konzept**, keine Behauptung einer fertigen Implementierung.

## Grundidee

Der Herrscher darf von jedem steuerpflichtigen Estate nominell 0–100 % Steuer fordern. Statt einer harten Estate-Max-Tax-Grenze gibt es **akzeptable maximale Steuer**. Überbesteuerung bewirkt langfristige Korruption. Bereits vorhandene Auswirkungen der Besteuerung auf die Estate-Loyalität bleiben erhalten.

## 1. Neue Bedeutung der bisherigen Max-Tax-Werte

- Vollständige Inventur aller Vanilla-Verwendungen von `<estate>_estate_max_tax` sowie `global_estate_max_tax`.
- Bestehende Werte von Gesetzen, Privilegien, Advances, Auto-Modifikatoren usw. werden mit identischer Vorzeichen-/Skalierungssemantik auf `ec_<estate>_acceptable_max_tax` bzw. `ec_global_acceptable_max_tax` übertragen.
- Besteuerungsobergrenze wird von der akzeptablen Steuer entkoppelt; **technisches Ziel: alle steuerpflichtigen Estates dauerhaft bis 100 %**.
- Auf Prozentwerte und Faktoren achten: Der Steuerregler kann einen Anteil an der Maximalsteuer darstellen; „100 %“ ist nicht ohne Prüfung mit 100 % des gesamten Estate-Einkommens gleichzusetzen.
- Texte sollen klar ausdrücken: positiv = größere Steuerakzeptanz, negativ = geringere Steuerakzeptanz.

## 2. Eigener Korruptionswert je Estate

- Nobility, Clergy, Burghers, Peasants, Tribes, Cossacks, Dhimmi und Crown: jeweils unabhängiger numerischer Korruptionswert zwischen 0 und 100.
- Sonderfall Krone: gehört zum Korruptionsmodell, ist aber nicht regulär steuerpflichtig; ihre Korruption erhält in v0.1 keinen steuerbasierten Zuwachs.
- Werte müssen dauerhaft im Savegame gespeichert und bei jedem Monatswechsel aktualisiert werden.
- `ec_<estate>_monthly_corruption` ist ein **Modifier für die monatliche Veränderung**. Positive Zahlen bedeuten mehr Korruption (schlecht). Einheit: Korruptionspunkte pro Monat, nicht relative Prozente.
- Überbesteuerung soll den monatlichen Zuwachs bewirken. Loyalität sinkt weiterhin unabhängig nach Vanilla-Logik.

## 3. Mathematisches Zielmodell

Pro steuerpflichtigem Stand `e`:

- `a[e] = clamp(akzeptierte Basissteuer + estate-bezogene und globale Acceptable-Tax-Modifikatoren, 0, 1)`
- `t[e] = tatsächlicher Steuerbefehl/Steuersatz im Engine-Sinn, im Bereich [0, 1]`
- `o[e] = max(0, t[e] - a[e])`
- `Δc[e] = k * o[e] + m[e] - r[e]`
- `c[e, nächster Monat] = clamp(c[e] + Δc[e], 0, 100)`

`k` ist das noch zu balancierende Ausmaß der Überbesteuerung, `m[e]` der neue Monthly-Corruption-Modifier, `r[e]` eine mögliche natürliche Erholung. **Noch keine festen Balancewerte beschlossen.** Basiswert der akzeptablen Steuer ist aus 1.4.9-Vanilla zu übernehmen, nicht zu erfinden.

## 4. Stufenlose Folgen

Jeder Estate besitzt einen eigenen Malus. Die volle Stärke entspricht Korruption 100, bei 50 wird die halbe Wirkung angewendet; 0 bedeutet keine Wirkung.

| Estate | Erste Wirkung bei 100 Korruption |
|---|---|
| Nobility (Adel) | −30 % Levy Combat Efficiency |
| Clergy (Klerus) | −25 % Pop Conversion Speed |
| Burghers (Bürger) | −25 % Trade Income |
| Peasants (Bauern) | −25 % Food Production |
| Tribes (Stämme) | −25 % Levy Recovery |
| Cossacks (Kosaken) | −20 % Levy Combat Efficiency |
| Dhimmi | −20 % Pop Conversion Speed |
| Crown (Krone) | −25 % Country Cabinet Efficiency |

Werte sind **Designvorschläge**. Wenn mehr als ein Estate denselben Country-Malus beeinflusst, müssen deren Effekte additiv und nachvollziehbar sein. Die exakten Modifier-Namen/Scopes sind mit 1.4.9 zu prüfen.

## Nicht Teil von v0.1

Kabinettsaktion „Korruption bekämpfen“, umfangreichere Korruptionsfolgen, neue GUI-Panels, dynamische Estate-Actions, automatische Reform-Events und erweiterte KI-Logik. Diese sind spätere Ausbaustufen.

## Abnahmekriterien

1. Jeder steuerpflichtige Stand kann 100 % Steueranforderung wählen; alle bestehenden Vanilla-Max-Tax-Quellen wirken stattdessen auf Akzeptanz.
2. Ein abweichender Estate-Steuersatz über Akzeptanz erzeugt monatlich steigende Korruption nur bei diesem Stand.
3. Keine Korruption über 100 oder unter 0, auch bei extremen Modifiern.
4. Acht voneinander unabhängige Korruptionswerte überleben Speichern/Laden.
5. Alle acht Malusse skalieren linear mit dem eigenen Korruptionswert.
6. Alle bisher vorhandenen Loyalitätseffekte durch Steuern bleiben erhalten.
7. Tooltips, deutsche und englische Localization sowie Logs sind geprüft.
8. Alle Quellen und Testresultate nennen Build und Referenz-Snapshot.
