# VALID-003 – Offlinevorbereitung und separater Koordinationstestpfad

14.11.2026. **Keine neue native Simulation, Seedreservierung oder Karrierefreigabe.**
VALID-002 und historische Forschungsarchive bleiben unverändert. Diese neue
Vorbereitung ist kein bereits bestandener Profil-/Stärke-/PKM-Leistungsaudit.

## Fragestellung und Umfang

Erhalten unsere neuen Profilabsichten die tatsächlichen Skalen, Spielerbindungen
und Kapazitäten, erkennen sie fehlende native Readbacks und funktioniert ein
budgetierter Testsupervisor exklusiv und ohne Wiederaufnahme nach Crash/Timeout?
Die Prüfung ist technisch, nicht statistisch: kein Taktik- oder Trainingseffekt,
keine Powerbehauptung, keine Rangliste und keine Holdoutnutzung.

## Implementierte Schnittstellen

- `research/validation003.py`: eigene 69er-Vektoren für GK/IV/AV/DM/AM/Flügel/ST,
  je drei deklarierte Rohinput-Tiers; explizite15 Positionsratings und Vereinigung
  der tatsächlichen IP/OOP-Ratingfamilien. Links/rechts einer gemeinsamen Familie
  werden nicht künstlich als unabhängige Ratings geführt.
- `context_from_dump`: strukturelle private Deskription einer bereits vorhandenen
  nativen Dumpquelle. Tatsächliche Counts/Identitäten vollständig erhalten,
  kein23er-Zwang, kein Abschneiden/Auffüllen.256 ist lediglich eine defensive
  Parserobergrenze, keine Behauptung über die maximale Enginekapazität.
- `bind_profiles`: eigene Profilabsichten nur bei genau passender nativer
  Spieleranzahl und Reihenfolge binden. Roh-IDs bleiben privat.
- `public_context`: feste Hash-/Count-Whitelist, keine Spieler-IDs, Namen,
  Pfade, Attributearrays oder Dumpbytes. Keine Replayfreigabe aus Strukturprüfung.
- `audit_readback`: vollständige Soll-/Ist-Attribute,23 Profilfelder und Pflicht-
  Evidenceflags vergleichen. Fehlend bleibt `missing`, Abweichung `mismatch`.
  Ein synthetischer Vollvergleich darf `passed=true` liefern, aber ausdrücklich
  weiterhin `native_validation_granted=false` und `career_replay_released=false`.
  Der Comparator ist kein Decoder und keine unabhängige Herkunftsverifikation.
- `research/coordination_testpath.py`: unveränderte `NativeLease` hält die
  Exklusivität über `DeadlineBudget.run` für **feste harmlose Pythonchildren**.
  Keine beliebigen Kommandos, kein FM-Host, keine Registry.2Versuchsplätze,
  30s Child-/60s UTC-Defaultcap; Crash/Fehler/Timeout bleiben dauerhaft sichtbar.
- `analysis/run_valid003_offline.py`: eigener privater Ausgabepfad,21Profilvektoren,
  zwei festgelegte Python-Probes, Hashreport. Vorhandener Ausgabepfad wird
  abgelehnt; kein Reset oder Überschreiben eines früheren Laufs.

## Skalierung und eigene Profile

Der geprüfte Windowsserver validiert (`validate_scenario`, Zeile208) die ersten
15Attribute als0..20, die übrigen54 als **native1..100-Rohwerte**. Deshalb sind
unsere Tiers low/medium/high **40/60/80 Rohinput**, ausgewählte positionsbezogene
Fähigkeiten erhalten+10 (Cap100). Körper-/CA-/Anzeigeeinheiten werden daraus
nicht hergeleitet. Gemeinsame Stufe ist keine empirisch gleiche Mannschaftsstärke.
InjuryProneness/Dirtiness/mehrere weitere Kontextfähigkeiten bleiben60, damit ein
„höherer“ Tier nicht zugleich diese Felder erhöht. Konkrete Indizes und eigene
Vektoren sind im ausführbaren Modul vollständig benannt.

GK besitzt GK20/sonstige Positionsratings0. Feldspieler: GK/Sweeper0,
aktive IP/OOP-Ratingfamilien20, sonstige Feldfamilien1. Die Stufe1 ist ein
kontrollierter extremer Sensitivitätskontext, kein empirisch realistischer
Karriere-Kader. Beispiel DM: DMR/IP und MC/OOP → Familien5/7, beide20.
Die Zuordnung setzt voraus, dass der künftige Adapter dieselbe Spieleridentität
unter dem tatsächlichen seitenabhängigen OOP-Slotmapping ermittelt. Das Modul
errät diese Bindung nicht aus gleichen Slotnummern.

Ein erster Offlineentwurf begrenzte alle69 Werte irrtümlich auf20; eine vorhandene
P1C-Dumpquelle wurde deshalb vor jeder neuen nativen Aktion abgelehnt. Die reine
Quellprüfung klärte die getrennten Skalen. Der korrigierte Regressionstest nutzt
auch die öffentlich dokumentierte eigene P1B/P1C-Profilregel (Abilityrohwerte60).
Keine historischen Werte geändert, keine native Fehlpartie und kein Ersatzseed.

## Tatsächlich geprüfte vorhandene Quelle

Historischer **Bundled-Fixture-Dump**, keine gespeicherte Karrierepartie:
`tech-deep_block-0-D00-r0` aus P1C. Der vorhandene private Eingabedump wurde
rein lesend gegen den veröffentlichten `input_dump_sha256` abgeglichen:
`05dc1ecba20f62a4c3d7f7bf9a31523333866c73045d1fb727913e972dd8015f`.
Beobachtete native Counts23/23, jeweilige Listen exakt23. Dies belegt nur diese
alte Dumpquelle. Es ist weder eine neue V3-Profilfreigabe noch eine unabhängig aus
PKM-Bytes ermittelte Karrierekapazität.

Bundled-PKM60314Bytes, SHA256
`39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6`.
`inspect_pkm_file` liest ausschließlich Bytes für Fingerprint/Größe; Kapazität und
Teams bleiben explizit `null`. Der vorhandene eigentliche PKM-Reader benötigt
NativeHost `--inspect-fixture`. Der Saved-Fixture-Pfad kann ebenfalls native
Probes starten. Deshalb kein Import des Servers und kein vermeintlicher reiner
Python-Karriere-PKM-Decoder in diesem Teilauftrag.

## Provenienz und tatsächliche Version

Lokale DLL-Dateiversion27.0.1, Produkt27.0.1+2503222 rein lesend abgefragt.
Toolstand v1114.6, Commit91f2eba57fac0b7fbd3dff616056907e3ce461be.
Quellbytes SHA256:

| Quelle | SHA256 |
|---|---|
| fm27_tactics_server.py | `5f2be140f30d576872351e7c397102b0b5a3de7d0b05f8d4e5011a65e94ea590` |
| fm27_profiles.py | `28f163f21c9aa80e9323e9b245127c3c48958218c1337cddb6ac6aae399c511f` |
| desktop_saved_fixtures.py | `2d4ca1b03e1f120cda3be8c270ab40b54bee7b0e1847dfbfd7363f36c8cf1e9b` |

[Server](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_tactics_server.py),
[Profile](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_profiles.py),
[Saved-Fixture-Pfad](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/desktop_saved_fixtures.py).
Keine Upstream-/Runtime-/Spieldatei verändert oder veröffentlicht.

## Koordination, Tests und reale Laufzahlen

Tests mit separaten Tempverzeichnissen, niemals mit `local/global-native` des
aktiven Forschungsauftrags. Ein echter zweiter Pythonprozess blockiert den Probe-
start **vor Budgetinitialisierung**. Ein abrupt beendeter Python-Supervisor lässt
Lease und aktives Budget blockierend zurück. Ein echter Python-Sleepchild wird
am festen Budget abgebrochen; Versuch zählt weiter und der Studienzustand haltet.
Fehlende/mehrfache Jobs, geänderte Limits, weitere Versuche nach Cap/Fehler und
Worker5 werden abgelehnt. Ein Neustart erstattet keine Zeit oder Versuchsplätze.

Neue gezielte Tests:8Profil-/Kapazitäts-/Readbackfälle und5Koordinations-/Budgetfälle.
Die vollständige lokale Repositorysuite besteht mit65/65 Tests.
CLI tatsächlich ausgeführt:21eigene Vektoren,2harmlose Pythonchildren,0native
Prozesse,0Seedreservierungen. Child-Zeit0,080s für den separaten Positivpfad
(lokale Messung, kein Enginebenchmark). Unit-Tests lösen zusätzliche harmlose
Pythonprozesse für Konkurrenz/Crash/Timeout aus, keine FM-Prozesse.

Reproduktion ab Repositorywurzel:

```powershell
python -m unittest discover -s tests -p test_validation003.py -v
python -m unittest discover -s tests -p test_coordination_testpath.py -v
python analysis/run_valid003_offline.py --output local/valid003-offline
```

Die CLI verweigert denselben bereits benutzten Ausgabepfad. Für eine **neue
separate Offline-Testinstanz** einen eigenen Pfad wählen, nie Zähler löschen.
Dies gilt nicht als Erlaubnis für Retry/Neueinstieg einer nativen Studie.

## Vor Freigabe weiterer Forschung

- **ATTR:** Profilmasken und erlaubte69er-Diffs einfrieren; GK/aktive IP/OOP-
  Familien konstant, Uniform-/Executionüberschreibung ausschließen. Passive
  Effektivitäts-/Suitabilitykomponenten fehlen weiter. Neue native Audits nötig.
- **MECH:** eigener opt-in Startpolicy-Encoder samt Runner/Auditor; gewöhnlicher
  Normalisierer überschreibt Fitness/Schärfe erneut. Eigene reine Struktur-
  /Rohwertvalidation ist keine wirksame7000-Startintervention.
- **TRAIN:** Karriere-RNG-Streams oder echte unabhängige Save-/Clubcluster,
  tatsächliche Kalender-/Teilnahme-/Verletzungsreceipts und Einheitenkalibrierung.
  Der bestehende Checkpointimport ist kein Karriereexecutor.
- **PKM:** kapazitätsgebundene native Quelle/Identität, Fixture-/Dump-/Readerhashes,
  Originalscore/Manager-/Phasen-/Startkontext und Nach-Vorbereitungsreadbacks.
  Unsere Deskriptoren stellen fehlende Evidenz dar, lösen diese Gates nicht.

TACT integriert NativeLease direkt um seinen neuen Supervisor im gemeinsamen
zentralen Leasepfad. Diese Offlineintegration ändert keinen historischen Runner
und keine Seedregistry. Alle tatsächlichen Seedallokationen bleiben beim Director
unter gemeinsamer Registrylock; privateIDs/Rohmaterial werden nicht veröffentlicht.
Nach unabhängiger Prüfung und zentraler CI integrieren/pushen. Kein eigener
nativer Folgeversuch durch VALID, keine Karriere-Replayfreigabe.
