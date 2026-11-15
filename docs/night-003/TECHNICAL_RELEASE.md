# N3-SHARPSTRUCT-C1: technische Freigabe und Änderung vor Main

15.11.2026,08:11:48UTC. **32/32 vollständige Technikmatches**,16/16 exakte
A/A-Paare und eine erwartete Exit108-Abweisung bestanden.33/33Jobs, keine
Ausfälle, keine Retries oder Ersatzseeds. Höchstens4 gleichzeitig zugelassene
kalte Calls, je ursprüngliches Job3-Containment; alle Bereinigungen bestätigt,
keine Pendingmarker oder NativeLease verblieben.27,681s beaufsichtigte Phase.

Alle16 Kontext×Seite×Arm-Zellen bestanden die vollständigen nativen Eingabe-,
Actor-, Rollen-/Positions-, Attribut-/Profil-, Startcache- und Kontrollgates.
OOP und Pressing unverändert, Schärfe auf beiden ursprünglichen Feldern im
richtigen Spielerumfang vorhanden. Alle Rohlogs und Inputdumps wurden nach
Phasenabschluss erneut gehasht, eingelesen und gegen den Export geprüft.
Diese zweite Prüfung erfolgte durch einen separaten Durchlauf desselben
Analysten/Prüfcodes; keine unabhängige Person behauptet.

Vorregistrierung `ac5b993330b49734d49088045ea55fd6a6a3385d`,
[erfolgreiche CI43693138863](https://github.com/Matchekk/FM-27-Research/actions/runs/43693138863).
[Messungen](../../data/night-003-sharpstruct/technical.jsonl) ·
[Summary](../../data/night-003-sharpstruct/technical-summary.json) ·
[Gate](../../data/night-003-sharpstruct/technical-release.json).

## Explizite Vor-Main-Änderung: Ausführungsreihenfolge

Beim zweiten Code-/Ablaufabgleich wurde erkannt: `jobs()` mischt zwar die
Planliste, aber der wiederverwendete `block_jobs()` sortiert vor Dispatch die
vollständigen Kontext-Seedblöcke lexikografisch erneut. Main wird deshalb
**in der tatsächlichen sortierten Blockreihenfolge** durchgeführt. Diese
Änderung wird vor dem ersten wissenschaftlichen Match veröffentlicht.

Keine wissenschaftlichen Daten wurden zur Entscheidung angesehen: bislang
ausschließlich Technikseeds. Keine Änderung an primärem Kontrast, Endpunkten,
Fallzahl, Seeds, Seitenpaarung, Armzuordnung, Inputs oder Analyse. Alle8Calls
eines unabhängigen Blocks bleiben zusammen. Die tatsächliche Reihenfolge ist
aus Dispatch-/Concurrencyledger rekonstruierbar. Der deterministische kalte
Host, gesperrte Ressourcen und Readbacks begrenzen mögliche Drift; ein
unbekannter zeitlicher Drift ist dadurch nicht mathematisch ausgeschlossen.
Keine nachträgliche Behauptung einer randomisierten Dispatchreihenfolge.

Die Änderung benötigt keinen neuen nativen Eingriff oder weiteren Techniklauf.
Alte eingefrorene Dateien/Hashes und ursprüngliche Planliste bleiben erhalten;
dieses Dokument hat für die Reihenfolgebeschreibung Vorrang.

## Mainfreigabe

4096neueMatches/512Blöcke, unveränderte Vorregistrierung mit obiger Änderung.
Technische Zustandswerte sind keine Leistungsbefunde. Quellen-/Patchstand wird
vor Main erneut geprüft. Erst vollständige Serie plus eingefrorene Analyse und
separate skalare Nachrechnung erlaubt einen Forschungsbefund.
