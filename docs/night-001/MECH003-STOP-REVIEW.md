# MECH-003 – unabhängiger Review des administrativen Mainstopps

14.11.2026. **Technik abgeschlossen und bestanden; Main nicht gestartet.**
0wissenschaftliche Matches,0beobachtete Mainseedblöcke, kein Wirkungsschätzer.
Der bedingte Mainentscheid aus dem technischen Review wurde vor Ablauf seines
Startcutoffs nicht vollständig freigabefähig: Veröffentlichung und exakte CI
fehlten. Der abgeschlossene Technikbefund bleibt davon unberührt.

## Budgetänderung exakt rekonstruiert

Private und öffentliche Stopreceipts sind identisch. Tatsächlichen privaten
Budget-Rawhash nach dem Stopp geprüft. Anschließend ausschließlich die zwei
neuen administrativen Felder entfernt und `halted` auffalse zurückgesetzt:
Die wiederhergestellte JSONserialisierung besitzt exakt den zuvor protokollierten
Rawhash. Damit sind die drei erklärten Änderungen vollständig gebunden:

- `halted`: false→true;
- neues `administrative_stop`;
- neues `administrative_stop_utc`.

| Privater Budgetzustand | SHA256 |
| --- | --- |
| vorher | `33058f4563ad2547d28986f3eec263eec1a5f8dfa2eb1e86c584e17793cd6d9b` |
| nachher | `880808300fd0027764d326e5aa2759d22ee8c73bfe8776593aa6e57a3df46181` |

Beide abgeschlossenen Operationen `prepare`/`technical`, sämtliche36bisherigen
Reservierungen,37,3480609verbrauchte Sekunden, Limits600s/1200s/36technical/
514main, Startzeit und Deadline sind exakt unverändert. Keine aktive Phase,
Zeitgutschrift, Counteränderung, Refund, Ersatzseeds oder Fristverlängerung.
Der Nachtmaster ist nicht angehalten und unverändert bei101,2047395/1800s;
keine MECH-003-Mainoperation oder Mainreservierung darin vorhanden.

## Main blieb vollständig unbegonnen

Alle550Abrechnungsplätze geprüft:35technische`ok`, eine erwartete Abweisung und
**514Mainplätze `not_started` und nicht reserviert**. Davon512Match- und zwei
Loader-/Capabilityplätze. Öffentliches `main.jsonl` ist leer, `effects.json`
existiert nicht. Kein privater Mainrunordner, keine Mainstdout- oder Mainlease-
Datei und keine Mainbudgetoperation. Keine globale NativeLease/Cleanupmarker
verblieben. Kein Hinweis auf einen versteckten Mainstart dieses Supervisors.
Die64Mainseeds bleiben im ursprünglichen Seedreceipt reserviert und unbenutzt;
sie werden nicht als beobachtete Stichprobe gezählt oder neu vergeben.

Die administrative Ressourcenprojektion wurde unabhängig nachgerechnet:
`ceil(16 × max(vier tatsächliche8Match-Sessionzeiten) +15s) =282s`.
Unverändertes Studienende19:30:38,762040UTC ergibt späteste Zulassung
19:25:56,762040UTC. Das ist eine nach der Technik erstellte Ressourcenentscheidung,
keine vorregistrierte Leistungsanalyse oder nachträgliche Effektauswahl.
Auch der vorher gesetzte späteste Start20:26:05CET war nicht vollständig gegated.
Der Stoppreceipt vom19:27:26,093741UTC dokumentiert deshalb keinen neuen Lauf.

Diese Studie bleibt dauerhaft vor Main geschlossen. Keine Wiederaufnahme,
neues Budget oder bloße Umetikettierung derselben Serie zur Umgehung der Frist.
Technische Eingabefreigabe ist kein Stamina-/Pressing-Leistungsergebnis und
kein Kausal-, UI-, Setter- oder Karrierebefund. Spätere andere technische Fragen
brauchen ihre eigenen Verträge und Gates unter dem unveränderten Nachtmaster.
Reviewer:0Hosts,0Matches,0Seeds,0Savezugriffe.
