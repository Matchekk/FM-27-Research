# TRAIN-004 – konkreter Nichtstart des Quickness-Piloten

15.11.2026. **NOT_STARTED_ACCESS_BLOCKED**.
[Vertrag](../../experiments/TRAIN-004-QUICKNESS.md).

| Notwendiges Gate | Tatsächlicher Status |
|---|---|
| Training/Fokus tatsächlich setzen | Kein verifizierter individueller Fokussetter |
| Setz-Readback | Kein abgeglichener Fokusreadback; GUI nicht erfassbar |
| Zulässige kontrollierte Fortschreibung | Kein nachgewiesener Karriereexecutor |
| Attribut-/CA-Endpunkte | Readerquellen vorhanden; kein neuer longitudinal kalibrierter Export |
| Unabhängige Ausgangskarrieren | Kein nachgewiesener Korpus von zwölf oder weniger geeigneten unabhängigen Paaren |
| Vollständige Armabrechnung | 0 gestartet, 0 abgeschlossen, 0 abgebrochen, 0 ausgeschlossen |

Vorhandene private Lesekopien aus alten Diagnoseverträgen liefern keinen
Nachweis unabhängiger RNG-Starts und werden nicht als neue Arme umetikettiert.
`research/career.py`/`research/training002.py` sind Import-/Diagnosewerkzeuge.
Die lokalen anderen Apps haben Fitness-/Moral-/PA-/Exportfunktionen, aber
keinen nachgewiesenen Quickness-Kalenderworkflow. Die fmsave-API v0.12.5 ist
kein Executor. Kein Spielschutz umgangen, kein neuer Controller gebaut.

Null Armwochen und Kalenderadvances; alle Endpunkte (ΔQuickness, CA, PA,
andere Attribute, Index, Minuten, Verletzungstage, Kondition/Schärfe),
Karrierepaar-SD und Konfidenzintervall **null/NOT_MEASURED**. Keine Effektrichtung
oder Trainingsentscheidung daraus möglich. Die 51 alten Pläne wurden nicht
erneut analysiert; ihre Vergleiche ersetzen keinen eigenen Fokusversuch.

Individuelle Anwesenheit ist allein **kein** ITT-Gate. Bei künftig belegter
Zuweisung, Fortschreibung und vollständiger Messung kann die Wirkung der
Zuweisung untersucht werden; tatsächliche absolvierte Dosis bleibt unbekannt.
Selbst zwölf vollständige Paare wären zunächst ein Durchführbarkeits-/Varianzpilot.
