# CA-002 – gemessene Modell-RCA-Differenzen

**Messklasse: MODEL_RCA. Tatsächliche CA-Kosten und Editor-RCA-Gold bleiben
unbekannt.** Kein Punkt der folgenden Tabellen darf als bewiesener CA-Verbrauch
oder kostenloses Attribut im Spiel interpretiert werden.

Ausgeführt: die unveränderte [externe Funktion](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/apps/desktop/src/lib/ca.ts).
[Vorregistrierung](../../experiments/CA-002-model-diagnostic.md),
[Manifest](../../data/player-development-002-ca/manifest.json),
[alle Eingriffe mit Vorher/Nachher-Hash und Ergebnissen](../../data/player-development-002-ca/model-interventions.jsonl),
[vollständige Zusammenfassung](../../data/player-development-002-ca/summary.json).

## Ergebnis und Faktoren

1.620beschriftete Eingriffe, **1.539einzigartige Requests**.81Aliaswiederholungen:
DC20+MC20 und MC20+DC20 sind bei AUTO identisch. Originalzeilen bleiben
markiert erhalten.513einzigartige Attribut×Profil-Leveltripel;
**339davon niveauabhängig**. Differenzen0/1/2/3/4 treten470/570/413/84/2mal
auf, keine negativen, keine am200er-Cap. Iterationszahlen1–30; kein beobachtetes
100er-Timeout, aber auch kein allgemeines Konvergenzzertifikat.

Die Antworten innerhalb dieses Modells:

- **Niveau:** Preise variieren einschließlich Rundungs-/Verteilungseffekten;
  ein höheres Niveau ist nicht durchgehend teurer. ST-Antritt3/2/3 statt konstant.
- **Position:** GK-Beweglichkeit2/1/2 gegenüber ST1/1/1. Andere Attribute siehe
  vollständige Basistabelle unten. Position ist keine konkrete Rolle.
- **Füße/Zusatzposition:** ST-Antritt12→13 beträgt bei Füßen5/100 ohne MC2,
  mit MC20 dagegen1; bei Füßen50/100 mit MC20 beträgt er2. Diese Differenz
  enthält die AUTO-Maximumwahl und den Verteilungs-/Positionsalgorithmus.
- **Alter, Persönlichkeit, CA, PA:** keine Inputs der Funktion. Daraus folgt
  keine Engineunabhängigkeit und keine realistische Trainingsprognose.

## Nachvollziehbare Rechenstruktur, keine neue Naturgesetzformel

Für jede Positionsspalte wird ein gewichtetes Rohattribut-/Fußmittel W
berechnet; der dominante100er-Fuß wird dabei nach Quellregel ausgelassen.
Initialwert `max(1,floor(20*(W/5−6)))`. Die Funktion bestimmt aus allen
Positionsratings einen internen Parameter P, korrigiert abhängig von
Attributabweichungen und Kandidatenwert iterativ und skaliert nach
Positionsvertrautheit. AUTO wählt anschließend das höchste ganzzahlige,
auf1..200begrenzte Ergebnis. **P ist keine beobachtete CA-Kostendifferenz.**
Die Iteration, Schwellen und Rundung sind im verlinkten Quellcode vollständig
reproduzierbar; ein einzelnes Gewicht ist keine Ableitung der Gesamtfunktion.

Alle übrigen gewichteten Attribute sind Roh60, die Zielwerte40/60/85 werden
auf45/65/90angehoben. `raw=5×display` ist die deklarierte Szenarioskala.
Füße und Positionen bleiben innerhalb eines Attributvergleichs unverändert.
Fehlende Attribute füllt die Originalfunktion sonst mit1; unser vollständiges
Modellprofil vermeidet diese Quellenfalle. Zehn Familien×neun Attribute
einschließlich GK wurden vermessen. Keine echten Spieleridentitäten.

## Reale Exportdiagnose bewusst gestoppt

Der alte öffentliche109GK-Export besitzt vollständige Attribute, aber Füße
als Kategorien wie Weak/Reasonable. Kein unabhängig verifiziertes numerisches
Mapping. **109/109Inputs zurückgewiesen,0Modellaufrufe, MAE/RMSE/Bias/KI=null.**
[Alle Zeilen-/Fehlergründe ohne Identitäten](../../data/player-development-002-ca/export-diagnostic.json).
Keine willkürliche Fußimputation oder neue Genauigkeitsbehauptung gegen die
alten1,606MAE. Ebenso kein unabhängiger neuer Datensatz vorgetäuscht.

## Konsequenz für tatsächliche Effizienz

Die Quellengewichte und frühere fm-scoring-Tabelle stimmen bereits in ihren
Attributsummen nicht überall überein, z.B.ST116gegen107. Weder deren Verhältnis
noch die470ganzzahligen Nullschritte liefern echte kostenlose Verbesserungen.
Ein Leistungs-/Nullkostenquotient wäre insbesondere unzulässig.
**Welche Attribute pro echtem CA am effizientesten sind, bleibt offen.**

## Vollständige Basistabelle

Nur Hauptposition20, alle anderen0, Füße5/100; jede Zelle ist die Modell-RCA-
Differenz für den angegebenen Schritt. Fuß-/Mehrpositionsvarianten vollständig
in JSONL. Kein KI aus konstruierten Profilen.

| Position | Attribut |8→9|12→13|17→18|
|---|---|---:|---:|---:|
| GK | acceleration | 2 | 1 | 1 |
| GK | pace | 0 | 0 | 1 |
| GK | jumping_reach | 0 | 0 | 1 |
| GK | stamina | 0 | 0 | 1 |
| GK | anticipation | 0 | 0 | 1 |
| GK | finishing | 0 | 0 | 0 |
| GK | strength | 1 | 0 | 1 |
| GK | agility | 2 | 1 | 2 |
| GK | reflexes | 2 | 1 | 2 |
| DL | acceleration | 3 | 1 | 3 |
| DL | pace | 2 | 1 | 1 |
| DL | jumping_reach | 0 | 0 | 1 |
| DL | stamina | 3 | 1 | 2 |
| DL | anticipation | 1 | 0 | 1 |
| DL | finishing | 0 | 0 | 0 |
| DL | strength | 1 | 1 | 1 |
| DL | agility | 3 | 1 | 2 |
| DL | reflexes | 0 | 0 | 0 |
| DC | acceleration | 2 | 1 | 1 |
| DC | pace | 2 | 0 | 2 |
| DC | jumping_reach | 2 | 1 | 1 |
| DC | stamina | 1 | 0 | 1 |
| DC | anticipation | 2 | 0 | 2 |
| DC | finishing | 0 | 0 | 1 |
| DC | strength | 2 | 1 | 1 |
| DC | agility | 2 | 1 | 1 |
| DC | reflexes | 0 | 0 | 0 |
| WBL | acceleration | 3 | 3 | 2 |
| WBL | pace | 2 | 2 | 3 |
| WBL | jumping_reach | 0 | 1 | 1 |
| WBL | stamina | 2 | 2 | 3 |
| WBL | anticipation | 0 | 1 | 1 |
| WBL | finishing | 0 | 1 | 1 |
| WBL | strength | 1 | 1 | 1 |
| WBL | agility | 2 | 1 | 1 |
| WBL | reflexes | 0 | 0 | 0 |
| DM | acceleration | 2 | 1 | 2 |
| DM | pace | 1 | 1 | 2 |
| DM | jumping_reach | 1 | 0 | 0 |
| DM | stamina | 1 | 1 | 2 |
| DM | anticipation | 1 | 1 | 2 |
| DM | finishing | 0 | 0 | 1 |
| DM | strength | 1 | 1 | 2 |
| DM | agility | 2 | 1 | 2 |
| DM | reflexes | 0 | 0 | 0 |
| ML | acceleration | 3 | 2 | 3 |
| ML | pace | 2 | 2 | 2 |
| ML | jumping_reach | 1 | 0 | 0 |
| ML | stamina | 1 | 1 | 2 |
| ML | anticipation | 0 | 1 | 1 |
| ML | finishing | 0 | 1 | 1 |
| ML | strength | 0 | 1 | 1 |
| ML | agility | 2 | 2 | 2 |
| ML | reflexes | 0 | 0 | 0 |
| MC | acceleration | 2 | 1 | 2 |
| MC | pace | 1 | 1 | 1 |
| MC | jumping_reach | 0 | 0 | 0 |
| MC | stamina | 2 | 1 | 2 |
| MC | anticipation | 0 | 1 | 0 |
| MC | finishing | 0 | 0 | 0 |
| MC | strength | 1 | 1 | 1 |
| MC | agility | 2 | 1 | 2 |
| MC | reflexes | 0 | 0 | 0 |
| AML | acceleration | 3 | 3 | 3 |
| AML | pace | 3 | 3 | 3 |
| AML | jumping_reach | 0 | 1 | 1 |
| AML | stamina | 2 | 2 | 2 |
| AML | anticipation | 1 | 1 | 1 |
| AML | finishing | 0 | 1 | 1 |
| AML | strength | 1 | 1 | 1 |
| AML | agility | 2 | 2 | 2 |
| AML | reflexes | 0 | 0 | 0 |
| AMC | acceleration | 2 | 2 | 3 |
| AMC | pace | 2 | 1 | 2 |
| AMC | jumping_reach | 0 | 0 | 0 |
| AMC | stamina | 1 | 1 | 2 |
| AMC | anticipation | 0 | 0 | 1 |
| AMC | finishing | 0 | 0 | 1 |
| AMC | strength | 0 | 0 | 1 |
| AMC | agility | 1 | 1 | 2 |
| AMC | reflexes | 0 | 0 | 0 |
| STC | acceleration | 3 | 2 | 3 |
| STC | pace | 2 | 1 | 2 |
| STC | jumping_reach | 0 | 1 | 2 |
| STC | stamina | 1 | 1 | 1 |
| STC | anticipation | 0 | 1 | 2 |
| STC | finishing | 2 | 1 | 3 |
| STC | strength | 1 | 1 | 1 |
| STC | agility | 1 | 1 | 1 |
| STC | reflexes | 0 | 0 | 0 |
