# Klubtraining und Stabilität des ursprünglichen PA-Ziels

## Können zwei Anlagenniveaus im Kontrollmonat unterschieden werden?

Der unveränderte Rust-Reader **fm27-scout-code 1.6.1** lieferte für die privaten Saves vom 30.03. und 30.04.2027 je 42.001 Klubzeilen. 188 enthielten einen numerischen Trainingsanlagenwert. Alle 188 behielten ihren gelesenen Wert. Sieben Klubs lagen bei 16 und vier bei 17. Der Reader sucht die Trainingsanlage in der Klubinfotabelle der Vereine mit monatlicher Finanzhistorie. Klubzugehörigkeiten und Einrichtungen sind in dieser Stichprobe deshalb stark selektiv. [Readerquelltext](https://github.com/shlk20/fm27-scout-code/blob/7fb12175f59b4d41b4418bf0378c3855a5bab4bd/crates/fm27-core/src/facilities.rs) · [Messwerte](../../research/pa-reach-001/manifests/facilities-and-pa.json)

| Abdeckung unter Feldspielern unter 28 am 30.03. | Identitäten | Mit identischem Anlagenwert an beiden Tagen | Gelesene 16 | Gelesene 17 |
|---|---:|---:|---:|---:|
| Nativ bestätigter, gleicher Klub an beiden Tagen | 25.059 | 1.533 | 169 | 138 |
| Zusätzlich identische PA, gleicher Faktor 1–4 und Ausgangs-CA mehr als zwei Punkte über dem berichteten Limit | 6.326 | 342 | 42 | 30 |

Diese Zahlen beschreiben die Abdeckung für einen möglichen Grenztest. Externe Tests vergleichen Trainingsanlagen mit den Einrichtungen-Bildschirmen von sieben Vereinen, prüfen numerische Regressionserwartungen und vergleichen die Klubstruktur mit dem Vorgängerbuild. Eine lokale unabhängige numerische Ablesung für beide Seiten der Schwelle fehlt. Die Bildschirmbezeichnung *Excellent* deckt nach der veröffentlichten Zuordnung **sowohl 16 als auch 17** ab. Ein Screenshot dieses Texts könnte die strittige Grenze daher nicht auflösen. Die drei lokalen Spieler-Vollscans enthalten keine numerische Trainingsanlage. Die Anlagen-API des eingesetzten fmsave 0.14.1 liefert das separat benannte Feld `corporate_facilities`. [Externer Validierungsbericht](https://github.com/shlk20/fm27-scout-code/blob/7fb12175f59b4d41b4418bf0378c3855a5bab4bd/docs/validation.md) · [Stufenzuordnung](https://github.com/shlk20/fm27-scout-code/blob/7fb12175f59b4d41b4418bf0378c3855a5bab4bd/apps/desktop/src/lib/labels.ts) · [fmsave-Anlagenmodell](https://github.com/rhiever/fmsave/blob/v0.14.1/src/fmsave/models/facilities.py)

Der nächste Nachweis erfordert einen unabhängigen, numerischen **Training Facilities**-Wert für mehrere eindeutige Klubidentitäten beiderseits der Schwelle, etwa eine rein lesende, benannte Eigenschaft der Spielengine oder den numerischen Ingame-Editor auf einer gesonderten Kopie. Zu erfassen sind jeweils Build, Save-Prüfsumme, Spieltag und derselbe Klub. Erst damit lässt sich der Grenzkontrast im beobachteten Kollektiv schätzen. Selbst dann trennt ein Netto-CA-Zuwachs die mutmaßliche Monatsfreigabe nicht vom Wachstum nach einer Freigabe. [Grenzfallanalyse](PROGRESSION_FACTOR_VALIDATION.md)

### Was zeigt der nativ benannte Anlagenwert?

Am 07.04.2027 wurde im Retentionsarm für sechs Kandidatenklubs mit einem Readerwert von 16 oder 17 jeweils ein zugehöriger Spieler abgefragt. Die Leseabfrage lief innerhalb einer Datumsklammer am selben gespeicherten Checkpoint. Die Spieler-ID und das Geburtsdatum stimmten in allen sechs Fällen mit dem Save und seinem nativen Referenzinventar überein. Die vom Spielerobjekt aus durchlaufene Verbindung `PrimaryClubTeam.Club.UniqueId` ergab bei vier Spielern genau den vorab ausgewählten Klub. Zwei abweichende Klubzuordnungen sind ausgeschlossen. [Grenzstichprobe](../../research/pa-reach-001/manifests/named-facility-boundary-0407.json)

Die benannte Eigenschaft `Club.TrainingFacilityRating` enthält eine Zahl `Rating`, einen angezeigten Bereich und eine Beschreibung. Bei den drei bestätigten Reader-16-Klubs und dem einen bestätigten Reader-17-Klub ergaben Zahl, Unter- und Obergrenze jeweils **18**. Der Text lautete in allen vier Fällen „Exzellente Trainingseinrichtungen (8/10)“. Das Feld für eine Scoutschätzung war jeweils deaktiviert. Diese Spielanzeige unterscheidet die beiden fraglichen benachbarten Zahlenwerte nicht. [Eigenschaftsprüfung](../../research/pa-reach-001/analysis/named_facilities.py)

Bei weiteren zehn vorab bestimmten, verschiedenen Klubs stimmten neun Klub-IDs überein. Die Paare von Save-Readerwert zu benannter UI-Zahl lauteten 7→13, 8→14, 10→15, 11→15, 12→16, 13→16, 14→17, 15→17 und 18→19. Der benannte Wert variiert über Klubs, mehrere benachbarte Readerwerte teilen sich eine dargestellte Stufe. Diese ausgewählten Fälle belegen weder die vollständige Umrechnungsskala noch den kausalen Effekt einer Anlage. Die exakte Trennung 16/17 bleibt ohne unabhängige Zahlenreferenz. [Kontrollen außerhalb der Grenze](../../research/pa-reach-001/manifests/named-facility-range-0407.json)

## Änderte sich das PA-Ziel?

Beide Stichtage jedes Intervalls erforderten eine eindeutige Identität über ID und Geburt sowie eine übereinstimmende CA/PA-Messung aus Save und nativem Inventar. Die folgende Zählung schließt Spieler unabhängig von einer möglichen PA-Veränderung ein.

| Intervall | Stichprobe zu Beginn | Einbezogene zu Beginn | An beiden Tagen bestätigt | Kein Identitätspaar am Ende | Andere PA am Ende |
|---|---|---:|---:|---:|---:|
| 31.01.–30.03. | Alle | 94.708 | 94.585 | 123 | 0 |
| 31.01.–30.03. | Feldspieler unter 28 | 60.635 | 60.550 | 85 | 0 |
| 30.03.–30.04. Kontrollkopie | Alle | 97.258 | 97.062 | 196 | 0 |
| 30.03.–30.04. Kontrollkopie | Feldspieler unter 28 | 62.047 | 61.920 | 127 | 0 |

Der persönliche historische Ausgangspfad war in der Konfiguration von FMLivingPotential Seasons 0.13.0 als zulässiges Ziel eingetragen. Für den umbenannten Kontrollarm ist die aktive Pfadbeschränkung belegt. Gleiche PA an den Vergleichstagen lässt mögliche frühere oder zwischenzeitlich rückgängig gewordene Änderungen offen. Eine individuelle Modwirkung erfordert ein datiertes, dieser Karriere und Identität zugeordnetes Schreibprotokoll. Beide Intervalle stammen von derselben Karriere. [Modkontext](NATIVE_BRIDGE_VALIDATION.md) · [Aggregat](../../research/pa-reach-001/manifests/facilities-and-pa.json) · [Reproduktion mit privaten Karrieredaten und festgelegtem Readerstand](../../research/pa-reach-001/analysis/facilities_and_pa.py)
