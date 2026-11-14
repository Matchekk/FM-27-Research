# MECH-002-SHARPNESS-P0: unabhängiger Abschlussreview

14.11.2026. **512/512 Hauptmatches und vollständige gespeicherte Auswertung
unabhängig geprüft, bestanden.** Es wird ausschließlich die Abnahme und
Publikation des bereits abgeschlossenen Piloten freigegeben. Keine neue
Simulation, Seedreservierung, Optimierung oder weitere Studie ist damit
autorisiert. Kein Computer-Use und kein eigener nativer Start dieses Reviewers.

## Unabhängige Beweisführung

Gelesen wurden alle512 stabil exportierten privaten nativen Logs, Inputdumps,
Exit-/Job3-/Processbelege, Claim-/GO-Marker, das vollständige Stop-/Counterledger,
beide festen Budgetoperationen und die Parentabrechnung. Alle16 Inputvarianten,
27 eingefrorenen Quellen, ursprünglichen Kontrollen und die unveränderte68er-
Seedreservierung wurden erneut geprüft. Es gibt64 neue unabhängige Mainblöcke,
32 je festem Gegnerkontext, beide Seiten und vier Arme; vier Technikseeds bleiben
getrennt. Historische/reservierte2528 Seeds sind ausgeschlossen. Kein Holdout,
Karrierereplay, Ersatzseed oder Ergebnisausschluss.

Vor Main tatsächlich veröffentlichter Commit:
`0adf47b5a431fd15e9274e12fd470ac113e60a29`, erfolgreicher
[CI-Lauf43643614021](https://github.com/Matchekk/FM-27-Research/actions/runs/43643614021).
Die API weist exakten Commit, `completed`, `success` und Abschluss21:37:44UTC
nach; vor Mainoperationsstart21:39:55.841134UTC. Alle45 für diesen Start
gebundenen Gitblobs stimmen mit den geprüften Dateien überein, einschließlich
technischer Freigabe und unabhängig geprüfter Duplikatentscheidung
`REPLICATION_WITH_TRANSFER`. Primärziel, Holm7, Eingaben und Seeds wurden durch
den parallelen Atlas-/Scoutimport nicht geändert. Die Quellen27 bleiben
unverändert; fremde Arbeit wird durch diesen Review nicht überschrieben.

Für jedes Match werden tatsächliche native Eingaben direkt aus Binärrecords,
Dumpbytes, Katalog und eingefrorener D00-Konfiguration nachgerechnet:3174
Attribute,1058 Profile,44 Phasenzellen und748 PI-Gruppen. Alle46 aktiven
Staminawerte bleiben60. Beide Startfelder und tatsächliche Startercaches tragen
das deklarierte Paket in Vorbereitung und erstem Advance; Kontrollfelder und
Raw33 sind unverändert. Geladene DLL, Kompatibilität, Seed und natürliches Ende
stimmen. Buildbindung27.0.1+2503222/DLL8c6971ce…340, unveränderter
Observer58e05a46…d32 und v1114.6/91f2eba… bleiben bestehen.

Insgesamt neu rekonstruiert:1536 Snapshots,70656 Akteursbeobachtungen,
1625088 Attributwerte,541696 Profilwerte,22528 Phasenzellen und382976 PI-Gruppen.
512 Claims und512 Abschlüsse, Peak vier Aufrufplätze, kein Stop-/Fehlerevent.
Für alle512 Jobs: Job3-Flags0x2008, Mitgliedschaft vor GO, kein Breakaway,
bestätigtes Kapselende und Kernelprozesszahl null. Kein behaupteter gemessener
Engine-PID-Peak. Keine offene Lease oder Pending-/Fehlermarker.

## Statistik aus originalen Scores und xG

Die unabhängige Berechnung ruft weder `analyse()` noch Projekt-Statistikfunktionen
auf. Aus originalen getestetseitigen Scores folgen Punkte3/1/0 und GF/GA, aus
Originalteamstatistik xGF/xGA und xGD. Physische Kontraste werden algebraisch aus
den vier Armen gebildet, dann Seiten innerhalb jedes Seeds gemittelt und beide
Kontextmittel mit je1/2 gewichtet.512 Matches werden nicht als512 unabhängige
Einheiten behandelt.

Alle acht vorregistrierten Kontrast-/Endpunktkombinationen stimmen: Mittelwerte,
gepaarte Kontext-/Seiten-SD und Kovarianzen, Welch-Satterthwaite-Freiheitsgrade,
95-%-Intervalle und p-Werte,20.000 deterministische stratifizierte Seedblock-
Bootstrapziehungen, Leave-one-seed-out und exakt Holm7. Alle512 gespeicherten
abgeleiteten Seedkontraste sind einzeln nach Identität, Reihenfolge und Wert
nachgerechnet. Die sieben Sekundärtests bilden eine eigene Holmfamilie; keine
simultane95-%-Abdeckung aller marginalen Intervalle wird behauptet.

| Vorregistrierter Kontrast | Effekt/Match |95-%-Welch-KI |p beziehungsweise Holm7-p |
| --- | ---: | --- | ---: |
| Paket10000−7000: xGD, primär |+0,476925 |[+0,321770;+0,632081] |7,8311×10⁻⁸, primär unadjustiert |
| Paket: tatsächliche Punkte |+0,441406 |[+0,242178;+0,640635] |0,000235701 |
| Paket: erzielte Tore |+0,445313 |[+0,231336;+0,659289] |0,000517253 |
| Paket: Gegentore |−0,359375 |[−0,556425;−0,162325] |0,001701322 |
| Paket: xGF |+0,270407 |[+0,170723;+0,370092] |0,0000100514 |
| Paket: xGA |−0,206518 |[−0,311135;−0,101901] |0,000845701 |
| Pressing: xGD |+0,097043 |[−0,059296;+0,253381] |0,438707465 |
| Paket×Pressing: physische xGD-DoD |−0,089083 |[−0,451897;+0,273732] |0,624879813 |

Primär-SE0,0774946580, Freiheitsgrade57,4254998. Bootstrap95-%-Intervall
[0,3259724182;0,6239906062]. Volle Welchbreite0,3103109208 unterschreitet das
Präzisionsziel0,50; die Untergrenze liegt im geprüften Kontext über der
vorab genannten praktischen Referenz0,30. Der Versuch bleibt der registrierte
Varianzpilot ohne vorab garantierte90-%-Power, keine nachträglich umbenannte
allgemeine Bestätigung.

Explorative Kontextmittel0,6217905723/0,3320595328; Block-SD0,7020151900/
0,5252320364. Einseitige95-%-Normalmodell-SD-Obergrenzen0,8901586943/
0,6659967909; Seitenkovarianzen0,0718391104/−0,1897090799. LOO-Mittel reichen
von0,4591497731 bis0,5061515423, maximale Änderung0,0292264898. Kontext- und
Seitenaussagen bleiben explorativ, die zwei Gegner sind keine Zufallsstichprobe
einer Gegnerpopulation. Alle Armmittel und15 deskriptiven Familien sind
unabhängig abgeglichen; tatsächlich0 Missing, keine Nullimputation.

## Bedingte neue Fallzahlen, keine neue Ausführung

Eine eigene lineare ganzzahlige Suche reproduziert die gespeicherte binäre
Fallzahlplanung für0,20/0,30xGD bei90% bedingter Power und zweiseitigemα0,05.
Gleiche feste Kontextgewichte, nichtzentrale Welchapproximation;2n unabhängige
Blöcke und16n Matches. Verwendet werden die tatsächlich nachgerechneten SDs
beziehungsweise simultane95-%-Normalmodell-Obergrenzen0,9333148562/0,6982852643
(je97,5%,df31). Kein verteilungsfreier oder neuer Karriere-Powerbeweis.

| Varianzannahme | Effekt |Neue Seeds/Kontext |Neue Blöcke |Neue Matches |
| --- | ---: | ---: | ---: | ---: |
| beobachtete SD |0,20 |52 |104 |832 |
| beobachtete SD |0,30 |24 |48 |384 |
| simultane SD-Obergrenze |0,20 |91 |182 |1456 |
| simultane SD-Obergrenze |0,30 |41 |82 |656 |

Alle tatsächlichen Planungswerte sind endlich und reproduziert. Der neue
Reviewer lehnt nichtendliche Planungswerte ausdrücklich ab. Die Zahlen sind
bedingte Modellrechnungen, kein automatischer Folgeauftrag. Keine neue
Forschungsrunde oder weitere gleichartige Simulation wird empfohlen oder gestartet.

## Vollständige Fehler- und Ressourcenabrechnung

512 gültige Mainmatches plus32 gültige technische Matches und eine erwartete
initiale Negativabweisung:545 geplante/abgerechnete Jobs,544 Vollmatches,
0 unerwartete Fehler,0 unaufgelöst,0 unbegonnen,0 Ersatz/Retry. Die vorhandene
öffentliche545er-Abrechnung wurde selbst als unveränderte Konkatenation beider
vollständigen Phasenabrechnungen geprüft. Die öffentlichen Mainmessungen stimmen
zeilenweise mit den privaten Rohrekonstruktionen überein.

Main498,59333940000215s; kumuliert560,5738462000008/900 eigene Childsekunden.
Globale Parentcharge792,1520872000037/1800s, äußerer Mainaufschlag523,1764172s.
Die unmittelbare erste Mainadmission um21:40:31.240763UTC ergibt aus den
tatsächlichen Operationen und Fristen unabhängig792,625864s Rest und besteht
das600s-Gate. Kein Budgetreset oder Verlängerung. Eigener Uhrstart
21:11:09.377746UTC, strengere eigene Deadline22:11:09.377746UTC; NIGHT23:00UTC.
Tatsächliche finale Reconciliation21:48:14.474332UTC liegt vor beiden Grenzen.
Finaler privater Budget-SHA256:
`66d6700177e24f979229bcdee03b013594a91dc2a080cf9d888bd31dea826e1b`.

## Dauerhaft prüfbare öffentliche Auswertung

`python analysis/review_sharpness002_results.py public-main --central <Archiv>`
prüft die gespeicherten `effects.json` und `seed-contrasts.jsonl` vollständig
gegen die eigene Score-/xG-Rechnung sowie registrierte Quellen und Analyse-
Provenienz. Die CLI gibt nicht bloß eine neue Zahl aus. Gezielte Tests verändern
Mittelwert, Holmwert, Bootstrap, SD, Kovarianz, Powerfallzahl, Nichtendlichkeit,
Seedkontrast, Rohscore und unzulässige Karrierebehauptung. Zusätzliche echte
Dateitests verändern gespeicherte Effekte beziehungsweise Blöcke und aktualisieren
deren Checksummen absichtlich; die CLI weist beides aufgrund der unabhängigen
Mathematik trotzdem ab. Nach Publikation prüft ein Repositorytest die tatsächlich
gespeicherten Mainartefakte bei zukünftiger CI erneut.

Die kompakte[eigene Main-Evidenz](../../data/mech-002-sharpness-p0/main-evidence-review.json)
bindet private Rawrekonstruktion, tatsächliche Publikations-CI, alle acht
unabhängigen statistischen Resultate, Powerplanung,545er-Abrechnung und Budgets.
SHA256 mit ausschließlich CRLF→LF:
`58db80e1564b27fe743a6afe51f622de80a4c8658bc6a478e7823c29fc3438e8`.
Bestehende Mainmessungen enthalten bereits alle512 erlaubten Messzeilen und
Raw-/Dump-/Cleanuphashes; sie werden nicht dupliziert oder überschrieben.
Rekonstruiertes privates Main-Artefaktmanifest:
`faea1fc8e9004f3bd77ebc5f4e060fc95b39821737e4258b472b90f7f808825a`.

Gegenprüfungen der zentralen Artefakte, SHA256 über öffentliche LF-Textbytes:

| Artefakt | SHA256 |
| --- | --- |
| `main.jsonl` | `593ad0dc202c86339f762e913c15d37d4be85ee4139a1b4cb14a6076c1c670c4` |
| `effects.json` | `bb0714ddbd34c2fb478a1b51df54baef7a04cedc101d974c99859ae9c0bfe33a` |
| `seed-contrasts.jsonl` | `938496e71a82077ac304c4ce2efeb3685e0a9c20110ccc7de6dc6f7c65c575b9` |
| `complete-job-accounting.jsonl` | `c077c7df9944bf0337e12a7d5178075e3b3e4ec1e5d7a42720f7cacb7b19a375` |

Der Directorentwurf `experiments/MECH-002-sharpness-results.md` wurde zusätzlich
auf sämtliche dargestellten Zahlen, Rundungen und Aussagegrenzen geprüft.
Die dortige vorläufige Review-Pending-Zeile kann nach Integration dieser Abnahme
entfernt werden. Die eigentlichen Studien-/Analyseartefakte bleiben unverändert.

Teststatus:339 Repositorytests erfolgreich, vier explizite Skips (drei optionale
Privatgoldtests sowie der neue Publikationscheck im separaten Worktree ohne
Mainmesskopien), zusätzlich fünf historische Analysetests bestanden. Unter den
14 Reviewer-Tests sind13 Softwareprüfungen bestanden; der gespeicherte
Publikationscheck läuft nach Integration mit den tatsächlichen Dateien in CI.
Die tatsächlichen zentralen Mainartefakte wurden zusätzlich ausdrücklich gegen
diesen öffentlichen Prüfpfad geprüft.340 NIGHT- und272 Round3-Archivdateien
unverändert. Alle512 privaten Jobverzeichnisse entsprechen exakt dem Plan;
keine zusätzlichen Verzeichnisse. Gitdiff, Dateigrößen und öffentliche
Artefakte auf private Identitäten, Pfade und Tokens geprüft.

## Zulässige Schlussfolgerung und Abschluss

Der gemeinsame originale Zwei-Feld-Startpaketeingriff verbessert xGD und
tatsächliche Ergebnisse im festen synthetischen Windowskontext. Die Größe
dieses engeren Eingriffs ist als vorregistrierter Transfer-/Replikationspilot
belegt. Pressing und Moderation bleiben unklar; keine Äquivalenz oder optimale
Taktik ist bewiesen. Kein isolierter Consumer, keine UI-Prozentskala, keine
Familiarity-/Mediations- oder Trainingswirkung und keine allgemeine
Karriereübertragung. Kein externer Match wird mit dem anderen Eingriff
gleichgesetzt. Dies autorisiert nur die geprüfte Publikation und den Stopp.
