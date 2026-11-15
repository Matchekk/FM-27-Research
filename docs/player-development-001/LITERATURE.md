# Quellen-, Patch- und Neuheitsprüfung · 15.11.2026

Atlas, alle35 Indexeinträge und eigene FINDINGS auf Basis3cd4317 geprüft.
Aktuelle Remotecommits per GitHub-API: Fm-Match-Lab9bc29019,
Tactics Lab cdda4be7, fmsave f4f70f62, fm-scoring b5928ba2.
Das installierte Lab wird nicht ungeprüft aktualisiert. Aktuelle DLL ist
27.0.1+2503222 mit unverändertem geprüftem Hash; offizieller
[Updateindex](https://community.sports-interactive.com/forums/forum/905-fm27-updates)
zeigt beim Abruf Launchhinweise9.11. und Minor Update2.11.; kein Anspruch,
dass ein Forumindex allein alle möglichen Plattformupdates beweist.

## Abgleich vor Hypothese und Seedreservierung

| Frage | Nutzerklasse / Archivklasse | Quellen und zusätzliche Information |
|---|---|---|
| allgemeine Bedeutung Tempo/JR, CA allein | ALREADY_ESTABLISHED / DUPLICATE_STOP | MAC-12/13B/20, Purity, ATTR-Reihe; keine neuen Läufe |
| CF/DLF × JR desselben ST | NOVEL_HYPOTHESIS / NOVEL_HYPOTHESIS | MAC-13B, FM27-PURITY-POS, TACT-002-R0, ATTR-006/007/009; neuer faktorieller Interaktionskontrast bei konstantem OOP und Spieler |
| tatsächliche CA-Grenzkosten | METHODOLOGY_BLOCKED / UNCERTAIN_SOURCE | neue öffentliche fm-scoring-Tabelle; Tabelle allein ist keine identifizierte marginale Kostenfunktion |
| PA-/Trainingseffekt | METHODOLOGY_BLOCKED / UNCERTAIN_SOURCE | TRAIN-001/002 und fmsave-API; keine validierte Teilnahme/RNG oder Langzeit-Holdouts |

**Heutige wichtige Quellenänderung:**
[MAC-13B](https://github.com/caiograco289/Fm-Match-Lab/blob/9bc29019adc87cf45138c462e96c4e19077a0381/docs/studies/13b-value-by-position-random.md)
enthält jetzt neben50.000 Gegenpress- auch34.340 berichtete Catenaccio-Matches
(vorzeitig beendet, laut Autor fortsetzbar). Der alte Atlas bleibt historisch
unverändert. Es handelt sich um dieselbe Autorenfamilie und nicht um eine neue
unabhängige Replikation. Die Studie variiert Attribute randomisiert nach
Positionsgruppen und Spielstil, isoliert aber keinen CF/DLF×JR-Kontrast.
[Purity](https://fm-arena.com/threads/attribute-importance-by-position-in-fm27-a-test-on-my-own-tactic.125/)
untersucht eine feste3-4-2-1-Taktik; gleiche Frage nicht identifiziert.
TACT-002-R0 variiert ST-/AMC-Rollen bei gleichen Attributen, ATTR-009
Positionsmasken×relative Attribute bei fixer Rolle. Beides beantwortet die
neue Interaktion nicht. Eigene N3-Schärfestudien sind abgeschlossen und
werden weder verlängert noch neu benannt.

[MAC-20](https://github.com/caiograco289/Fm-Match-Lab/blob/9bc29019adc87cf45138c462e96c4e19077a0381/docs/studies/20-current-ability.md)
ist ein Test nominaler CA bei fixen Attributen, kein Attributkostenmesser.
[CA-Tabelle](https://github.com/jamiebolden/fm-scoring/blob/b5928ba2b9aba3c4c40a8f32118401eafb6f4c99/docs/ca_costs_fm27.csv)
und deren knapper Quellenkontext liefern keine unabhängigen Editorreadbacks,
Stufen8→9/17→18 oder Fuß-/Multipo­sitionskosten. Diese Unsicherheit wird nicht
durch die Spaltenbezeichnung „CA cost“ behoben.

[Harvestgreen22](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test),
[ZaZ](https://fm-arena.com/threads/training-schedules.60/),
[Zergos](https://sortitoutsi.net/content/78226/optimal-training-schedules)
und [Sports Interactive](https://www.footballmanager.com/fm27/features/fm27-training-and-tactical-effectiveness)
wurden direkt geöffnet. Keine fremden Ergebnisscreenshots als eigene
reproduzierte Messungen, Empfehlungen nicht als kausale Effektschätzung.
PA-Progression-Factor-Behauptungen erhalten ohne belastbare FM27-spezifische
Original-Code-/Saveprovenienz keinen Status „direkt durch Code bestätigt“.

Abrufhashes, Versionen und Zugriffsgrenzen werden in `source-audit.json`
gespeichert. Keine fremden Repositories, FMFs, Spielstände, DLLs oder
Trainingsanhänge werden in dieses öffentliche Forschungsarchiv kopiert.
