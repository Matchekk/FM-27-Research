# Runde2 – Agent SET: SET-V0 Offlineimplementierung

14.11.2026. Exklusiver Branch `codex/set-v0`, eigener Worktree; Startstand790727f.
**Native Starts0, neue Seeds0, keine Registry-/Runneränderung, keine Karriere-/
Holdoutzugriffe.** Lokaler geprüfter Commit wird zentral vom Director integriert;
dieser Agent pusht nicht. Historische Daten/Vorregistrierungen bleiben unverändert.

## Konkretes Ergebnis

Implementiert: [research/set_v0.py](../../research/set_v0.py), ein eigenständiger
strikter Offlineparser, [10 Testmethoden](../../tests/test_set_v0.py) mit
[elf eigenen Goldfällen](../../data/set-v0/gold-cases.json),
[Messvertrag](../../experiments/SET-V0-measurement.md) und
[Capabilitymanifest](../../data/set-v0/capabilities.json).

Die Nativeboundary bleibt hart blockiert: native Inputs liefern
`unresolved_native_mapping`, `exposures=null`, `attribution=null`,
`native_validated=false,performance_ready=false`. Es gibt keinen Parameter
`validated=true`, der diese Grenze umgeht. Mutieren eines erhaltenen
Capabilitydicts verändert keine Implementierungsfreigabe. Auch vollständige
synthetische Erfolgsfälle erhalten keinerlei native-/Leistungsfreigabe.

## Frage, Quellen und echte lokale Bestandsprüfung

Technische Frage: vollständige normalisierte Kontakte, finale Legalität,
Schuss-/Torstatus und kontrollierte Besitzketten ohne Doppelzählung auswerten.
Die geschützte Runtime wurde nicht importiert und kein Host gestartet.
DLL-Versionresource lesend File27.0.1/Product27.0.1+2503222;
SHA2568c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340.
Upstreamquellkopie tatsächlich auf Commit91f2eba57fac0b7fbd3dff616056907e3ce461be,
freigegebener Toolstandv1114.6. Quellenbytehashes und zulässige Gapdiagnostik
stehen in [native-source-gap.json](../../data/set-v0/native-source-gap.json).

Direkt gelesene Primärquellen dieses exakten Commits:

- [Host: Auswahlzustände](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/desktop_host.cpp#L847): Routinekey wird pro Team dedupliziert; kein nachgewiesener Kontakt-/Ausführungszähler.
- [Tor-/Kartencollector](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_match_events.py): vorhandene Goal-/Card-Reconciliation ist kein vollständiger Schuss-/Besitz-/SET-Mapper.
- [Episodenmodus](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_setpiece_episode.h): Deadball-/Fensterbeobachtung ist keine Goldvalidierung tatsächlicher Ausführung oder standardbezogener xG.

Zwei frühere erlaubte VALID-002-Full-event-Logs erneut rein lesend geprüft:
112/122Zeilen, je52 Auswahlmeldungen an26Ticks; beide gehören zur gleichen
Seed-/0:0-Konstellation. Die SHA256 stimmen mit dem früheren SET-Bericht überein.
Kein Zähler echter Ecken, keine geschätzte Expositionsrate und keine unabhängigen
Replikate daraus abgeleitet. Rohmaterial/Spieleridentitäten bleiben privat.
Andere Programmunterlagen und Independent Review wurden berücksichtigt.

## Vertrag, Zustandslogik und Testabdeckung

Alle Felder, Clock und Grenzregeln im [Vertrag](../../experiments/SET-V0-measurement.md).
Nur eigener Syntheticnamespace akzeptiert berechnete Werte. Neue native Quellen
brauchen später vertrauenswürdiges gehashtes Schema-/Source-/Clockmapping und
unabhängige native Goldfallabnahme; V0 besitzt dafür keinen Freigabeschalter.

Elf manuell erwartete Goldfälle prüfen: keine Situation; Auswahl ohne Ausführung;
Repetition mit nur einem legalen Kontakt;10s-Kontergrenze; nächster Standard;
VAR-Storno bei weiter gültigem Schuss-xG; final nicht gezählter Offside-Schuss;
Periodenwechsel; Rückeroberung; Eigentor ohne erfundenes Schuss-xG; gleiche Routine
in zwei verschiedenen legalen Situationen. Doppelte Offensiv-/Defensiv-Auswahl
bleibt Diagnose; doppelte physische IDs scheitern geschlossen. Ein zukünftiger
Rawmapper muss Kontaktidentität belegen, statt Routinehash/Tick als ID zu erraten.

Konterfenster[Besitzwechsel,Besitzwechsel+10s), genau10s ist außerhalb.
Schuss-Snapshot bewahrt Attribution bei späterem Torregister-/VAR-Eintrag.
Eigene/defensive Expositionen und xG/Tore sowie Gegenkonter werden getrennt
aggregiert; keine Doppelattribution. Original-XG und finale XG-Zählbarkeit sind
getrennte Pflichtfelder; ein Goal-Storno ändert nicht automatisch das Schuss-XG.

Negative Fälle lehnen unbekannte/fehlende Felder, unsafeIDs, Clockregression,
fehlenden Perioden-/Matchabschluss, offene Awards, fehlenden Kontakt/finale
Legalität, falsche Wiederholungslinks, unkontrollierte Besitzerannahmen,
Missing/NaN/Inf/ungültiges xG, fehlenden finalen Schussstatus, widersprüchliche
Tore/Endstände und ungültige VAR-Verweise ab. Keine stillen Nullersetzungen.
Reguläre Open-Play-Ereignisse bleiben unzugeordnet und der Gesamtendstand geprüft.

## Tatsächliche Tests und Ressourcen

```powershell
python -m unittest discover -s tests -p test_set_v0.py -v
python -m unittest discover -s tests -v
```

Zehn SET-Testmethoden bestehen mit elf Goldtraces und den beschriebenen negativen
Varianten. Gesamtsuite im eigenen Worktree:62 Tests bestanden (52 bestehend+10neu).
Die Tests importieren weder nativen Server noch Host. Reale Belege nur lesend.
Keine neue Match-, Power- oder Routineeffektmessung; Nativebudgetverbrauch0.
Native Goldfall-/Expositionsabnahme bleibt offen. Zentrale CI/Independent Review
folgen nach Integration, nicht durch diesen lokalen Teilauftrag behauptet.

## Grenzen und nächster konkreter Auftrag

Dies ist ein Parser für explizite synthetische Evidenz, kein implementierter
validierter FM-Ausführungsextraktor. Die Pflichtfelder können aus den alten
Selektionslogs nicht erzeugt werden. Daher keine Standard-Wirksamkeitsstudie,
kein Raten-/Clusterbootstrap und keine fiktive90-%-Power.

Als nächstes gemeinsam mit VALID passives Originalmapping spezifizieren:
Ausführungskontakt+finale Legalität, periodenkalibrierte Clock, kontrollierter
Besitzwechsel, ursprüngliches/final gezähltes Schuss-xG und Goal/VAR-Identität.
Versionierte Mapping-/Gatehashes und unabhängig annotierte positive/negative
native Goldfälle vor jeder neuen Freigabe. Fehlende Ereignisklassen blockieren
zugehörige Behauptungen; keine zusätzlichen Seeds durch Nachsuchen erzwingen.
Erst danach ein gesonderter technischer Nativevertrag und später SET-002-R0.
