# MECH-002-STARTPOLICY-TECH-V1 – ursprünglicher Eingabepfad bestanden

16technische Vollmatches,8exakte A/A-Paare,8Anfangskontrollpaare und eine
erwartete108-Abweisung vollständig abgeschlossen.4neue Seeds,1serieller Worker,
0Ausfälle/Retry/Ersatzseeds/Holdouts. Veröffentlichung und erfolgreiche
[CI43636256046](https://github.com/Matchekk/FM-27-Research/actions/runs/43636256046)
auf `0744238cbcbd429dd59602f0470b18a1d9f52057` gingen jeder Probe voraus.

Der unveränderte historische Codec verändert ausschließlich je zehn tatsächliche
Feldstarter im getesteten Team: zwei Profilrecords pro Spieler, C90/C7A als
Rohpaket7000 beziehungsweise10000. Die Controls sind bytegleich mit D00.
Keine Attribute, Rollen, PI, Gegner- oder Bankprofile wurden verändert.

Nach **Originalvorbereitung und erstem Originalfortschritt** erreichen die beiden
Rohfelder7000/7000 und der gesonderte Cache8A70. Die Highkontrolle bleibt
10000/10000/100.320gezielte Actor-Stage-Übertragungen und704initiale Startercaches
sind direkt nachgerechnet. Sämtliche nicht intervenierten Anfangswerte und die
33-Byte-Rohregion stimmen zwischen den Armen überein.

Damit ist kein neuer nachträglicher Setter nötig, um dieses gemeinsame
Rohpaket im geprüften Kontext wirksam zu übertragen. Der Host wurde nicht
geändert, Kind61/Executionhooks bleiben aus. Am Ende der Lowläufe steigt C90
bereits bis mindestens7783, während C7A weiterhin bei7000 liegen kann:
der Test erzwingt keinen permanenten Low-Finishclamp. Die genaue UI-Bedeutung
und ein bestimmter weiterer Consumer sind dadurch nicht kalibriert.

[Unabhängiger Rohreview](STARTPOLICY-002-RESULTS-REVIEW.md) rekonstruiert22
eingefrorene Gitblobs, alle16×3Snapshots/2208Actor-Stages sowie50.784Attribute,
16.928Profilwerte, Phasen und PI.17Kernelbereinigungen, genau eine erfolgreiche
Abrechnung und das finale Reconciliationreceipt bestehen.
58,0844142von180inneren Sekunden;900s-Fenster eingehalten.
Globaler NIGHT-Stand170,4746041von1800Childsekunden.

[Messungen und17Jobplätze](../../data/mech-002-startpolicy-tech/README.md)
bleiben anonym öffentlich; native Dumps/Rohspielmaterial bleiben privat.
Keine wissenschaftliche Leistungswirkung wurde aus diesen Technikseeds geschätzt.
Kein Warmbetrieb, Karriere-/Trainingsversuch, UI-Prozentwert oder allgemeiner
Familiarityeffekt freigegeben. Eine separate Leistungsfrage benötigt eigene
neue Seeds, Vorregistrierung, konkretes Design, technische Abnahme und CI.
