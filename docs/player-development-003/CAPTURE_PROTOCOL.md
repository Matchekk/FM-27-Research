# Externe Editor-Goldmessung – sofort nutzbare technische Übergabe

**Keine Messdaten, kein wissenschaftliches Ergebnis.** Nur auf isolierten,
autorisierten Wegwerfprofilen verwenden. Zuerst Original sichern und hashen;
erst nach unabhängig überprüftem Editorzugang beginnen.

## Einmaliger Herkunfts-/Skalennachweis

Editorname/Version, Spielruntime-/Savebuild und Datum notieren. Belegen, dass
das Feld wirklich Recommended Current Ability berechnet und STORED_CA separat
vorliegt. Quellen-/Funktionsherkunft dokumentieren; eine Scout-Portierung oder
FMRTE-Schätzung ist ohne weiteren Nachweis kein unabhängiges Engineorakel.
Native Engine-RCA und unabhängig implementierte Editor-RCA als unterschiedliche
Referenzklassen führen; Letztere validiert nur gegen diesen belegten Editor.

Alle 40 Modellrohattribute, zusätzlich Determination/Natural Fitness/Flair/
Aggression, beide numerischen Fußwerte und alle 15 Positionsratings auslesen.
Nicht sichtbare Werte bleiben null. Modellskalen: Attribute 1..100, Füße 0..100,
Positionen 0..20; der tatsächliche Messweg und seine Umrechnung müssen belegt
sein. UI-Rundwerte×5 sind kein Nachweis gleicher Rohprofile. Originalexporte,
Screenshots und Identitätsmapping privat sichern; nur erlaubte pseudonymisierte
Messungen nach gesonderter Inhaltsprüfung veröffentlichen.

## Zwölf Pilotfälle – noch nicht ausgeführt

Je Familie dieselbe gemessene Ausgangsidentität; andere Felder zunächst
vollständig aufnehmen. Zwei Edits jeweils von deren unverändertem Original,
keine kumulierte Eingriffsfolge. Sechs gewünschte Basisidentitäten, tatsächliche
Baselinehashzahl gesondert zählen. Nur wenn die exakten Ausgangswerte in einer
Zielkopie reproduzierbar gesetzt/gelesen werden können, diesen Fall starten.

| ID | Familie | Genau ein Feld | Ausgang→Ziel im Modellrohmaß |
|---|---|---|---|
| G01 | GK | acceleration | 40→45 (8→9) |
| G02 | GK | reflexes | 60→65 (12→13) |
| S01 | ST | pace | 85→90 (17→18) |
| S02 | ST | left_foot | 5→50; right_foot konstant 100 |
| D01 | DC | jumping_reach | 60→65 |
| D02 | DC | acceleration | 85→90 |
| M01 | MC | pace | 40→45 |
| M02 | MC | positions.dm | 0→15; MC konstant 20 |
| A01 | AML | acceleration | 60→65 |
| A02 | AML | pace | 85→90 |
| L01 | DL | strength | 40→45 |
| L02 | DL | right_foot | 100→50; left_foot konstant 5 |

Die übrigen Startwerte müssen vor Goldsichtung eingefroren werden; die Tabelle
ist kein vollständiger Profilfreeze. MC20/DM0 bleibt die Baseline von M02;
MC20/DM15 im Nachzustand liefert die Mehrpositionsabdeckung. Keine stille
Änderung einer Tabellenzeile nach Goldsichtung.

## Pro Fall

1. Eine Zeile der [JSONL-Vorlage](../../data/player-development-003/editor-capture.template.jsonl)
   in eine **private** Erfassungsdatei kopieren. Pseudonyme statt echter Namen/
   UIDs; `baseline_id` verbindet wiederholte Edits desselben Ausgangsprofils.
2. Original- und Zielkopie eindeutig identifizieren; Originaldateihash und
   vollständigen Vorherexport sichern. Privates Original nie überschreiben.
3. Baselineprofil, STORED_CA und EDITOR_RCA zweimal unverändert lesen. Quelle,
   Skalen, Timestamp, Hash der Originalbelege und Builds eintragen.
4. Genau das deklarierte Feld ändern. Alle Profilfelder, CA und RCA erneut
   lesen. Bei Drift/Buildwechsel/ungeklärtem Feld keine Wirkungsinterpretation;
   Zeile mit Fehlergrund erhalten. Keine Karrierefortschreibung in CA-003.
5. Kanonische Profilhashes mit `analysis.ca_costs002.digest(profile)` bilden.
   Darin sind `model_request` **und** die vier Zusatzattribute enthalten.
   Rohdateihashes zusätzlich separat führen. Nicht aus einem Nachherhash
   rückwirkend ein Original ableiten. `MODEL_RCA` erst danach berechnen.
6. Für jede neue Zeile Erfolg, Fehler oder Abbruch explizit führen. Ein leerer
   Templateeintrag ist kein gestarteter Fall. Anschließend Zielprozess geordnet
   schließen, falls für den Versuch gestartet; Originalhash erneut prüfen.

## Bestehenden Comparator und Analyse wiederverwenden

Keine neue Rechnerimplementierung erforderlich. `source_keys` prüft den
gepinnten Quellhash; `evaluate` führt die Originalfunktion mit A/A aus;
`metrics` berechnet Fehlerstatistiken. Beispiel für eine **einzelne zuvor
menschlich verifizierte vollständige Zeile**; nicht auf private Daten in Git ausgeben:

```python
import json
from pathlib import Path
from analysis.ca_costs002 import source_keys, evaluate, metrics, digest, SLOTS

source = Path('local/player-development-003/sources/ca-pinned.ts')
row = json.loads(Path('local/player-development-003/verified-case.jsonl').read_text())
keys = source_keys(source)
assert row['status'] == 'VERIFIED_GOLD_CAPTURE'
assert row['source']['independent_rca_verified'] is True
assert row['source']['independence_evidence_sha256']
assert row['source']['scale_evidence_sha256']
assert row['source']['game_runtime_build'] and row['source']['editor_build']
profiles = [row[side]['profile'] for side in ('before', 'after')]
for side, profile in zip(('before', 'after'), profiles):
    state = row[side]
    req = profile['model_request']
    assert set(req['attributes']) == set(keys)
    assert set(req['positions']) == set(SLOTS) and req['position'] == 'AUTO'
    for mapping, low, high in ((req['attributes'], 1, 100), (req['positions'], 0, 20),
                               (profile['extra_attributes'], 1, 100)):
        assert mapping and all(type(v) is int and low <= v <= high for v in mapping.values())
    assert set(profile['extra_attributes']) == {'determination', 'natural_fitness', 'flair', 'aggression'}
    assert all(type(req[k]) is int and 0 <= req[k] <= 100 for k in ('left_foot', 'right_foot'))
    assert state['input_sha256'] == digest(profile)
    assert state['evidence_sha256'] and state['observed_utc']
    assert type(state['EDITOR_RCA']) is int and 1 <= state['EDITOR_RCA'] <= 200
    assert type(state['STORED_CA']) is int and 1 <= state['STORED_CA'] <= 200

def flatten(value, prefix=''):
    if isinstance(value, dict):
        return {p: v for k, x in value.items() for p, v in flatten(x, prefix + k + '.').items()}
    return {prefix[:-1]: value}
b, a = map(flatten, profiles)
changed = [k for k in b if b[k] != a[k]]
assert changed == [row['changed_field']]
assert b[changed[0]] == row['from_raw'] and a[changed[0]] == row['to_raw']
assert row['before']['STORED_CA'] == row['after']['STORED_CA']
outputs = evaluate(source, [p['model_request'] for p in profiles])
for side, output in zip(('before', 'after'), outputs):
    row[side]['MODEL_RCA'] = output['estimated_ca']
errors = [o['estimated_ca'] - row[s]['EDITOR_RCA']
          for o, s in zip(outputs, ('before', 'after'))]
print({'MODEL_RCA': {s: row[s]['MODEL_RCA'] for s in ('before', 'after')},
       'errors': errors, 'descriptive_two_states': metrics(errors),
       'exact_matches': sum(e == 0 for e in errors),
       'delta_error': errors[1] - errors[0]})
```

Der Herkunftsbool ist eine dokumentierte menschliche Prüfung, kein automatisch
bewiesenes Gütesiegel. Assertions sind Bedienhilfen; nicht mit `python -O`
ausführen. Das Beispiel ersetzt nicht die vollständige Hauptserienauswertung:
gemeinsame Baselines deduplizieren, alle fehlenden/gestarteten Fälle erhalten,
Positions-/Niveau-/Fußgruppen und Cluster wie im Vertrag auswerten. Für null
Goldzeilen **metrics nicht auf ein leeres Array anwenden**; alle Schätzer null.
Vorhandene gezielte Prüfungen: `tests.test_ca_costs002` für Inputhash,
Einzeländerungen, Duplikate, Quellenhash und Missing-Fußdaten. Kein neuer
allgemeiner Validator wurde für einen noch fehlenden Messzugang gebaut.
