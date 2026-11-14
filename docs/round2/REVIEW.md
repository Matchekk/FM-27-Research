# Runde2 – unabhängiger Implementierungs- und Preflightreview

**14.11.2026 · Code-/Offlineunterlagen zur Integration und zentralen budgetierten
Vorbereitung freigegeben. Keine native Rollen-, Profil-, Karriere- oder
SET-Messfreigabe durch diesen Review. Noch keine TACT-Ergebnisse vorhanden.**

## Umfang und tatsächliche Unabhängigkeit

Eigener Codex-Subagent, eigener Branch `codex/round2-review`, geprüft bis
Integrationsstand74c6841. AGENTS/Methodik und die relevanten Programmunterlagen,
Autorenmodule/Tests und konkreten Verträge wurden gelesen. Keine native Anwendung,
kein Serverimport, keine Seed-/Registryänderung oder Holdout-/Karriereausführung.
Der Director bleibt alleiniger nativer Supervisor. Die Versionsresource wurde
selbst rein lesend geprüft: File27.0.1/Product27.0.1+2503222, DLL-SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.

**86/86 Repositorytests selbst im Review-Worktree ausgeführt und bestanden**,
einschließlich tatsächlicher harmloser Pythonprozess-, Konkurrenz-, Crash-,
Timeout-, Budget-/Belegretentions- und Parser-Negativtests. Das ist kein
nativer End-to-End-Test und keine externe Replikation einer Matchstudie.

## Gefundene und nachgeprüfte Korrekturen

1. **SET-Wiederholungsnachweis:** Der erste Parser akzeptierte nach einem
   illegalen Kontakt eine legale Wiederholung mit `repeat_of=None`. Direkt am
   synthetischen Goldfall unabhängig nachgestellt. Fehlende Herkunft war damit
   nicht strikt verworfen. Korrigiert im SET-Folgecommit10e9247/main2680438:
   erster Kontakt ohne Vorgänger, jeder spätere genau auf den unmittelbar
   vorherigen illegalen Kontakt desselben Awards. Drei-Kontaktfolge und
   fehlende/übersprungene/fremde Links sind jetzt getestet; alle11 SET-Testmethoden
   selbst erneut bestanden. Synthetische Goldresultate bleiben unverändert.
2. **TACT-Leaseprovenienz:** Der erste Supervisor überschreibend schrieb einen
   Phasenleasebeleg, bevor der dauerhafte No-Retry-Gate griff. Ein abgewiesener
   Wiederholungsaufruf konnte dadurch alte Provenienz ersetzen. Korrigiert im
   Folgecommitdbf5f8f/main74c6841: vorher Active/Halted/abgeschlossenePhase und
   erhaltenen Beleg prüfen, dann exklusives `x`/fsync. Regression testet echten
   harmlosen Childlauf und danach bytegleichen alten Budget-/Leasebeleg ohne
   neuen Prozess. Alle10 TACT-Testmethoden selbst bestanden.

Keine dieser Entwicklungsprüfungen startete ein natives Match oder verbrauchte
Studienseeds. Beide Lücken wurden vor budgetierter nativer Vorbereitung behoben.

## VALID-003: geprüfter Stand und Grenzen

69Attribute korrekt getrennt: erste15 Positionsratings0..20,54 Abilityrohwerte
1..100.21 eigene Vektoren mit Rohinput-Tiers40/60/80 und deklarierten Boosts;
keine1–20-Anzeige-,CA-,Gleichstärken- oder Leistungsfreigabe. Geteilte DC-/DM-
Ratingfamilien und GK-Ausnahme werden explizit behandelt. Eigene aktive IP/OOP-
Familien werden vereinigt, nicht aus gleichen Slotnummern geraten.

Private Kontextdeskriptoren erhalten synthetisch getestete Kapazitäten26/18 und
Identitäten ohne23er-Trimming.256 ist eine defensive eigene Parsergrenze, keine
behauptete Enginekapazität. Öffentliche Ausgabe ist Hash-/Count-Whitelist.
Opake PKM-Bytes werden nur gehasht, tatsächliche Kapazität bleibtNone; kein
Decoder oder Karriere-Replayadapter wird als fertig behauptet. Der Soll-/Ist-
Comparator erkennt Missing/Mismatch und vergibt selbst bei synthetischem
Vollvergleich **keine** native oder Karrierefreigabe. Readerherkunft, originale
Vorbereitung/Managerzustände und passive Effektivitätswerte bleiben offen.

Der separate Lease-/DeadlineBudget-Testpfad lässt nur feste harmlose Python-
Children zu. Konkurrenz blockiert, Crashbelege bleiben, Timeout/Fehler und
verbrauchte Versuchsplätze verhindern Neustart. Er ist kein Ersatz für globale
Seed-/Zeitlimits alter Runner. Der neue TACT-Supervisor integriert dieselbe
Lease tatsächlich um den gesamten beaufsichtigten Childlauf.

## SET-V0: geprüfter Stand und Grenzen

Elf eigene synthetische Goldfälle, kontrollierte Periodenclock, finale Legalität,
eindeutige Award-/Ausführungs-/Schuss-/Toridentität,10s-Konterfenster und
Schusssnapshots für spätere Goal-/VAR-Nachrichten. Endstand wird reconciliert;
finale Schuss-xG-Zählbarkeit wird getrennt vom Goal-Storno verlangt. Doppelte
Auswahlansichten erhöhen keine Exposition, doppelte physische Kontakte scheitern.

Native Inputs bleiben hart `unresolved_native_mapping`, Exposition/Attribution
`null`, Freigabeflagsfalse. Ein caller-Flag kann diesen Stand nicht ändern.
Auch synthetische Erfolge erhalten keine native/performance readiness.
Echte Ausführung, Clockmapping, Schuss-xG/Besitz und Goldannotation bleiben
Vorbedingungen einer gesonderten SET-Messabnahme; keine Wirksamkeitsstudie hier.

## TACT-002-R0: Design-, Audit- und Budgetprüfung

Feste Reihenfolge R00/R10/R01/R11. ST-Koeffizienten(−½,+½,−½,+½),
AMC(−½,−½,+½,+½),physische DoD(+1,−1,−1,+1) korrekt. Ein PrimärtestST×xGD,
Holm7 sekundär genau AMC×xGD,DoD×xGD,ST×Punkte/GF/GA/xGF/xGA.
Seitenmittel innerhalb kompletter Seeds, feste Gegnergewichte je½, keine
512-fache Unabhängigkeit.32Seeds je Gegner ergeben64 unabhängige Blöcke und
512Matches.32technische Vollmatches/16A/A-Paare+1Negativprobe separat;67neue
Reservierungen, historische/failed/offene Seeds werden unter Allocationlock
geprüft. Neue unabhängige Seeds sind noch nicht durch diesen Codeaudit nachgewiesen;
die konkrete Reservation muss nach zentraler Vorbereitung erneut geprüft werden.

Eigene t-/nct-Nachrechnung bestätigt die vorab bedingten Breiten0,400/0,600/0,900
und Power≈84/50/26% für0,30 bei angenommenen SD0,8/1,2/1,8. Keine garantierte
90-%-Power und keine Nutzung einer kleinen P1B-SD als Rollenvarianz. Keine
Gewinnerwahl oder D15-Optimierung. Das volle2×2 ist ein Mechanismus-/Varianzpilot,
kein allgemeiner Karrierenachweis.

R00 wird gegen P1B-D00-Binärhashes geprüft; andere Eingaben erlauben ausschließlich
deklarierte kind4-IP-ST/AMC-Rollenrecords. Alle übrigen JSON-Felder müssen durch
Zurücksetzen der zwei Role-IDs wieder genau D00 ergeben. Rollen-/Positions-/Duty-
/PI-/Targets und beide Teams werden geprüft, native Rollenpresets nicht mit
zusätzlichen PI verwechselt. Nach Vorbereitung44Rollenzellen/44PI-Zellen/748PI-
Gruppen und alle69Attribute/1058Profilfelder plus wirksamer Seed/Naturabschluss.

**Zusätzliche echte Schemaprüfung:** Ohne Serverinitialisierung wurden vier
vorhandene erlaubte P1C-D00-Dumps (beide Gegner/Seiten) lesend mit dem neuen
`audit_contract` geprüft. Runtimekatalog-SHA256c08a8a… wurde abgeglichen und
OOP-Permutation direkt aus dem bestehenden Defaultdump abgeleitet. In jedem
Fall44/44Rollen/PI-Zellen und748Gruppen korrekt; `flags` ist eine dezimale
Zeichenkette, Targetfelder sindInteger. Dies belegt reale R00-Schemakompatibilität,
**keine** neue native Wirksamkeit der drei geänderten Rollenarme.

Dauerhafte Caps512Haupt/33Technik,900s Child/1800s festeUTC-Frist,max4Worker,
90s ohne Fortschritt,2GiB/20GiBReserve sind im Vertrag und Runner konsistent.
Lease hält gesamten Budgetchild einschließlich Vorbereitung/Probes; Worktree-
Nativestarts werden verweigert. Native Gates/Identitätsdrift stoppen, keine
Ersatzseeds/Retry/1024-Erweiterung. Vor Main prüft Code exakten erfolgreichen
CI-Commit des publizierten Technikberichts und unveränderte Techniksummary.

## Geprüfte Quellenhashes

SHA256 nach LF-Normalisierung, vor nativer Vorbereitung:

| Datei | SHA256 |
|---|---|
| research/validation003.py | `5c29945950e21ef183397b92d1cb8d09f38a300ef1de51d9b356f04bd956af1d` |
| research/coordination_testpath.py | `81d223ec2e2be5679cb2b8238db1e48a111c966fb3310a0b5acaaa14a573f7c3` |
| research/set_v0.py | `6c99824d5f7534011b84c9c82ca52c7a1a5212d21cb43b6a30c40f543827b290` |
| analysis/run_tact002r0.py | `f0b1323a84c552fc7c496c9f0d9ff42ea821a5e418ad498987d3eb281eab433a` |
| analysis/analyse_tact002r0.py | `f71ec48102c9ff3bde7c4f41e32d064601acc2c77aa139d0afcb02f8f5287563` |
| analysis/export_tact002r0.py | `5138b15147eb4f69f146f947a1f86b406bdd29628722a83bdbf3f7a2d8f80136` |
| experiments/TACT-002-R0-preregistration.md | `6e31a7df951072bce6ccee24edca84d4b749a13fea481cdb1ac4da09870b7a4e` |

## Freigabekette und ausstehende Ergebnissichtung

Director darf nach Integration/Tests die **budgetierte Vorbereitung** durchführen,
Konfiguration/Hashes/Seeds veröffentlichen und die technische Serie freigeben.
Vor dem ersten Hauptmatch müssen konkrete neue/disjunkte Seeds, alle16nativen
Zellen und16A/A-Paare/Negativprobe, echter Versions-/Hashkontext und veröffentlichte
Vorregistrierung/Code sowie Technikbericht mit erfolgreicher CI belegt sein.
Dieser Codeaudit überspringt keines dieser Gates.

`analysis/review_tact002.py` ist ein separater Reviewer-Rechenkern ohne Import von
Projektanalyse/Runner/`research.stats`. Er meldet bei fehlenden Resultaten ausdrücklich
noch keinen Leistungsbefund. Nach tatsächlicher zentraler Ausführung erfolgt
unabhängige Rohzeilenrekonstruktion aller8Kontraste/t-/Bootstrapintervalle,
Holm7,192Seedkontraste,Power-Minima und545Versuchsplätze einschließlich Lease/
Budgetprüfung. Erst danach eine Ergebnisfreigabe, keine vorgezogene Leistungsbehauptung.
