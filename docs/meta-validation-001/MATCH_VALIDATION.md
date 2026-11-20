# Lokale Matchabnahme · 20.11.2026

Die Steam-Installation meldete für game_plugin.dll die Produktversion **27.1.0+2505117**, Dateiversion 27.1, Steam-Build-ID 26620374. Der archivierte Adapter v1114.6 verweigerte diese DLL mit Exit 2. Für die Abnahme wurde das offizielle v1118.1-Release ausschließlich privat separat bereitgestellt. Release-EXE und Source-ZIP stimmten mit den GitHub-Digests überein. Die Steam-DLL stimmte mit der Referenz des Pakets überein. Der lokale Host meldete original_build_verified, kompatible Ressourcen und das Profil fm27_desktop_d12202dd_adapter_v1. [Release](https://github.com/lqf0624/fm-tactics-lab/releases/tag/v1118) · [Hashes für Engine, Host, Fixture und acht Setups](technical-plan.json)

| Objekt | SHA-256 |
|---|---|
| Release-EXE v1118.1 | `685c691390186a1d65301b06a5baa06eee1683afa57cf0f9d899179fdaa36c56` |
| Source-ZIP v1118.1 | `4ca1e5825d9b08a9ed40ed4c07845da5b4adaeb0fcbf12e260c770fa84b37f3d` |
| Release-Payload | `35283182cc04bbdcf8f3c4735dae72154dc67c697833dd3b4fc357cdfafc9fbc` |

**A.** Es fand kein nativer Transfer eines echten Scout-Kandidaten statt. Der Szenarioencoder bindet die Reihenfolge und nativen IDs an die Fixture-Träger. Der Adapter bietet separate Save-Importfunktionen. Eine vollständige Übernahme zweier konkreter Spieler des geforderten Exports einschließlich versteckter Merkmale und Positionsratings ist hier unbelegt.

**B.** 16/16 vollständige technische Matches in 16 einzeln gestarteten und ordnungsgemäß beendeten Steam-Sitzungen. Ein Worker, ein Heimfixture, ein Gegner, derselbe reservierte Seed 3539707856. 8 Setups, jedes zweimal. Wichtigkeit 10, je 23 aktive Profile. Je Match 4.726 nach der Originalvorbereitung bestätigte Eingaberecords, 22 gebundene Spieler in beiden Phasen und 322 Profilfeld-Readbacks. Alle 46 × 69 Attribute und die Identitäten wurden mit den Sollprofilen verglichen. Je Position wechselt zwischen den Stufen genau das JR-Feld 54 am vorbestimmten Starter. Innerhalb jeder A/A-Zelle stimmen Endstand, Endtick und ursprüngliche Teamstatistik exakt überein. Null fehlgeschlagene Matchaufrufe, Retries oder ausgeschlossene Ergebnisse. Kumulierte native Matchzeit 30,968 s ohne Sitzungsstart und Nachverarbeitung. Die privaten Originalbelege bleiben für die Nachrechnung erhalten.

| Heimstarter | Ballbesitz / gegen den Ball | Positionsrating aus vorbereitetem Profil |
|---|---|---:|
| Slot 10 | ST CentreForward / STL OPCentreForward | ST **1/20** |
| Slot 2 | DCR CentreBack / DCR OPCentreBack | DC **17/20** |

Der Stürmer wurde tatsächlich an der geplanten Stelle eingesetzt. Seine geringe Vertrautheit macht ihn für eine Interpretation als natürlicher Mittelstürmer ungeeignet. Für einen späteren Positionsvergleich ist die Eignung bei der Profilauswahl festzulegen. Das mitgelieferte Matchfixture wurde ausschließlich für die technische Reproduzierbarkeit verwendet.

**Originalspielanzeige.** FMSuperScout rundet beim Lesen sichtbarer Fähigkeiten den Rohwert geteilt durch fünf. Tactics Lab schreibt für seine Stufen das Fünffache. Der unabhängige Abgleich verwendete auf dem Zielbuild den mit dem Release gelieferten Save-Reader und die Original-FM-Eigenschaft AttributeJumpingReach, jeweils mit Abgleich der UniqueId und des tatsächlichen Anzeigetexts. Der Save stammt aus dem Spielzustand 12.03.2027. Am 17.03. zeigten drei identitätsgleiche Spieler aus den Rohstufen 35/45/80 exakt 7/9/16 (Untergrenze = Obergrenze = Text). Für den ersten Träger mit Rohwert 95 zeigte FM einen Strich, die beiden Grenzwerte waren −1. Fünf weitere zeitlich versetzte 95er-Proben am 20.03. lieferten 14–20, 17–20, 17–20, 13–20 und 17–20. In allen Fällen stimmte die Spieleridentität. Bei einer ersten Vorabfrage zu Rohwert 35 fehlte das Datumsfeld. Die dokumentierten späteren Abfragen verwendeten die Original-Eigenschaft CurrentGameDate. Weder maskierte Felder noch unterschiedliche Spieltage erlauben die vollständige Vierstufenkalibrierung. [Pseudonymisierte Belege](results.json)

Der eingefrorene Abnahmeplan wurde vor dem ersten Match auf dem Forschungsbranch veröffentlicht. Die eigenständige Nachrechnung liest aus den privaten Workerplänen das tatsächlich verwendete Fixture und dessen Hash, aus den Abschlussereignissen Score/Seed/Tick, aus den vorbereiteten Dumps Identitäten, JR und Positionseignung und aus den Sitzungsbelegen die Freigabe des Workers. Die öffentlich lesbare Prüfung kontrolliert Vollständigkeit, Planbindung und A/A-Identität. Beide Berechnungen stammen aus derselben Forschungsrunde. [Runner](../../analysis/meta_validation001_tech.py) · [Nachrechnung](../../analysis/review_meta_validation001.py) · [Kompakte Matchdaten](technical-matches.jsonl)
