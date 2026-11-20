# Jugendaufnahme und jährliche Vertragsbindung

Seit dem 15. Juni 2027 bleiben die offenen Problemverträge ihrem regulären Ablauf überlassen. Änderungen der Laufzeit, Abgänge und spätere Entwicklung werden in den regulären Messständen ausgelesen. In späteren jährlichen Angebotsrunden werden bereits abgelehnte oder anhängige Vorgänge übersprungen. [Datierte Änderung des Versuchsplans](EXPERIMENT_DESIGN.md)

Für künftige Zubieta-Spielzeiten gilt die vom Nutzer festgelegte aktive Vertragspolitik auf dem privaten Retentionszweig. Alle Jugendkandidaten und alle eigenen Spielerverträge einschließlich Jugend, Reserve und auswärtig eingesetzter eigener Spieler gehören zur jährlichen Prüfung. Die private Ausgangskopie vom 30. März bewahrt den Zugang zum Intake am 31. März.

### Belegter Ausgangsbestand und Vergleich

| Bilanz | 30. März | 30. April, Urlaubskontrolle |
|---|---:|---:|
| Vom eigenen Klub gehaltene Verträge | 83 | 99 |
| Bis 30. Juni 2027 fällige Altverträge | 29 | 29 |
| Gegen den datierten Scanner bestätigte Fälligkeiten in dieser Gruppe | 29 | 29 |
| Ausgangsverträge mit unverändertem Enddatum | – | 83 |
| Neu beobachtete eigene Vertragszuordnungen ohne festes Ende | – | 16 |

Sieben der 83 Ausgangsverträge gehören Spielern außerhalb des aktuell registrierten eigenen Kaders. Ein registrierter Spieler hat einen anderen Vertragseigentümer. Bei allen 29 fälligen Ausgangsverträgen war die Zuordnung eindeutig. Die 16 Zugänge des Urlaubsarms haben im Save ein gemeinsames Eintrittsdatum am 31. März, sind 15 oder 16 Jahre alt und besitzen noch kein bestätigtes festes Ende. Zur eindeutigen Klassifikation als Jugendkandidaten dient die Intake-Liste des jeweiligen Zweigs. Jugendspieler aus getrennten Fortschreibungen können unterschiedlich ausfallen. [Märzinventar](../../research/pa-reach-001/manifests/zubieta-contracts-march.json) · [Aprilinventar](../../research/pa-reach-001/manifests/zubieta-contracts-april-control.json) · [Gepaarte Vertragsbilanz](../../research/pa-reach-001/manifests/control-contract-followup.json)

### Zählregeln im Retentionszweig

- Vollständige jährliche Liste vor den frühesten Fristen abgleichen, einschließlich noch langfristig gebundener Spieler. Kandidaten mit Intake-Beleg gesondert erfassen.
- Persönliches Angebot, Annahme, zugesagter künftiger Vertrag und bereits wirksamer neuer Vertrag sind getrennte Zustände. Für eine bestätigte Verlängerung die neue Laufzeit auslesen. Für eine Mechanikstudie zum Vertragsbeginn den Beginn relativ zum Stufenwechsel zeitlich absichern.
- Ablehnung, fehlendes Budget, Mindestalter, nicht eröffnete Verhandlung, bestehender langfristiger Vertrag und unklare Identität behalten ihre eigenen Gründe. Fehlende Follow-ups erlauben keine Aussage über einen Abgang.
- Der Kontrollarm trägt seine bisher beobachtete Urlaubs- und Vertragspolitik. Gemeinsamer Ausgangspunkt, unterschiedliche neu erzeugte Spieler und mögliche spätere Klub-/Trainereffekte begrenzen den kausalen Vergleich. [Experimentdesign](EXPERIMENT_DESIGN.md) · [Vergleichsprogramm](../../research/pa-reach-001/analysis/contract_followup.py)

Am 31. März wurden allen 16 Kandidaten einzeln Vertragsbedingungen vorgelegt. Die 16 Angebote wurden über die Intake-Liste jeweils eindeutig einer Person zugeordnet. Die unterbreiteten Bedingungen sind am Stichtag noch keine wirksamen Verträge. Dieselben 16 Identitäten sind auch in der Urlaubskontrolle im April nachweisbar. Alle hatten im Retentionszweig bei der Aufnahme den Faktor 0. Im April-Kontrollzweig lagen die Faktoren bei 1 (ein Spieler), 2 (einer), 3 (einer) und 4 (dreizehn). Die beiden Spielstände unterscheiden sich in Datum und Behandlung. [Intake-Abgleich](../../research/pa-reach-001/manifests/zubieta-intake-cross-branch.json) · [Vertragsbestand nach Angeboten](../../research/pa-reach-001/manifests/zubieta-contracts-retention-0331.json)

Die Meldung zu auslaufenden Verträgen am 31. März umfasste dieselben 29 Spieler wie das Saveinventar. Für alle 29 wurde die Verhandlung im Spiel einzeln dem Sportdirektor übergeben. Anschließend war eine ausdrückliche Absage wegen Transferlistung sichtbar. Ob die Verhandlungen zu einer längeren Laufzeit führen, entscheidet der spätere Vertragsabgleich. Die übrigen 54 Ausgangsverträge haben ein späteres Ende. [Aktionsbelege](../../research/pa-reach-001/manifests/bridge.json)

### Wirksame Verträge am 7. April 2027

Alle **16 von 16** identitätsgeprüften Kandidaten besitzen nun einen laufenden eigenen Vertrag mit festem Enddatum. Save und datierter Vollscan stimmen bei allen 16 Enddaten überein. Der Save zeigt 15 Jugendverträge und einen Vollzeitvertrag. Zwei beginnen am 2. April, 14 am 3. April. Ein Vertrag endet im Juni 2029, elf im Juni 2030 und vier im Juni 2031. Elf Spieler haben zusätzlich zukünftige Vertragsbedingungen im selben Klub. So lassen sich der erste wirksame Vertrag und eine erst später startende Vertragsperiode getrennt verfolgen. [Jugendverträge](../../research/pa-reach-001/manifests/intake-contract-followup-0407.json) · [Identitäts- und Laufzeitabgleich](../../research/pa-reach-001/analysis/intake_contract_followup.py)

Bei **28 der 29** bis Juni fälligen Altverträge sowie zwei der 54 länger laufenden Verträge wurde ein neuer Beginn im Beobachtungsintervall und ein in beiden Quellen bestätigtes späteres Ende festgestellt. Alle 83 Ausgangsspieler ließen sich wiederfinden. Die übrigen 53 hatten am 7. April dasselbe Vertragsende wie im März. Ein unverändertes Ende gibt für sich keinen Aufschluss darüber, ob eine Person eine Anfrage erhalten hat. [Vergleich der 83 Ausgangsverträge](../../research/pa-reach-001/manifests/retention-contract-followup-0407.json) · [Vollscan am 7. April](../../research/pa-reach-001/manifests/zubieta-contracts-retention-0407-scanned.json)

### Vollständige Jahresrunde und Vergleich am 30. April

Bei allen **83 Ausgangsvertragsspielern** ist die Einzelbearbeitung dokumentiert. FM bestätigte bei 77 einen Verhandlungsauftrag und bei vier weiteren ein aktives Angebot. Zwei verweigerten die Verhandlung sofort, darunter der bereits bis Juni 2029 gebundene Spieler, der am 16. März unterschrieben hatte. Unter den 77 delegierten Fällen gingen anschließend zwei weitere ausdrückliche Absagen ein. Die vier bekannten Absagen schließen einen ausgeliehenen, transfergelisteten Spieler mit Ablauf im Juni ein. Die zweite Sicherung vom 7. April bewahrt diesen Bearbeitungszustand. In 108.989 gepaarten Spielerrecords blieben über die beiden Speicherungen desselben Tags CA, PA, Faktor und 52 gespeicherte Attribute gleich. [Jahresbilanz](../../research/pa-reach-001/manifests/bridge.json) · [Gleichdatiger Vergleich](../../research/pa-reach-001/manifests/retention-april7-action-snapshot-invariance.json)

Am 30. April hatten **64 von 83** ein bestätigtes späteres Vertragsende und einen neuen ausgewiesenen Beginn. Darunter sind 28 der 29 ursprünglich fälligen sowie 36 der 54 länger laufenden Verträge. Alle 16 Jugendlichen waren weiterhin gebunden. Im Kontrollzweig behielten alle 83 ihren ursprünglichen Endtermin und für sämtliche 16 Kandidaten fehlte ein bestätigtes festes Ende. [Bestandsverträge](../../research/pa-reach-001/manifests/retention-contract-followup-0430.json) · [Jugendverträge](../../research/pa-reach-001/manifests/intake-contract-followup-0430.json) · [Kontrollzweig](../../research/pa-reach-001/manifests/control-contract-followup.json)

| Vorab definierte Gruppe | Am selben Tag in beiden Zweigen gepaart | Mittlere CA-Differenz Retention minus Kontrolle | Unterschiedliche gespeicherte Faktoren |
|---|---:|---:|---:|
| Bis Juni fällige Bestandsverträge | 29 von 29 | +0,414 | 19 |
| Länger laufende Bestandsverträge | 54 von 54 | −0,056 | 24 |
| Jugendkandidaten | 16 von 16 | −0,125 | 8 |

Bei allen 99 war die PA im Armvergleich identisch. Der reguläre native Inventarlauf erfasste die 16 Jugendkandidaten der Kontrolle nicht. Der bereits zu diesem Spieltag geklammerte separate FMSuperScout-Vollscan enthielt alle 16. Für jede Person passten eindeutige ID, Geburtstag, CA und PA zum gehashten Kontrollsave. Im Retentionsarm gelang der Abgleich aller 99 über das reguläre native Inventar. Bei acht Kandidaten unterschieden sich die gespeicherten Faktoren zwischen den beiden Armen. Die PA-Ausschöpfung dieser Jugendlichen am Ende der Entwicklungsphase ist offen. Eine unabhängige Karriere für eine Unsicherheitsschätzung des Politikeffekts fehlt. [Matrizen, Quellhashes und Ausfälle](../../research/pa-reach-001/manifests/club-branch-comparison-0430.json) · [Reproduktion](../../research/pa-reach-001/analysis/club_branch_comparison.py)
## Jugend- und Vertragsrunde im Frühjahr 2028

Am 5. April erhielten alle 16 erstmals am 31. März im Klubbestand erschienenen Jugendkandidaten jeweils ein individuelles Angebot. Alle 16 Angebotsquittungen sind über Identität und Geburtsdatum mit dem vorher fixierten Jahrgang verbunden. Die Angebote allein belegen keine Unterschriften. [Ausgangsstichprobe](../../research/pa-reach-001/manifests/zubieta-intake-2028-april-baseline.json)

Für die 98 Bestandsspieler ergibt der Abgleich der März- und April-Aktionen 38 bestätigte Verhandlungsaufträge, 36 ungeklärte Ergebnisse nach einmaliger Bearbeitung, drei nicht zweifelsfrei identifizierte Profile, 18 aus der Vorjahresliste ausgenommene Spieler und drei unbearbeitete Spieler. Bei keinem Bestandsspieler wurde ein zweiter Verhandlungsversuch protokolliert. Alle drei am 5. April noch bis Juni auslaufenden Verträge gehörten zur Ausnahmeliste. Die Jahresrunde wurde zugunsten der anstehenden Messungen beendet. [Quellhashes und Statuszählung](../../research/pa-reach-001/manifests/annual-actions-20280405.json) · [Abgleich der einzelnen Quittungen](../../research/pa-reach-001/analysis/retention_actions_2028.py)
