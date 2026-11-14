# SET-V0 – Offline-Messvertrag und Parsergrundlage

14.11.2026. **Implementierte Offlinevorarbeit, keine native Zählerfreigabe und
keine Leistungsstudie.** Native Starts0, neue Seeds0, Holdout-/Karrierezugriffe0.
[Agentenbericht](../docs/round2/SET.md), [Modul](../research/set_v0.py),
[Tests](../tests/test_set_v0.py), [synthetische Goldfälle](../data/set-v0/gold-cases.json).

## Technische Frage und Annahmekriterium

Kann eine eindeutig definierte, vollständige Ereigniskette ohne Doppelzählung
in legale Standardexposition, Schuss-/Torzuordnung und unmittelbaren Konterpreis
zerlegt werden? Dieser Auftrag prüft ausschließlich Parserlogik an selbst
verfassten synthetischen Fällen. Keine Hypothese über stärkere Standardroutinen,
keine Fallzahl-/Powerbehauptung und keine neuen Matchmessungen.

Offlinegate: alle elf manuell erwarteten Goldfälle und alle negativen
Schema-/Identitäts-/Clock-/Kontakt-/Legalitäts-/Scorefälle müssen bestehen.
Das Bestehen dieses Gates beweist **nicht** die native Herkunft oder Vollständigkeit
irgendeines Ereignistyps. Das native End-to-End-Gate bleibt ausdrücklich offen.

## Harte Herkunftsgrenze

`capability_manifest()` beschreibt den tatsächlich implementierten Adapterstand:
`native_mapping_implemented=false`, `native_validated=false`,
`performance_ready=false`. Native Schema-/Quell-/Clockmapping- und Gatehashes
sind `null`. Diese Felder lassen sich nicht durch einen Aufrufer als Freigabe
an `parse_trace()` übergeben. Ein vermeintliches `validated=true` oder beliebiger
Gatehash in einem nativen Input schaltet nichts frei.

Nur `origin=synthetic`, Schema `SET-V0-synthetic-v1` und Clock
`synthetic_period_milliseconds` werden analysiert. Auch deren Ausgabe behält
`native_validated=false` und `performance_ready=false`. Jedes andere Origin geht
an die blockierte Nativeboundary: Status `unresolved_native_mapping`,
`exposures=null`, `attribution=null`. Auswahlmeldungen bleiben reine Diagnose.
Die Liste fehlender Capabilities bedeutet fehlende SET-End-to-End-Freigabe;
sie verneint nicht die Existenz einzelner Upstream-Tor-/Kartenfunktionen.

Eine zukünftige Nativeversion benötigt eine gesonderte Code-/Schemaversion mit
gehashtem vertrauenswürdigem Source-/Clockmapping und unabhängiger nativer
Goldfallabnahme. V0 implementiert dafür bewusst keinen Freigabeschalter.

## Vollständiger normalisierter Vertrag

Traceheader exakt: `schema`, `origin`, pseudonyme `match_id`, `clock`,
`final_score` und `events`. Jedes Event hat eindeutige pseudonyme `id`, `type`,
`period`1..4 und ganzzahlige nichtnegative `ms` innerhalb der Periode.
Unbekannte Felder/Typen werden abgelehnt. IDs sind eigene kurze Labels, keine
privaten Spieleridentitäten. Periodenzeit ist monoton; Reset erst nach explizitem
`period_end`. `match_end` muss letzter Datensatz sein und das endgültige Torregister
muss dem Headerendstand exakt entsprechen. Kein angenommener nativer Hz-Faktor.

| Ereignis | Zusätzliche Pflichtfelder | Bedeutung |
|---|---|---|
| award |award_id,setpiece_type,side|Neue zugesprochene Ecke/Freistoß/Einwurf. Schließt alte Kette. |
| select |award_id,view_side,routine_sha256|Nur Auswahlansicht. Viele Samples und beide Ansichten erhöhen keine Exposition. |
| execute |award_id,execution_id,contact_verified,legal,repeat_of,reason|Eindeutig nachgewiesener Kontaktversuch mit **final** adjudizierter Legalität. Nur legal zählt. |
| abort |award_id,reason|Expliziter Abbruch ohne Exposition. |
| possession |side,controlled|Nur kontrollierter Besitzwechsel startet/beendet Konter. Berührung allein genügt nicht. |
| shot |shot_id,side,xg,counted_in_final_xg|Ursprüngliches Schuss-xG0..1, keine Verteilung einer Matchsumme. Speichert Kettensnapshot. |
| goal |goal_id,side,shot_id,own_goal|Endgültig adjudizierbares Tor. Reguläres Tor braucht bekannte Schussherkunft; Eigentor darf ohne Schuss auftreten. |
| cancel_goal |goal_id,reason|VAR/Offside-Storno, verhindert endgültige Torzählung; kein automatisches Ändern des finalen Schuss-xG-Status. |
| stoppage / period_end / match_end |keine|Explizite Ketten-/Perioden-/Matchgrenzen. |

Ausführungslegalität wird im normalisierten Enddatensatz endgültig benannt,
auch wenn ein künftiger Mapper dafür spätere Originaladjudikation lesen müsste.
Ein zur Wiederholung bestimmter erster Kontakt hat `legal=false,reason=repeat`;
der erste Kontakt hat `repeat_of=null`. Jeder spätere Kontakt muss via
`repeat_of` exakt die unmittelbar vorherige illegale Ausführung **desselben**
Awards benennen. Fehlende, übersprungene, künftige, awardfremde oder bereits
legale Vorgänger sind Fehler. Final legale
Ausführung schließt den Award. Offene Awards am Perioden-/Matchende sind Fehler,
nicht automatisch Null. Nicht belegte Ballkontakte werden abgelehnt.

Physische Kontakte brauchen eindeutige `execution_id`. Doppelte Event-/Kontakt-
IDs, erneute legale Ausführung desselben geschlossenen Awards und widersprüchliche
Ansichten scheitern geschlossen. Ein künftiges Rawmapping muss die physische
Identität gegenüber zwei Kamera-/Teamansichten nachweisen; V0 errät keine
Deduplikation aus Tick oder Routinehash. Dieselbe Routine in zwei verschiedenen
Awards kann dagegen zwei legale Expositionen ergeben.

## Ketten und Zähler

Nach legalem Kontakt läuft die Angriffskette bis Unterbrechung, neuem Standard,
Periodenende oder kontrolliertem gegnerischem Besitz. Letzteres startet die
Konterkette mit Fenster **[Besitzwechsel, Besitzwechsel+10.000ms)**. Wiedererlangter
kontrollierter Originalteambesitz, nächste Unterbrechung/Standard/Periodengrenze
oder die10s-Grenze beendet sie. Genau an10s ist ein neuer Schuss nicht mehr
zugeordnet. Keine nachträgliche Wahl zwischen Fenstern.

Schuss-xG und Torattribution verwenden den Schuss-Snapshot. Eine spätere
Torregister-/VAR-Nachricht wird so nicht versehentlich dem nächsten Standard
zugeordnet. Die separate Pflichtangabe `counted_in_final_xg` bestimmt, ob das native finale
Schuss-xG in die Summen eingeht. Eine Torstornierung allein setzt diesen Status
nicht: der Goldsatz enthält sowohl ein VAR-storniertes Tor mit weiterhin gültigem
Schuss-xG als auch einen final nicht gezählten Offside-Schuss. Fehlender Status
wird abgelehnt. Eigentore ohne Schuss erhalten kein erfundenes xG. Nicht zuordenbare
Open-Play-Schüsse/-Tore behalten `context=null`; endgültiger Endstand bleibt dennoch
vollständig geprüft. Ein widersprüchlicher Schussbesitzer wird nicht geraten.

Ausgabe je Typ und angreifender Seite: legale `executed`, xG/Tore für/gegen und
Konter-xG/-Tore gegen den Ursprung. `defended`, defensive xGA/Gegentore werden aus
den gegenüberliegenden Angriffen abgeleitet. Kein doppelter Offensiv-/Defensiv-
Nenner. `net_xg=xg_for−xg_against` bleibt ein synthetischer Parserwert.
Keine Raten, Kandidatenrangfolge, p-Werte oder Wirksamkeitsintervalle in V0.

## Reale vorhandene Belege und Grenzen

Geprüft nur zwei bekannte VALID-002-Logs:112/122Zeilen, jeweils52
`native_setpiece_selected`-Meldungen an26Ticks, derselbe Seed/0:0-Kontext.
Ausführung, vollständige Clock-/Schuss-xG-/Besitzketten sind dadurch nicht belegt.
[Vollständige zulässige Hash-/Gapdiagnostik](../data/set-v0/native-source-gap.json).
Keine Rohlogs/Spieler-IDs/PKM wurden kopiert oder veröffentlicht.

Aktueller lesender Versionsbeleg: FM27 File27.0.1/Product27.0.1+2503222,
Engine-SHA2568c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340.
Quellcommit91f2eba57fac0b7fbd3dff616056907e3ce461be/v1114.6.
Das ist kein neuer nativer Kompatibilitäts- oder Reproducible-Build-Test.

## Nächstes natives Gate – nicht gestartet

VALID-003D muss echten Ausführungskontakt/finale Legalität, Periodenclock,
kontrollierten Besitz, ursprüngliche Schuss-xG und endgültigen Tor-/VAR-Status
passiv und vollständig erfassen. Gegen unabhängige Quelle/Annotation prüfen:
Abbruch, Wiederholung, doppelte Ansichten, kurze Ecke mit zweitem Pass,
Standardtor/VAR/Eigentor, Übergang in Konter, Rückeroberung und Periodengrenze.
Fehlende positive Ereignisklassen bleiben blockiert. Erst danach neuer
registrierter Nativeadapter; Performanceversuche benötigen zusätzlich eigenen
Seed-/Budget-/Analysevertrag. Kein Eintrag im alten SET-001 wird umgeschrieben.
