# NIGHT-002 – konsolidierter Forschungsbericht

**Zwischenstand vor erster nativer Ausführung.** Dieser Bericht wird mit
tatsächlich abgeschlossenen Abschnitten ergänzt; geplante Studien sind keine
gemessenen Befunde.

## A. Neue Forschungsfragen

[Zehn geprüfte Kandidaten](NOVELTY_MATRIX.md) mit Hypothese, Überschneidung,
Novelty-Entscheidung, Endpunkt, Kontrolle, Einheit, Confoundern, Aufwand und Nutzen.
Beste drei: getrennte C90/C7A-Attribution; kontrolliertes ST→AMC-IP-Paket bei
fester OOP-Struktur; Nettoertrag tatsächlich ausgeführter Ecken.
Zuerst wird MECH-004-SPLIT-R0 technisch geprüft. [Quellenrefresh](LITERATURE_AUDIT.md)
ergänzt unter anderem Puritys neuen Torwartnachtrag und aktualisiert den
dynamischen FMAX-Stand. Externe Zahlen bleiben Autorenangaben, keine eigene Replikation.

## B. Tatsächlich ausgeführte Studien

Bis zu diesem Zwischenstand: **0 Hauptmatches,32 technische Vollmatches,
1 erwartete Negativabweisung** in NIGHT-002. MECH-004 ist registriert auf Vorregistrierungscommit
`0e535dc`, [CI43648809178 erfolgreich](https://github.com/Matchekk/FM-27-Research/actions/runs/43648809178).
Der registrierte vollständige Jobplan wurde vor Technik veröffentlicht.
Alle32 technischen Matches und16 exakte A/A-Paare bestanden; beide Felder
überstehen Vorbereitung/Erstfortschritt getrennt. Der Cache8A folgt in allen
gekreuzten Startaufnahmen C90 (70/100), unabhängig von C7A. Noch kein Matcheffekt.
[Technischer Bericht](../../experiments/MECH-004-split-validation.md).
[Unabhängige technische Rohabnahme](SPLIT004-TECHNICAL-REVIEW.md) bestanden;
Mainfreigabe liegt als konkretes Gate vor und benötigt öffentliche erfolgreiche CI.
Eigene Phasenchildzeit78,533s, global107,962s; separat110,736 summierte native
Callsekunden.0 unerwartete Fehler,0 Retries/Ersatzseeds, vollständige Bereinigung.
Historische MECH-002-Zahlen werden nicht als neue Messungen gezählt.

## C. Technische Fortschritte

Neue separate Missionsbudget-/Admissionmodule und Splitcompiler-/Readback-/
Analysemodule sind offline implementiert. Aktuelle fokussierte Tests:22 bestanden.
Gesamtsuite403 durchlaufen (402bestanden,1Skip), fünf Analysetests sowie alle
bestehenden CI-Archiv-/Ergebnisverifier bestanden.68 neue Seeds wurden gegen2597
historische/reservierte Werte geprüft; konkrete Inputs sind offline erzeugt.
Der konkrete [Inputreview](SPLIT004-INPUT-REVIEW.md) hat alle16 Eingaben,
68disjunkte Seeds und unveränderte Ressourcen unabhängig akzeptiert.
Vorregistrierung/CI sind veröffentlicht; registrierter Jobplan und native
Splitabnahme bleiben vor Main erforderlich.
Der Director hat den von einem anderen Agenten geschriebenen Missionscontroller
separat auf Authentifizierung, feste Limits, strikte Argumente und Leasegrenzen geprüft.
Das tatsächliche neue Transfergate ist nun bestanden; die frühere reine
Offlinevorbereitung wird davon unterschieden. [Sicherheit](SAFETY_ASSESSMENT.md)
und konkrete Input-/Runnerreviews lagen vor dem ersten Aufruf vor.

## D. Praktische Konsequenzen

Noch keine neuen eigenen Spieler-/Taktik-/Trainingsempfehlungen.
Meta-Scorev0.1 bleibt unverändert und unvalidiertes Prognosemodell.
Getrennte Rohfeldattribution könnte die Interpretation des alten Schärfepakets
verbessern; eine UI-Skala oder natürliche Karrierewirkung folgt daraus nicht.

## E. Kritische Bewertung

Bislang Quellenklärung und überprüfbare Versuchsplanung, keine neue bestätigte
Enginewirkung. Der Forschungswert hängt vom tatsächlichen Transfergate und
gegebenenfalls nachfolgenden neuen Seedmessungen ab. Fehlende Gates werden
als Blocker dokumentiert und nicht als Effekte dargestellt.

## F. Nächste Prioritäten

1. MECH-004: konkrete publizierte Inputs/Review/CI, dann technische Splitidentifikation;
   nur nach unabhängiger Freigabe begrenzter Hauptpilot.
2. ST→AMC: kontrollierbare Originalpositionen/-rollen und feste OOP-Identitäten
   offline prüfen, bevor ein separater nativer Vertrag entsteht.
3. SET: reale Ausführungs-/Schuss-/VAR-/Konterketten zunächst technisch lesbar
   und mit Goldfällen prüfbar machen; keine Wirksamkeitsserie ohne Nenner.
