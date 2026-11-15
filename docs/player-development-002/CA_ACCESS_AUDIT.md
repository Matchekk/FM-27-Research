# CA-002: technischer Zugang und Quellenprüfung

15.11.2026. Ergebnis des begrenzten Zugangschecks: **eine ausführbare externe
RCA-Rekonstruktion gefunden; keine lokal validierte native CA-Kostenfunktion**.
`MODEL_RCA` bezeichnet Berechnungen dieses externen Modells. Der Status behauptet
weder echten CA-Verbrauch noch einen unabhängig abgenommenen FM27-Editorreadback.

## Neuer belastbar referenzierbarer Messweg

[FM27 Scout](https://github.com/shlk20/fm27-scout-code/tree/084d7f0a18ac790d7c4087c5b6bdff008186d4fa)
stellt einen vollständigen Rechner bereit. Die
[TypeScript-Funktion `estimateCaExact`](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/apps/desktop/src/lib/ca.ts)
akzeptiert rohe Attribute auf 1–100, beide Fußwerte auf 0–100, alle 15
Positionsratings auf 0–20 und optional die auszuwertende Position. Rückgabe:
ganzzahlige Modell-RCA, gewählte Position, gewichtetes Mittel, Positionskosten
und Iterationsdiagnostik. Ein reiner Offlineaufruf braucht keine Spielinstallation,
keinen Save und keine Mutation eines Spielers. Node v25.9.0 ist hier vorhanden;
die einzige Einfuhr der Datei ist eine entfernbare Typeinfuhr.

Der [Rust-Rechner](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/crates/fm27-core/src/ability.rs)
ist eine zweite Implementierung derselben Quellenfamilie. Das ist geeignet zur
Implementierungskontrolle, jedoch keine unabhängige Enginevalidierung.
MIT-Lizenz vorhanden; nur einzelne Quelldateien im ignorierten lokalen Cache,
kein fremdes Repository oder geschütztes Spielmaterial im Forschungsarchiv.

Der vollständige Algorithmus berücksichtigt die Attributverteilung, Füße,
Positionenkombination und Positionsvertrautheit. Er ist deshalb ein neuer
konkreter Messkandidat gegenüber der bisherigen linearen Gewichtstabelle.
Sein Rundungs- und Iterationsverfahren muss unverändert ausgeführt werden;
eine einzelne Gewichtszelle ist weiterhin kein Preis in CA-Punkten.
**Ein Modell-Delta von null kann durch Ganzzahlrundung entstehen.** Es belegt
keinen kostenlosen Attributpunkt im Spiel.

## Ursprung und verbleibende Verifikationslücke

Der [Originalbericht von ChoreaW](https://www.playgm.cc/thread-986285-1-1.html)
vom 04.11.2026 beschreibt zunächst das Reverse Engineering des FM26-Pregame-
Editors. Im Schlussabschnitt berichtet der Autor anschließend eine Übertragung
auf FM27 mit Speicherreadbacks von 200 Einpositions- und 500 Mehrpositions-
Spielern ohne Abweichung. Exakter FM27-Build, vollständige Profilzeilen,
Goldreadbacks und Trennung von gespeichertem CA gegenüber RCA fehlen im
zugänglichen Bericht. Der Transferclaim ist daher **extern berichtet**, keine
eigene Bestätigung. Die Einordnung allein als FM26-Quelle wäre ebenfalls falsch.

FM27 Scout berichtet über 48.000 Saveprofile, MAE 0,8 und alle Fehler innerhalb
fünf Punkten. Entscheidend: Der
[reale Savetest](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/crates/fm27-core/tests/ability_real_save.rs)
vergleicht berechnete RCA ausdrücklich mit **gespeichertem CA**. Er prüft keinen
Editor-RCA-Goldstandard und ist ohne privaten Referenzsave übersprungen.
Weder dessen Fehlerangaben noch Quelltextformulierungen wie „Exact“ beseitigen
unsere Messlücke. Die tatsächliche lokale Genauigkeit ist unbekannt.

## Andere geprüfte Wege

| Weg | Beobachteter Zugang | Entscheidung |
|---|---|---|
| Installierter Tactics-Lab-Host v1114.6 | `current_ability` ist ein separat gesetztes Profilfeld; in den untersuchten Python-/Hostdateien kein RCA-Rechner gefunden | Kein Kostenorakel; unverändertes CA nach Attributänderung nicht auswerten |
| fmsave | Leser für gespeichertes CA/PA/Attribute | Kein unabhängiger Attribut→CA-Rechner |
| Talent Seer | Aktueller Autorenbeitrag nennt Version 27.1.3 und live aktualisierte Recommended CA | Kein lokal abgenommener Headless-Messweg; geschlossene Implementierung |
| FMAX | Aktuelle FAQ beschreibt Unterstützung für 27.0.1+2503222 und Berechnung nach Spielregel | Kein zugänglicher Rechnerquelltext im öffentlichen Release-Repository; kein unabhängiger Beleg der Semantik |

Beim [Talent-Seer-Autor](https://sortitoutsi.net/content/78140/talent-seer-is-here-a-free-scouting-and-editing-tool-for-football-manager-27)
steht am 05.11. ausdrücklich, dass RCA berechnet und nicht einfach als
gespeicherter Speicherwert gelesen werde; für die Rekonstruktion wolle er FM26
verwenden. Eine spätere Funktionsankündigung ersetzt keine Überprüfung des
FM27-Transfers. Die [FMAX-FAQ](https://hexase1-ship-it.github.io/fmle/en/faq.html)
war über den Webindex lesbar; beim direkten HTTP-Abruf kam nur eine Weiterleitung
auf eine anschließend nicht erreichbare Seite. Dies ist ein dokumentierter
Zugriffsunterschied, kein Beweis einer fehlenden Funktion.

## Neue externe Karrierebelege, keine eigene Replikation

Der neue
[Editorversuch](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/docs/editor-test-plan.md)
enthält vier vom Autor fortgeschriebene Ableger desselben jungen Stürmers auf
FM27 **27.0.0+2486695**, 25.07.–27.08.2026. Gemeldet werden Rückanpassungen
von Attributen nach getrennten CA- und Attributedits. Es ist **ein Karrierecluster,
ein Spieler**, keine Studie unabhängiger Karrieren und kein Trainingsplanvergleich.
Die zugänglichen Ergebniszusammenfassungen liefern keine Seeds, Unsicherheits-
schätzung, vollständigen Kontrollreadbacks oder öffentlich ausführbaren Rohsaves.
Sie stützen einen konkreten Replikationskandidaten: gespeichertes CA und die
Attribute können zeitweilig auseinanderliegen und sich anschließend verändern.
Sie identifizieren keine marginalen Attributkosten und keine Wachstumsgarantie.

## Neuheitsentscheidung und Reproduzierbarkeit

Atlas, Index und FINDINGS sowie PD-CA-001 geprüft. Überlappung: MAC-20,
PD-EXT-SCOUT-CA und die fm-scoring-Tabelle. Neue IDs: `SHLK20-SCOUT-RCA`,
`PLAYGM-RCA-20261104`, `SHLK20-EDITOR-ABC`. Entscheidung für den Kostenclaim:
**UNCERTAIN_SOURCE**. Die vollständige externe Funktion ist ein neuer
prüfbarer Modellgegenstand; die bisherigen 109 GK-Exportzeilen werden nicht
als neue unabhängige Stichprobe wiederholt.

[Abrufprovenienz und SHA256](ca-access-source-audit.json) binden alle neun
gepinnten Quell-/Dokumentdateien und dynamische Webseiten. Vollständige Kopien
liegen ausschließlich im ignorierten `local/`-Cache. Keine native Simulation,
Karrierefortschreibung oder Profilmutation wurde für dieses Audit ausgeführt.
