# NIGHT-002: aktueller Primärquellen- und Neuheitsaudit

**Stand:** 14.11.2026, 22:23 UTC / 23:23 CET. Eigener Quellenreview,
keine unabhängige Nachrechnung externer Rohdaten, keine neuen Matches.
Der eingefrorene [Atlas](../FM27_EXTERNAL_STUDY_ATLAS_2026-11-14.md),
[35er-Index](../../research/fm27-external-study-index-20261114.json),
[lokale FINDINGS](../../FINDINGS.md), Methodik, Research Log, Roadmap,
NIGHT-001-Prioritäten, externe Replikationsprüfung und Meta-Score v0.1 wurden
vor der Kandidatenauswahl berücksichtigt. Historische Quellenarchive bleiben
unverändert. Neue Abrufe und Inhaltsprüfsummen stehen im
[NIGHT-002-Auditindex](../../research/night002-source-audit.json).

## Was gegenüber dem Atlas tatsächlich neu ist

- **Purity ergänzt Torhüter:** Im [originalen Positionsthread, Beitrag #8](https://fm-arena.com/threads/attribute-importance-by-position-in-fm27-a-test-on-my-own-tactic.125/)
  vom 14.11., **13:32:30 UTC**, steht eine zusätzliche, laut Autor eigene
  200.000-Match-Kampagne mit 48 Keeperattributen, Brentford/3-4-2-1 und auf 100
  gesetzter Tactical Effectiveness. Neue Quellen-ID `FM27-PURITY-GK-20261114`.
  Dies ist eine Erweiterung derselben Purity-Autorenfamilie; Kamas' nachfolgende
  Genie-Scout-Gewichte sind keine unabhängige Replikation. Allgemeine
  Keeper-Rankings sind damit noch weniger als neue Forschungsfrage begründbar.
  Konkrete Regressionsrohjobs und Buildhashes wurden nicht nachgerechnet.
- **FMAX ist weitergewandert:** [Live-HTML](https://getfmax.com/en/lab/) nennt im
  ersten 30er-Ausschnitt inzwischen Diamonds 1.4 STL mit 75,5 und Hearts 1.6 STL
  ebenfalls mit 75,5 Punkten. Der Suchindex liefert noch den alten Snapshot
  Hearts 76,1 / 186 Taktiken / 205.400 Matches. Diese alten Gesamtzahlen werden
  **nicht** als aktueller Census weiterverwendet. Live-Ränge sind Paketbenchmarks,
  keine kausale Zerlegung des Stürmerlos-Mechanismus.
- **Mac-Studien unverändert:** [HEAD e92cf141](https://github.com/caiograco289/Fm-Match-Lab/commit/e92cf1416ca5c8c4b13009f8cf7d695f290b0368)
  vom 14.11., 14:46:59 UTC bleibt der neueste Commit. Der Baum enthält
  **23 einzelne Studienseiten plus README = 24 Markdownseiten**; keine neuen
  Studien 16/18 oder abgeschlossenen Catenaccio-13b-Lauf hinzuerfinden.
  Alle Seiten wurden aktuell abgerufen und gehasht; Designs, Einschränkungen
  und für die Auswahl relevante Originalberichte/Implementierungen geprüft.

## Quellfamilien, aktueller Inhalt und Grenze

| Quellen-IDs | Originalquelle / geprüfter Stand | Konsequenz für NIGHT-002 |
|---|---|---|
| MAC-01/02/12/13/13B/14/14B | [Studienverzeichnis @ e92cf141](https://github.com/caiograco289/Fm-Match-Lab/tree/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies) | Globale, Positions-, Liga- und Dosisrankings umfangreich vorbearbeitet; neue Studie braucht andere kausale Interaktion oder eingefrorenen Prognosetest. Ältere Nullbefunde werden durch 13b teilweise präzisiert. |
| MAC-03/04/17 | [Familiarity](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/03-tactical-familiarity.md), [IP/OOP-Ratings](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/17-positions-in-and-out-of-possession.md) | Künstliche Recordwerte, Positionsratings und tatsächliche Formationspositionen unterscheiden. Kein Nachweis realer Trainingslernrate; 17 erklärt den Zonenmechanismus ausdrücklich nicht abschließend. |
| MAC-05 | [Bericht](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/05-everything-else.md), [originaler Builder](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study5_everything.py) | Sharpness-Bedingungen schreiben beide Felder gemeinsam. Keine gekreuzten C90/C7A-Arme. |
| MAC-06/07/07B/19; FM27-FMAX-LAB | [Mac-Taktikliga](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/07b-tactic-league-18.md), [FMAX](https://getfmax.com/en/lab/) | Ranglisten vergleichen mehrere gleichzeitig variierende Komponenten. Kontrollierte ST→AMC-Pakete mit fester OOP-Struktur darin nicht identifiziert. |
| MAC-08 | [Tactical Tweaks](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/08-tactical-tweaks.md) | Alle Eingriffe ab Anpfiff; späte Aktivierung nach Minute/Score ausdrücklich nicht unterstützt. Späte Spielmanagementfrage bleibt eigenständig, benötigt aber neue sichere Eingriffsmessung. |
| MAC-09/10/11/15/15B/20/21 | [Originalberichte @ e92cf141](https://github.com/caiograco289/Fm-Match-Lab/tree/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies) | Attributgruppen, Hidden-Werte, CA und Standort-Haupteffekte nicht erneut breit screenen. Publikum, Stadion und Matchumgebung sind in 15b ausdrücklich nicht getrennt. |
| FM27-PURITY-POS; FM27-PURITY-GK-20261114 | [Purity-Originalthread](https://fm-arena.com/threads/attribute-importance-by-position-in-fm27-a-test-on-my-own-tactic.125/) | Ein Klub/eine Taktik; Zielgröße Goal Difference wird im Thread klargestellt. Keeper-Erweiterung berücksichtigt. Keine universellen Positionsgewichte daraus ableiten. |
| FM27-HARVEST-ATTR | [Harvestgreen22-Originalbeitrag](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test) | Dosen 1/6/12/18 und FMRTE-gesperrte Zustände; Autor benennt begrenzte Stichprobe und Unsicherheit. Excel/Bilder nicht unabhängig nachgerechnet. |
| FM27-ZAZ-TRAIN | [Training Schedules](https://fm-arena.com/threads/training-schedules.60/) | Trainingsguide und einzelne Sharpness/Minuten-Beobachtungen; kein kontrollierter Split-Field-Nachweis oder unabhängiger Karriere-RNG-Versuch. |
| FM27-MAC-MIRROR | [caiograco-Sammelthread](https://fm-arena.com/threads/fm27-match-engine-what-we-know-so-far.122/) | Spiegel derselben Mac-Studien, keine zweite Replikation. |
| FM27-FMTL-METHOD | [FM Tactic Lab Methode](https://www.fmtacticlab.com/fm27-test-method) | Seite steht weiter auf 5.11. und sagt, noch kein Test sei durchgeführt. Kein neues validiertes Ergebnis gefunden; nicht mit dem Windows-Quellprojekt verwechseln. |
| FM27-TACTICS-LAB | [Upstream HEAD cdda4be](https://github.com/lqf0624/fm-tactics-lab/commit/cdda4be7280aa74681f015c02be77d7b47eacc4a) | Aktuelles Release-API nennt v1114; der lokal validierte Quelltag v1114.6 ist separat gepinnt. Kein automatisches Update oder behauptete neue Buildvalidierung. |

## Aktueller Patchstand

Das [offizielle SI-Updateforum](https://community.sports-interactive.com/forums/forum/905-fm27-updates)
zeigt beim Abruf die Launch-Mitteilung und das Minor Update vom 2.11. Die
[offizielle französische Launch-Mitteilung](https://community.sports-interactive.com/forums/topic/612981-mise-%C3%A0-jour-de-lancement-fm27-2701/)
vom 10.11. nennt ausdrücklich **27.0.1**. Der
[SI-Ausblick vom 9.11.](https://community.sports-interactive.com/forums/topic/612924-details-on-fm27-launch-patch-notes-and-first-post-launch-update/)
kündigt einen weiteren Postlaunchpatch später im Monat an. Keine neuere
veröffentlichte Engineversion wurde in diesen geprüften Primärquellen gefunden.
Das beweist weder Abwesenheit jeder neueren Veröffentlichung noch einen lokalen
DLL-Hash. Exakte Version/Hash, Host, Fixture und Ressourcen sind pro nativer
Phase durch den Director gesondert zu prüfen.

Die [SI-Enginebeschreibung](https://www.footballmanager.com/fm27/features/fm27-tactical-tweaks-and-match-engine-upgrades)
motiviert Fragen zu Ausdauer und Positionsbewegung; die
[SI-Trainingsbeschreibung](https://www.footballmanager.com/fm27/features/fm27-training-and-tactical-effectiveness)
beschreibt Effectiveness/Complexity. Beides sind Herstellerbeschreibungen,
keine unabhängigen Wirkungsdaten oder C90/C7A-Prozentskalen.

## Ausgewählte Neuheit und priorisierte nächste Fragen

**1. MECH-004-SPLIT-R0: `NOVEL_HYPOTHESIS`.**
Überlappung: `MAC-05`, `MECH-002-SHARPNESS-P0`. MAC-05s Builder setzt
`sharpness` und `sharpness_secondary` gemeinsam auf denselben Wert; der
[Profilcodec](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/src/fm27_profiles.py)
benennt trotzdem getrennte Eingabefelder 16/17. Lokales MECH-002 untersucht
ebenfalls nur die gemeinsame Diagonale. Die neue Frage lautet, ob die beiden
gekreuzten Rohzustände C90=10000/C7A=7000 gegenüber C90=7000/C7A=10000
unterschiedlich wirken. Primär der gepaarte xGD-Offdiagonalkontrast; andere
Felder, Positionsratings, Spielerzahl und Management konstant. Neu ist die
relative Identifizierbarkeit der Felder, kein weiterer gemeinsamer Haupteffekt.
Separate native Schreib-/Vorbereitungs-/Cache-Readbacks und Legalität sind
zwingend. Ein legaler Labzustand ist noch kein in einer Karriere erreichbarer
Zustand; Consumer- und Physiologiesemantik bleiben offen. **Literaturfreigabe
erteilt; keine technische oder wissenschaftliche Startfreigabe durch diesen Text.**

**2. Kontrollierter ST→AMC-Vergleich: `NOVEL_HYPOTHESIS`.**
Überlappung: `MAC-06/07/07B/19`, `FM27-FMAX-LAB`, `TACT-002-R0`.
Gleiche Spieler und Profile, deklarierte IP-Positions-/Rollenänderung,
OOP-Zuordnung fest. Primär xGD im explorativen Paketpilot, Punkte/Tore/Gegentore
zusätzlich. Neu wäre ein isoliert definierter veränderbarer Teil eines
stürmerlosen Pakets. Formation, Rolle, persönliche Anweisungen und Complexity
dürfen nur bei belegter Gleichheit als separat identifiziert gelten.

**3. Rollen-/Positionskontext × marginale Attributwirkung:**
`NOVEL_HYPOTHESIS`, falls genau ein bisher ungeprüfter, nativ validierter
Rollen-/Positionsmoderator festgelegt wird. Überlappung `MAC-02/12/13B/17`,
`FM27-PURITY-POS`, `ATTR-009`. Nach erfolgreichem Strukturpilot zuerst einen
konkreten JR- oder Antrittseingriff im neuen Kontext testen; nicht einfach
Positionstabellen wiederholen oder den synthetischen Rohwert als UI-Wert
ausgeben. Hoher Scoutingnutzen, aber Profil-/Dosengates und ausreichende
Interaktionspräzision vor Lauf erforderlich.

Die vollständige Kandidatenmatrix mit mindestens acht konkreten Fragen,
Kontrollen, Einheiten, Aufwand und Abbruchentscheidungen wird zentral in
[NOVELTY_MATRIX.md](NOVELTY_MATRIX.md) geführt. Echte Eckenausführungen,
eingefrorener Meta-Score auf gehaltenen Daten und GK×Defensivlinie bleiben
eigenständige Alternativen, sobald ihre spezifischen Messgates bestehen.
Gemeinsame Sharpness-Wiederholung und Reaktivierung des terminal gestoppten
Staminaversuchs sind `DUPLICATE_STOP`; unlesbare Shout-Quellen zunächst
`UNCERTAIN_SOURCE`.

## Grenzen dieses Reviews

Neuheit bedeutet ausschließlich **in den tatsächlich geprüften lokalen und
externen Quellen nicht beantwortet**. Gezielte Suchen nach C90/C7A,
`sharpness_secondary`, kontrollierten stürmerlosen Vergleichen und Nettoertrag
pro Ecke fanden keinen solchen Split-Field-Nachweis. Unvollständige Indexierung,
nicht öffentlich zugängliche Daten und spätere Veröffentlichungen bleiben
möglich. Kein Begriff „weltweit erstmals“. Kein nativer Prozess, Seed, Save,
Kalenderadvance oder Match wurde durch den Research Agent ausgeführt.
