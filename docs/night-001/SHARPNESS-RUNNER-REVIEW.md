# MECH-002-SHARPNESS-P0: unabhängiger Runnerreview

Stand 2026-11-14. **Code und inerte Vorbereitung freigegeben; keine Native-
oder Mainausführung durch diesen Review.** Geprüft: ursprünglicher Cold-Runner
`581b5a61777c804ae4fa00a68ce77cb9a8becbda`, danach Autorfix
`c993a9e51cdbccf9c472ad30e06f1fc4e166af08`. Keine verbleibenden blockierenden
Befunde im geprüften Runnerpfad. Der wissenschaftliche Vertrag und der46er-
Factoryfix haben einen getrennten Review. Konkrete Inputs,68 frische Seeds,
Publikation, exakte CI und nachfolgende Technik-/Maingates bleiben erforderlich.

LF-normalisierte Quellenbindungen:

| Quelle | SHA256 |
| --- | --- |
| `analysis/run_sharpness002.py` | `93e773263a0226a3f26c5d87d081fd4c1673445f123f468eafd8a6317ba2afa3` |
| `analysis/sharpness002_runner.py` | `268e6cc3d98dcca332dd118820fa9e09f8dc74584d43f9533955a7e0f97b8ec2` |
| neuer zentraler `analysis/night_supervise.py` | `117488289f1ea002d0832df757d9112e4e9a3a936f588a23ac635b8b65d00227` |
| unveränderter `research/native_process005.py` | `03c50200bb46c3daaeeba5901502f9eede04f2bba7ad04884b2d3dd6ebaa8faf` |

Der Masterstand wurde separat read-only als endgültiger neuer Rootdiff geprüft.
Er gehört zur neuen Sourcegeneration; frühere Observer-/TECH17-Quellen und
Reviews behalten ihre historischen Gitbindungen.

## Admission, atomare Claims und Prozessgrenze

Vorbereitung importiert keinen Server/NativeLab und startet keinen Host. Die
externe Registry wird nur gelesen:64Main- plus vier Technikseeds,68 eindeutige
gültige uint32, disjunkt zu öffentlichen/privaten Altbelegen und fremden
Reservierungen. Keine eigene Seedallokation, Rückerstattung oder Wiederholung.
Existierende Vorbereitung beziehungsweise Phasenartefakte verhindern Neustarts.

Ein ThreadPool mit vier Threads und ein gemeinsames Claim-/Stoplock begrenzen
admittierte Aufrufe auf vier. Ein Claim wird vor Prozessaufruf exklusiv und
dauerhaft protokolliert. Der erste erkannte Fehler setzt dasselbe Stopflag;
anschließend werden weder neue Claims noch spätere Blöcke aufgenommen.
Bereits vorher geclaimte Aufrufe dürfen ihren begrenzten Ablauf beenden und
bleiben abgerechnet. Deren GO kann nach einem anderen Workerfehler liegen;
eine stärkere sofortige Abbruchgarantie wird nicht behauptet.

Jeder einzelne Cold-Aufruf erhält seinen eigenen unveränderten Kernel-Job3:
Kapsel, Host und dessen Enginekind. Vier Claims begründen eine Obergrenze von
vier Enginekindern unter der unveränderten Hostarchitektur. Der Counter ist
ausdrücklich kein gemessener Peak tatsächlicher Engine-PIDs. Die Technikphase
muss vier gleichzeitige Claims und16 exakte A/A-Paare tatsächlich ausüben.
Kein Warmbetrieb, neues C++, Kind61, Setter oder fortlaufender Profilclamp.

Vor dem ersten möglichen Prozessstart steht je Aufruf ein dauerhafter
Pendingmarker. Nach betretenem Containmentpfad wird dieser ausschließlich bei
persistiert bestätigtem Kapselexit und Kernelnull mit erwartetem Limit3 entfernt.
Unbekannte Bereinigung hält Marker und globale4Worker-Lease zurück und haltiert
das Budget. Eine reine Gateabweisung vor Eintritt in die Containment-API startet
keinen Prozess und darf ihren eigenen Marker entsprechend entfernen.
Threadpoolabschluss wartet auf die bereits beanspruchten Aufrufe.

## Budget und Fehlerexport

Ein persistentes eigenes Budget umfasst33Technikplätze und512Mainplätze,
900s kumulierte überwachte Childzeit und ein unverlängertes3600s-UTCfenster ab
Technikreservierung. NIGHT1800s und23:00UTC bleiben zusätzliche Grenzen.
Je Call90s ohne Fortschritt und eine aus den verbleibenden Fristen begrenzte
Gesamtdauer. Private Artefaktgrenze2GiB, freier Speicher>20GiB.

Vor Main werden eigene und globale Childallowance, eigene UTCfrist, aktive
äußere Deadline und harte Nachtdeadline gemeinsam geprüft. Unmittelbar vor dem
ersten Containmentaufruf folgt ein atomarer erneuter600s-Check nach frischer
Admission. Der erste Call läuft dafür seriell unter dem eigenen FirstMainLock;
danach folgen normale begrenzte Cold-Aufrufe mit erneut aktueller Admission.
Die600s-Regel wird bei späteren Matches nicht nochmals als Startschwelle
verlangt. Die erste tatsächliche API-Allowance ist zusätzlich auf den geprüften
Rest begrenzt. Warten auf den ersten Call darf keine alte Allowance fortschreiben.

Parentbudget, exakte Phasen-/Reservierungsschlüssel, zeitliche Bounds,
Chargensumme, unveränderter UTCrahmen und post-Lease-Reconciliation sind für
Erfolg erforderlich. Jetzt muss auch `op_start + elapsed <= child_deadline`
gelten. Ein positives Childsummary allein gibt keine Auswertung frei. Nach
Parentfehler, Timeout, fehlender Reconciliation oder unbekanntem Cleanup werden
Status und vollständige Attemptabrechnung exportiert, keine neuen Main-
Performancezeilen. Unbekannte verrechenbare Zeit bleibt null; der rohe erfasste
Chargewert bleibt getrennt und private Token-/argv-/Pfadfelder bleiben verborgen.

## Quellen, Readbacks und öffentliche Freigabekette

TECH17 benötigt tatsächliches unabhängiges Release, Summary-/Ergebnisreviewhash,
veröffentlichten Releasecommit und erfolgreiche exakte CI. Dessen frühere
Codehashes werden gegen registrierte historische Gitblobs geprüft, damit ein
zulässiger neuer Master die alte Abnahme nicht fälschlich verändert.
Fehlende reale TECH17-Freigabe blockiert bereits vor Factory/Seedplanvorbereitung.

Der neue Runner und Master wählen vor Projektimports einen frischen nachgewiesen
absenten UUID-Cacheprefix und deaktivieren Bytecodewrites. Direkte CLI-Einstiege
weisen vorgeladene Projektmodule ab. Namespace-/Shadowmodule einschließlich
`analysis/__init__.py`, `.pyc`, `analysis.py` und `.pyc` sind ausgeschlossen;
`research/__init__.py` ist im Runner-CODE gebunden. Bestehende Caches werden
nicht gelöscht oder überschrieben.

Vor Native werden Host, Fixture, Ressourcen, Buildmanifest, C++-/Headerquellen,
Katalog, Konfigurationen und alle Inputs über eigene Windows-Lesehandles gegen
Schreiben/Löschen geschützt und unter diesen Handles erneut gehasht. Der
ursprüngliche Runtime-/Leasequellstand und die deklarierte Software werden
geprüft. Die erwarteten Identitäten bleiben Engine27.0.1+2503222/SHA8c697…e340
und Observerhost58e05…d32. Dieser Codereview beansprucht keine neue Ausführung
oder Live-Neumessung dieser Spielartefakte.

Jeder Vollmatch fordert komplette Attribute/Profile, beide tatsächlichen
Taktikphasen, Rollen/PI, Seed-/Setupidentität, natürliche Enden und Originalstats.
Stamina bleibt bei allen46 aktiven Actors60. Beide Sharpnessrohfelder und
Startercaches müssen prepared/first den deklarierten Wert tragen; unveränderte
Anfangsfelder/33TF-Bytes sind an D00-Gold gebunden. Fehlende Finishedcaches
bleiben null mit Grund. Die15 deskriptiven Größen begründen keine zusätzlichen
Signifikanz- oder UI-/Consumerbehauptungen.

Register bindet zuerst veröffentlichte Draftinputs samt unabhängigen Inputreview.
Danach werden registrierter Manifest und komplette33/512-Jobpläne veröffentlicht
und erneut auf exakte erfolgreiche CI geprüft. Main benötigt zusätzlich eine
eigene tatsächlich bestandene Cold-Technikreihe mit32Full/16A/A/108-Negativprobe,
abgeglichenem Budget, unabhängigem Technikreview und veröffentlichter Freigabe.
Kein automatischer Mainstart nach Prepare oder erfolgreicher Techniksummary.

## Tatsächlich geprüfte Regressionen

Drei eigene Gegenversuche waren auf581b5a6 rot: akzeptierte Childdeadline-
Überschreitung, ausgeführter fremder timestamp-valid PYC trotz unveränderter
Helperquelle und `FileNotFoundError` beim regulären Entfernen eines parallelen
Pendingmarkers zwischen `is_file`/`stat`. Die Korrekturen bestehen diese Fälle.
Der Zähler verwendet nun ein einzelnes stat je Pfad und ignoriert gezielt
verschwundene Dateien; andere I/Ofehler bleiben Fehler.

Alle17 Autortests und fünf eigene Reviewerfälle bestehen, zusammen22 gezielte
Tests. Die eigenen Fälle prüfen zusätzlich das tatsächliche600s-API-Gate sowie
einen echten temporären Master-PYC-/Namespace-Gegenversuch. Separat bestehen
alle zwölf zentralen Router-/Mastertests. Der Router verlangt genau33Technik-
schlüssel beziehungsweise512Mainjobs,64 unterschiedliche Seeds,32 Blöcke je
Kontext, jeweils beide Seiten×vier Arme und die registrierte SHA-Sortierung.
Die alte TECH17-Route erlaubt weiterhin keinen Main.

Eigene Tests: `tests/test_sharpness002_runner_review.py`. Im separaten Worktree
zeigt `FM_RESEARCH_MASTER_SOURCE_ROOT` für den Mastertest ausdrücklich auf den
geprüften zentralen Diff; integrierte CI nutzt ihren eigenen Repositoryroot.
Nur eigene temporäre Pythonquellen und harmlose Python-CLI-Kinder, keine
Upstreamkopie, Hosts, Saves, Registrywrites oder Seedreservierungen. Der
veröffentlichte vollständige Sourcefreeze und konkrete Inputreview stehen vor
jeder nachfolgenden tatsächlich zugelassenen Phase.
