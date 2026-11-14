# SET-N2-03: konkreter Export- und Identifizierbarkeitsblocker

**Ergebnis:** Der unveränderte vorhandene Observerhost liefert keinen
freigabefähigen End-to-End-Datensatz für Netto-xG je tatsächlich ausgeführter
Ecke. Auswahl, Tore/Karten und aggregierte Statistik sind teilweise vorhanden;
Ausführungskontakt/finale Wiederholungsentscheidung, einzelnes ursprüngliches
Schuss-xG mit finalem Zählstatus und kontrollierte Besitzketten fehlen als
implementierte und nativ validierte Verknüpfung. Deshalb **kein zusätzlicher
Technik- oder Wirksamkeitslauf** aus diesem Audit.

Nur Quellen und drei bereits vorhandene private Logs wurden gelesen; keine
Host-/Engineprozesse, Builds, Seeds, Saves, UI- oder Kalenderaktionen. Die
Originalressourcen und Rohlogs wurden nicht kopiert oder veröffentlicht.
Die [SET-V0-Synthetik](../../experiments/SET-V0-measurement.md) bleibt unverändert.

## Exakt geprüfte Identität

Der vorhandene passive Host hat tatsächlich SHA256
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`.
Seine private modifizierte Hostquelle hat
`e1edbec9d45cdfccfbb719a5fe031d1cf86c81a77a644502374dfeee74c61450`.
Die folgenden tatsächlich gelesenen unveränderten Header passen zu den
ursprünglichen Buildmanifest-Hashes des auf `91f2eba57fac0b7fbd3dff616056907e3ce461be`
/v1114.6 basierenden Hosts:

| Quelle | SHA256 |
| --- | --- |
| `native_setpiece_episode.h` | `311e04ee09de7a08a140908a3918e1344c3259db68dc7cde4be41657c204e49b` |
| `native_match_events.h` | `197cb8c5c8dce17a543eb5886eb15bca9e497a8cec485e9bb1588f56f345f462` |
| `native_statistics.h` | `06e38230ef488dbeab91a245974b7bcaf7f8e4c49a14ce6482498451421dae60` |

Der genaue FM27-Pflichtkontext bleibt27.0.1+2503222 mit Enginehash
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Dieses lesende Audit ist keine neue native Kompatibilitätsabnahme.

## Was tatsächlich exportiert wird

| Funktion / Datensatz | Vorhandene Felder und Logik | Exakte Grenze für SET |
| --- | --- | --- |
| Hostsimulationsschleife, `native_setpiece_selected` | `side,deadball,type,variant,frequency,strategy,swing,tick`; Auswahlkey pro Teamansicht aus Deadball/Typ/Variante, Ausgabe nur bei Keywechsel | Typ5 ist offensive Ecke, Typ0 defensive Ansicht. Eine reale Situation kann beide Ansichten und mehrere Auswahlzustände liefern. Kein Award-/Kontakt-/Execution-ID, keine finale Legalität oder `repeat_of`; kein Clock-/Periodenfeld in dieser Meldung. |
| `desktop_capture_event_queue()` | Beobachtet Queuepakete vor Leerung; dekodiert Kind32 als `native_goal_event`,26/29 als `native_card_event`. Optional `desktop_event_packet` mit `kind,tick,clock,period,hex` für20 rohe Bytes | Nur Goal/Card semantisch dekodiert. Zusätzliche Rohpaketinhalte sind ungeklärt; ihre Existenz beweist keinen vollständigen Kontakt-/Schuss-/Besitzexport. Der Goal/Card-Deduplikationshash enthält Tick und relevante Paketbytes, keine validierte physische Corner-Execution-ID. |
| `desktop_final_incidents()` | `native_final_incident_registry`, mit nativer Art/Seite/Akteur, nomineller Minute, Nachspielminute, nativem Tick und rohen40Bytes | Der vorhandene Pythoncollector verwendet Arten1/2/3 für Tore sowie14/15/38 für Karten. Keine implementierte Shot-ID/xG- oder Corner-Verknüpfung. Andere Arten werden dort nicht als solche Ereignisse validiert. |
| `desktop_player_totals()` und `fm27_match_events.collect()` | Finales Tor-/Kartenregister gegen Akteursstatistik und Endstand; Queue-Collector berücksichtigt Scorezuwächse und spätere Rücknahmen | Wertvolle Tor-/Kartenintegrität. Eine Score-Rücknahme identifiziert aber weder den ursprünglichen Shot-xG-Datensatz noch dessen finalen xG-Zählstatus oder die vorausgehende Ecke. Kein nativer VAR-/Retake-Goldnachweis in den drei hier geprüften Logs. |
| `desktop_match_statistics()` | Finale Teamwerte `xg,shots,shots_on_target,passes,completed_passes,possession_ticks,possession` | Matchsummen, keine Liste einzelner Schüsse und keine zeitliche Reihenfolge kontrollierter Besitzer. Finales xG lässt sich nicht rechtmäßig auf Standardsituationen aufteilen. |
| `desktop_stats_snapshot()` | Bei aktivem Audit vorbereitete/finale Team-/Spielerstatistikbytes | Zwei Endpunkte sind keine vollständige Schuss-/Besitzzeitreihe. Rohbytes bleiben ohne Feld-/Writer-/Clockmapping uninterpretierte Belege. |
| CLI `wmain()` | Fixture, Seed, Output, Scenario, Inputdump und Tickstep1..256; keine deklarative Cornerkontakt-/Shot-/Possession-Exportoption | Tickstep1 erhöht Abtastung, fügt aber keine fehlenden strukturierten Ereignisklassen hinzu. |

Originale öffentliche Referenzen desselben Quellstands:
[Host](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/desktop_host.cpp),
[Eventheader](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_match_events.h),
[Episodenheader](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_setpiece_episode.h),
[Python-Goal/Card-Collector](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_match_events.py).
Diese Referenzen ersetzen nicht die oben gehashte tatsächliche private
Observerhostquelle; deren eigener Zusatz bleibt auf die passiven Zustandsaufnahmen begrenzt.

## Warum der vorhandene Episodenmodus die Lücke nicht schließt

`desktop_episode_init()` wird über `FM27_EPISODE_TYPE` aktiviert, akzeptiert
Typ5..9, Seite0/1 und ein Fenster5..120 Sekunden; Standard ist Typ5/Seite0/30s.
`desktop_episode_step()` startet, wenn der beobachtete Deadball-Typ und die
taking-Teamreferenz passen. Als `delivery_tick` gilt bereits der erste Wechsel
des Typs oder des taking-Teams. Das ist **kein nachgewiesener Ballkontakt**;
Abbruch, Wiederholung oder anderer Zustandswechsel sind nicht separat adjudiziert.

Das Statistikfenster wird anhand `clock−delivery_clock ≥ seconds×4` geschlossen.
Ein kontrollierter Ballbesitzwechsel, Rückeroberung, neuer Standard oder eine
10s-Kontergrenze wird dort nicht als Attribution abgebildet. Der Faktor4 ist
eine Annahme dieses Codes, keine hier unabhängig kalibrierte Periodenclock.

Zusätzlich unterscheiden sich die Zeitbereiche der ausgegebenen Ergebnisse:
`window_stats` wird beim Fensterschluss gespeichert, beendet wird erst nach
weiteren240 Clockeinheiten. `desktop_episode_finish()` berechnet Tore aus dem
dann aktuellen Score minus Startscore, xG/Schüsse dagegen aus den zuvor
gespeicherten Fensterstatistiken. Bei der Codeannahme4Einheiten/s ist der
Torebereich60s länger als der xG-Bereich. Spätere Tore sind dadurch nicht
automatisch dem ursprünglichen Standard oder dem xG-Fenster zuzuordnen.

Der Modus endet via `desktop_finish_and_exit()` mit
`native_setpiece_episode_finished.full_match_completed=false`. Selbst ein
`valid=true` in diesem Record bedeutet nur, dass sein Fenster/Settlement
abgelaufen ist; es ist keine SET-Kontakt-/Kettenvalidierung und kein Vollmatch.
Eine Gleichsetzung mit `natural_match_finished` wäre falsch.

## Konkreter Hardware-Hook-Konflikt

Ein naheliegender Versuch, fehlendes Schuss-xG über
`FM27_DESKTOP_STATS_AUDIT` nachzuliefern, funktioniert im bestehenden Host nicht
als vollständiger paralleler Eventexport:

1. `desktop_stats_snapshot(match,"prepared")` richtet per
   `desktop_watch_setup()` vier Datenwatchpoints in DR0..DR3 ein; DR7 aktiviert
   die Slots. Diese Funktion läuft **vor** `desktop_events_start()`.
2. `desktop_event_setup_thread()` setzt seine drei Eventqueue-Breakpoints nur,
   wenn `!(Dr7&255)` gilt. Bereits belegte Statistikslots verhindern die Installation;
   `desktop_events_start()` liefert dann keinen installierten Observer und der
   Host bricht mit181 ab. Dies ist aus Quellreihenfolge/-bedingungen abgeleitet,
   kein hier neu provozierter nativer Fehler.
3. Selbst getrennt wäre `desktop_stats_exception()` kein vollständiger Shotstream:
   Er beobachtet nur die Statistikreferenz von Seite0 und dedupliziert pro
   Writer-RVA/Feld, maximal128Einträge. Ein wiederholter Schuss desselben Writers
   liefert so keinen eigenen Datensatz. Das gelegentliche `record_value` am
   xG-Writer ist keine vollständige, identifizierte Shotliste mit Finalstatus.

`FM27_DESKTOP_EVENTS_AUDIT` allein könnte vorhandene rohe20Byte-Pakete ausgeben,
ohne neuen Host. Es fehlt jedoch deren validiertes Kontakt-/Shot-/Besitzschema;
kein entsprechender Auditpacket-Stream liegt in den drei unten geprüften Logs.
Die Umgebungsflags werden nach **Vorhandensein**, nicht nach boolescher
Textinterpretation geprüft: beispielsweise würde vorhandenes
`FM27_SKIP_EVENT_DETAILS=0` die Details trotzdem abschalten. Ein neuer Vertrag
müsste widersprüchliche Flags ausdrücklich ausschließen. Das Aktivieren eines
Flags allein ist keine native SET-Freigabe.

## Tatsächlich vorhandene Logbelege

Die beiden alten VALID-002-Logs wurden erneut vollständig gelesen und gegen
die bereits veröffentlichten [SET-V0-Hashes](../../data/set-v0/native-source-gap.json)
geprüft. Ein vorhandener VALID-005-Observerlauf ergänzt einen echten Torfall.
Nur zulässige Zählungen/Hashes werden hier publiziert; keine Akteursidentitäten.

| Privates Artefaktlabel | SHA256 | Befund |
| --- | --- | --- |
| `full-events/home_baseline-2362620850-r0.jsonl` | `bd16b50548b28afc71c61d2a32472995b1fc2204ef46f304a8f9bd630d759cd7` |112Zeilen,52Auswahlmeldungen an26Ticks;15offensive Typ5- und15defensive Typ0-Meldungen.0Auditpackets,0Goal-/Scoreänderungsmeldungen; finales0:0, gültiges Finalregister vorhanden,22714Queuebeobachtungen. |
| `full-events/home_baseline-2362620850-r1.jsonl` | `5f4860ee770addac04333a4fa2c5eec42c48468aa7300f01c9e28b131ea066e6` |122Zeilen, dieselben52Meldungen/26Ticks und15+15Corneransichten;0Auditpackets, finales0:0,22714Queuebeobachtungen. Derselbe Seedkontext, kein unabhängiger Cornernachweis. |
| `VALID005/high_press-0-observer_on.jsonl` | `2ed8d8bbb392c36dff5d10a975abb00e05e36602f6967310c87c759fdcda8269` |189Zeilen,62Auswahlmeldungen an31Ticks;14offensive/14defensive Corneransichten.0Auditpackets,1Goal-/1Scoreänderungsmeldung, finales0:1; gültiges Finalregister mit11Incidents,23649Queuebeobachtungen. |

Im dritten Log stehen echte Matchsummen von7/11Schüssen, xG0,412376285/1,43779039,
Endtick23583 und Endclock22584. Trotz vorhandener Schüsse, Tor und
funktionierendem Queueobserver enthält sein strukturierter Export keine
Einzelschuss-xG-/Execution-/kontrollierten Besitzrecords. Die14offensiven
Cornerauswahlen werden deshalb **nicht** als14ausgeführte Ecken gezählt.
Aus den drei Logs wird weder eine Expositionsrate noch ein Effizienzbefund berechnet.

## Bestehender Parser und kleinste notwendige Reparatur

[`research/set_v0.py`](../../research/set_v0.py) verlangt bereits die richtigen
getrennten Belege: `execute.contact_verified/legal/repeat_of`, periodenkalibrierte
Clock, `shot.xg/counted_in_final_xg`, kontrollierten Besitz und endgültige
Tor-/Stornoreferenzen. Native Inputs bleiben `unresolved_native_mapping`,
`exposures=null`, `attribution=null`, `performance_ready=false`.
Alle11 vorhandenen SET-Testmethoden einschließlich der elf synthetischen
Goldfälle bestehen erneut. Das belegt Parserlogik, keine native Vollständigkeit.

Die engsten Reparaturen, in dieser Reihenfolge:

1. **Tatsächlichen Eckkontakt und finale Retake-/Abbruchentscheidung exportieren.**
   Ein gehashter Originalquellenpfad muss Award, physischen Kontaktversuch,
   finale Legalität und unmittelbar vorherigen illegalen Kontakt desselben
   Awards eindeutig binden. Zwei Teamansichten oder ein Deadball-Keywechsel
   dürfen keine zusätzlichen Expositionen erzeugen. Erst dieser Export erlaubt
   einen nachprüfbaren Nenner. Die jetzigen optionalen Queue-Rohbytes sind
   dafür eine mögliche Untersuchungsquelle, noch kein implementiertes Mapping.
2. **Schuss-xG/Finaltor und kontrollierte Besitzkette an diesen Nenner binden.**
   Ursprüngliche Shot-ID/xG und finaler xG-Zählstatus getrennt erfassen; Tor-/VAR-
   Register auf Shot/Execution zurückführen, Eigentore gesondert erhalten.
   Dazu tatsächliche kontrollierte Besitzerwechsel, Unterbrechungen und
   periodenkalibrierte10s-Zeitgrenze exportieren. Finale Teamstatistiken und
   bloße taktische IP/OOP-Phasenwechsel ersetzen diese Kette nicht.
3. **Echte positive und negative Goldfälle unabhängig validieren.**
   Reguläre/kurze Ecke, Retake/Abbruch, doppelte Ansicht, Shot/VAR mit getrenntem
   xG-Status, Gegenkonter/Rückeroberung und Periodenende müssen gegen eine
   unabhängige Originalquelle abgeglichen werden. Noch nicht aufgetretene
   Ereignisklassen bleiben offen; keine zusätzlichen Seeds erzwingen, bis
   ein seltener Fall zufällig erscheint. Danach erst neuer Messadapter und
   ein separat vorregistrierter technischer Vertrag.

Ein kleiner End-to-End-Reader ohne diese neuen belegten Quell-/Exportbindungen
ist derzeit nicht nachgewiesen. Ein weiterer unveränderter Hostlauf würde die
fehlenden strukturierten Capabilities nicht freischalten. Daher werden hier
weder ein≤8-Match-Lauf noch eine Wirksamkeitsserie vorregistriert. Der konkrete
Fortschritt dieses Audits ist die Eingrenzung auf Kontakt-/Legalitätsquelle,
Shot-/Besitzbindung und die beiden vorhandenen, für SET ungeeigneten Alternativen
Episodenfenster beziehungsweise deduplizierter Statistikwatchpoint.
