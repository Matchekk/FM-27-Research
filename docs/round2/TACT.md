# Runde2 – AGENT TACT Implementierungsbericht

TACT-002-R0 ist als eigener kleiner512-Match-Runner vorbereitet,nicht in diesem
Worktree nativ ausgeführt. Getrennter Branch `codex/tact002-r0`,historische Quellen
unverändert. Vollständiger2×2-CF/DLF×AttackingMidfielder/SecondStriker.
D00bleibt Instruktions-/Profil-/OOP-Baseline,keine D15-Optimierung/Holdouts.

Neue Dateien: `analysis/run_tact002r0.py`, `analyse_tact002r0.py`,
`export_tact002r0.py`, `verify_tact002r0.py`, `report_tact002r0.py`,
`tests/test_tact002r0.py` und die experimentbezogene Vorregistrierung.
Keine Änderung bestehender öffentlicher APIs,keine neue Dependency.

Architektur: zentrale prepare/register/technical/main-Phasen; eigene normale
NativeLab-Anbindung ohne Upstreamänderung. R00binäridentisch zu P1B-D00,
Varianten nur kind4-ST/AMC-IP-Rollenrecords. BeideTeams/Phasen und alle44Rollen-
/Dutyzellen/748PI-Gruppen/Targets auditiert,IntrinsicRolepresets nicht mit PI0
verwechselt. Neue NativeLease integriert um den ganzen beaufsichtigten Childlauf;
Worktrees dürfen nicht nativ starten. Dauerhafte900sChild-/1800sUTC-Grenzen,
512main/33techVersuche,max4Worker,90sFortschrittstimeout,keine Retries/Ersatzseeds.

Wissenschaftlich: ST-Haupteffekt xGDprimär,exaktHolm7Sekundärpaare,
physische Koeffizienten und vollständige64Seedblöcke,Seitenmittel und feste
Gegnergewichte.20000Blockbootstrapziehungen,Kontextvarianz/LOO und bedingte
neue Fallzahlen. Keine Gewinnerwahl oder Karrierebestätigung.

## Tatsächliche Offlineprüfungen

Zehn fokussierte Tests bestehen: physische Haupt-/DoD-Skalierung gegen bekannte
synthetische Effekte,fehlende/duplizierte/driftende Readbacks,erlaubte Binärdiffs,
Rolleneligibility/D00-Reinheit,PI-Fehler auch im anderen Team/OOP,32Technikjobs/
16Paare,Leasekonkurrenz/Budgetretention und öffentliche Export-Whitelist und CI-Bindung an den exakten technischen Freigabecommit.
Keine nativen Anwendungen,Serverimports,Seedreservierungen oder Registrywrites.
Vollständige Repositorytests62/62 und historische Analysetests5/5 bestanden vor Übergabe. Neuer Verifier meldet erwartungsgemäß noch keine registrierte Studie.

## Zentrale Befehle nach Review/Integration

Mit vorhandenem Rootvenv,aus Hauptcheckout `D:/FM Research`,ausschließlich Director:

```
python analysis/run_tact002r0.py prepare
# erzeugte Inputs/Rollenmanifest/Seedplan/JSON-Vertrag prüfen,committen/pushen,CI
python analysis/run_tact002r0.py register --commit <published-preregistration-sha>
python analysis/run_tact002r0.py technical
python analysis/export_tact002r0.py
#32Vollmatches/16A/A/Negativkontrolle prüfen,Gatebericht committen/pushen,CI
#data/tact-002-r0/technical-gate.json braucht passed:true,published_commit und ci_run
#ci_run muss completed/success mit exakt diesem headSha sein; gh wird geprüft
python analysis/run_tact002r0.py main
python analysis/export_tact002r0.py
python analysis/verify_tact002r0.py
python analysis/report_tact002r0.py
```

Vor erster prepare muss Code und Analyse vollständig reviewed sein,da dabei die
festeUTC-Frist beginnt. Keine Entwicklung während knapper Restdeadline.
Kein Wiederholungsversuch bei Gatefehler. Nach prepare hat das Repository zehn
specJSONs: zentrale harte Testzählung in `tests/test_platform.py` gezielt anpassen,
nicht als Änderung historischer wissenschaftlicher Verträge.
Root muss Readme/Researchlog/Finding/Roadmap/CI und tatsächlichen technischen
Gatebericht nach gemessenen Ergebnissen ergänzen; diese Zuständigkeiten liegen
außerhalb dieses Agentenbereichs. Kein eigener Push oder nativer Leistungsclaim.

## Reviewkorrektur vor Veröffentlichung

Der unabhängige Reviewer fand einen Provenienzfehler: eine neue abgewiesene
Phasenwiederholung konnte den alten Leasebeleg vor dem No-Retry-Gate ersetzen.
Der neue Supervisor prüft abgeschlossene/aktive/abgebrochene Phasen vor jeder
Leasebelegmutation und legt Belege exklusiv mit flush/fsync an. Retain-/Crash-
belege bleiben blockierend. Regressionstest führt einmal einen gewöhnlichen
Pythonchild aus und beweist anschließend unveränderte Budget-/Leasebytes sowie
keinen weiteren Childstart bei abgeschlossener oder zurückbehaltener Phase.
Keine nativen Prozesse, Registryaktionen oder neuen wissenschaftlichen Seeds.
