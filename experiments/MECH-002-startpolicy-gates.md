# MECH-002 – Startpolicy: technische Sperre nach Quellenprüfung

14.11.2026. **Technische Vorarbeit, keine wissenschaftliche Registrierung oder
Ausführung.** Verbindlicher Auftrag: [Runde3](NEXT-ATTR-MECH-TRAIN-round3.md).
Historische MECH-/TACT-/ATTR-Dokumente bleiben unverändert. Vorläufiger
[JSON-Vertrag](../data/mech-002/contract-draft.json),
[eigener Offlineprüfbericht](../data/mech-002/offline-report.json),
[Quellprovenienz](../data/mech-002/source-audit.json).

## Tatsächlicher Status

**Blockiert, vor Seedreservierung und nativem Start.** 0 neue native Starts,
0 technische Prüfmatches, 0 Hauptmatches, 0 neue Seeds. Alle 512 geplanten
Hauptmatches und 35 technischen Plätze unbegonnen. Keine Ausfälle/Ergebnisse,
keine Ersatzsimulationen, Holdouts, Karrierefortschreibung oder Clamp-Hooks.
Die technische Ablehnung ist kein gemessener Schärfeeffekt.

Lesend verifiziert: FM-Dateiversion27.0.1, Produkt27.0.1+2503222, Tooltag
v1114.6/91f2eba57fac0b7fbd3dff616056907e3ce461be. DLL-, Host- und
gebündelte Fixture-SHA256 entsprechen VALID-002; vollständige Werte im
Quellbeleg. Kein neuer Ressourcen-/Loaderaudit, kein eigenständig reproduzierter
Hostbuild. Die alte VALID-002-Freigabe gilt weiter nur für ihren alten Pfad.

## Quellenprüfung und harte Gates

Referenzen sind die tatsächlich lokal gelesenen Dateien am genannten Commit,
keine aus Gesprächszusammenfassungen übernommenen Testbehauptungen. C++ stammt
aus der sauberen lokalen Upstreamkopie `local/upstream/fm-tactics-lab/native/`,
Python aus der installierten Runtime `local/runtime-v1114.6/source/`.
Quellhashes und der Hash des gelieferten Hosts sind getrennte Belege; diese
Prüfung beweist keine bytegenaue Übersetzung des Hosts aus jener Quellkopie.

| Gate | Quellbefund / Konsequenz |
|---|---|
| Historische Normalisierung | [Server210,323–382](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_tactics_server.py#L210) überschreibt beide Schärfefelder mit10000; `encode_scenario()` normalisiert erneut. Einfaches JSON7000 ist kein neuer wirksamer Pfad. |
| Zeitpunkt nach Originalvorbereitung | [Host799–822](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/desktop_host.cpp#L799) ruft `apply_scenario` **vor** Originalvorbereitung809 auf; danach `verify_scenario`815, Dump817, initialer Snapshot822. Kein eigener Setter nach Vorbereitung. Selbst ein erfolgreicher Readback wäre kein Beleg des verlangten Setzzeitpunkts. |
| Startreadback | [native_statistics.h3–16](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_statistics.h#L3) liest beide Schärfefelder und weitere Zustände einmal nach Vorbereitung. Diese existierende Quelle beweist noch keinen neuen opt-in-Lauf. |
| Erste Fortschreibung | [Host904–907](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/desktop_host.cpp#L904) schreitet fort und schreibt periodisch Tick/Clock; kein passiver Profil-/Schärfesnapshot direkt nach dem ersten Schritt. **Nicht erfüllt.** |
| Passive Original-Familiarity | [execution_snapshot158](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_execution_experiment.h#L155) endet bei `!execution_active`. Aktivierung installiert intervenierende Hooks/Versionsmarker. Das ist kein passiver Originalrecordaudit; Dict-Understanding verändert aggregiertes Overall, nicht isoliert24Bereichsbytes. **Nicht erfüllt.** |
| Runnerbindung | [NativeLab.run](../research/native.py) verlangt weiterhin exakte historische Serverbytes. Er bleibt unverändert; kein Override/Monkeypatch/ungeprüfter Binärtransport. Neuer Audit-/Runnerpfad fehlt. **Nicht erfüllt.** |

Die Event-/Statistikaudits erfassen zusätzliche Statistikrecords, aber keine
vollständige passive Familiarity und keinen ersten Profil-Fortschreibungssnapshot.
Experimental execution bleibt verboten. Eine Nach-Vorbereitungsänderung könnte
außerdem bereits berechnete Ableitungen auslassen; ein künftiger Adapter muss
die native Nutzung bzw. Invalidierung dieser Ableitungen nachvollziehbar belegen.

## Implementierte sichere Vorarbeit

[research/startpolicy.py](../research/startpolicy.py) implementiert einen eigenen
versionierten **Offline-Recordcodec**, keine Hostintegration. `None` erhält die
Standardbytes; explizites `StartPolicy(side,7000)` erzeugt aus geordneten
absoluten Records neue Records und serialisiert sie vollständig. Nicht als
nachträglicher Patch eines eingereichten Runnerjobs verwenden. Keine
Serverimporte, Dateiänderungen, Prozesse, Adress-/Memorywrites oder Runtimehooks.

Opt-in setzt ausschließlich Feld16/17 gemeinsam bei den zehn Feldspielern der
angegebenen D00-Startelf. D00-Zell0 bindet den GK, Zellen1..10 die Feldspieler;
das bleibt zusätzlich nativ anhand tatsächlicher Phase/Identität zu beweisen.
Die Startelf wird aus den absoluten Lineuprecords gebunden, nicht als
Rosterindizes1..10 geraten. Gegenmannschaft/GK/Bank und alle übrigen Records
bleiben bytegleich. Condition10000/Fatigue0 und vollständige kontrollierte
Startprofile beider Kader werden verlangt; unbekannte/doppelte Profilfelder,
ungültige Rohwerte, unvollständige Lineups und Executionrecords werden abgewiesen.
7000 ist ein Rohwert, keine belegte70-%-Karriereanzeige.

[verify_mech002_preparation.py](../analysis/verify_mech002_preparation.py) ist ein
rein lesender privater Binärvergleich. Vier echte archivierte D00/R00-Eingaben
(zwei Discoverygegner×beide Seiten, jeweils5557Records) wurden geprüft:
Default/full exakt bytegleich; low auf jeder Seite exakt20 erlaubte
Schärfewertdifferenzen. Das ist ein **Kodierungsbeleg**, kein neuer nativer
Eingabe-/Zeitpunkt-/Effektivitätsbeleg. Öffentlicher Bericht enthält nur Namen,
Hashes, Zähler; keine Binärdateien, Spieleridentitäten oder privaten Pfade.

Sieben portable Unit-Tests decken beide Seiten, nichttriviale Lineupzuordnung,
Default/full-Gleichheit, genaue Änderungsmenge, Schema-/Binärnegativfälle und
unveränderliche Eingaben sowie Kontrastvorzeichen/Vertragsabrechnung ab.
Der gesamte lokale Repositorytestlauf besteht mit93Tests; zusätzlich bestehen
die5historischen Analysetests. `native_status()` bleibt in dieser Offlineversion
unbedingt gesperrt; Callerflags oder synthetische Receipts schalten nichts frei.

## Geplanter wissenschaftlicher Vertrag, noch nicht freigegeben

Frage: Welchen xGD-Verlust verursacht das gemeinsame niedrige Startpaket und
verändert Standard/MoreOften-Pressing diesen Verlust? D00 bleibt fest; je32
neue unabhängige Seeds für high_press/deep_block, je2Seiten×4Arme,512Matches,
64unabhängige Seedblöcke. Keine D15-Übernahme oder neue Gegnerwahl.

Arme R00=10000/Standard, R10=7000/Standard, R01=10000/MoreOften,
R11=7000/MoreOften. Primär positiver Vorteil voller Schärfe
`F=(R00−R10+R01−R11)/2` auf xGD. Sekundär genauHolm8: F auf
Punkte/GF/GA/xGF/xGA; Pressing `(R01−R00+R11−R10)/2` auf xGD;
DoD `R11−R01−R10+R00` auf xGD und Punkte. Negative DoD bedeutet
größeren Schärfeverlust bei MoreOften. Ein Primärtestα0,05; keine gemeinsame
95-%-Absicherung über Primär- und Sekundärfamilie behaupten.

Erst Seitenmittel je Seed, Gegner je½, Welch-Satterthwaite-t und20.000
stratifizierte vollständige Seedblock-Resamples. Fehlende Arme sperren jede
wissenschaftliche Analyse. Praktisches Pilotziel0,30xGD, gewünschte volle
95-%-Breite≤0,50; tatsächliche SD unbekannt. Bei angenommener gemeinsamer
F-SD0,8/1,2/1,8 etwa0,400/0,600/0,900 volle Breite und84/50/26%Power für0,30
(Planungswerte aus MECH-Programmentwurf, keine neue Messung/Powergarantie).

Technik:16Gegner×Seite×Arm-Zellen zweimal=32Vollmatches/16A/A-Paare,
zusätzlich3negativeProbes(ungültiger Rohwert, unbekannte Profilfeld-ID,
beschädigte Binäreingabe). Grenzen gemeinsam über alle Phasen:
547Versuchsplätze,900sChild,1800s unverrückbareUTC-Frist,≤4Worker,
90sFortschrittsgrenze,2GiBprivateArtefakte/20GiBfreieReserve. Zentrale
NativeLease und Registry unverändert nutzen; ein Supervisor, nie gleichzeitig
ATTR. Ohne nativen Freigabepfad wurde bewusst kein ausführbarer Supervisor oder
pseudo-persistenter Budgetzähler als fertige Freigabe veröffentlicht.

## Erforderlicher nächster technischer Auftrag

Einen getrennten, reversiblen, quellgebundenen Host-/Runneradapter entwerfen:
Start-only-Zuweisung nach Originalvorbereitung mit belegter nativer Wirkung;
passive vollständige Profile und Original-Familiarityrecords unmittelbar
vor/nach Zuweisung sowie nach der ersten Fortschreibung, Tick/Clock/Identität
und unveränderte Kontrollen. Keine wiederholte Erzwingung. Default ohne opt-in
gegen historische Bytes **und** natürliche Ausführungsbelege vergleichen.
Neue Host-/Encoder-/Auditorhashes und Auswirkungen auf Originalvorbereitung
separat abnehmen; nötige Hook-/Setterarbeit ist kein beiläufiger Pythonfix.

Erst danach vollständigen wissenschaftlichen Vertrag/Analyse/konkrete Inputs,
zentrale neue technische und wissenschaftliche Seeds und persistente Budgets
registrieren/pushen, CI/Review/Technik bestehen, optional die512erSerie starten.
Keine automatische1024erErweiterung, Holdoutstudie oder Karrierefreigabe.
