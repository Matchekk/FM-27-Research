# NIGHT-002 – unabhängige Ressourcen- und Sicherheitsprüfung

14.11.2026 · statische Prüfung und Offline-Tests, keine nativen Aufrufe durch den
Validation Agent. Ausgangsstand `062fa7e3bfc129d61c28b112b71bf7f54fc4123f`.

## Identität tatsächlich erneut geprüft

Die installierte DLL meldet über ihre Windows-Dateimetadaten ProductVersion
`27.0.1+2503222`, FileVersion `27.0.1`. Die folgenden Dateien wurden erneut
gelesen und gehasht; dies ist keine neue native Kompatibilitätsprüfung.

| Artefakt | SHA256 |
| --- | --- |
| installierte `game_plugin.dll` | `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340` |
| unveränderter Observerhost | `58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32` |
| ursprünglicher Simulatorhost | `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e` |
| gebündeltes Fixture | `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6` |
| neu berechneter Ressourcenfingerprint | `6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883` |

Der lokale ursprüngliche Upstream-Checkout steht auf
`91f2eba57fac0b7fbd3dff616056907e3ce461be` (v1114.6). Runtime-Quellkopien haben
kein eigenes Git-Repository; ihre Identität muss über die einzeln eingefrorenen
Quellhashes geprüft werden. Ein `git -C runtime/source rev-parse` würde sonst das
übergeordnete Forschungsrepository melden und ist kein Upstreamnachweis.
Die Projektumgebung enthält Python3.12.10, NumPy2.3.5 und SciPy1.16.3. Der einfache
Systemaufruf `python` besitzt NumPy nicht; Tests und Analysen verwenden die
Projekt-venv. Kein Paket wurde dafür verändert.

## Mission strikt getrennt

Die alten Dateien `research/night_control.py` und `analysis/night_supervise.py`
bleiben unverändert. Sie binden NIGHT-001 an23:00UTC und1800Childsekunden und
dürfen weder umetikettiert noch mit verlängerten Fristen geöffnet werden.
Der alte MECH-003-STAMINA-R0-Budgetbeleg enthält einen ausdrücklichen terminalen
administrativen Stopp. Seine Reservierungen bleiben verbraucht; Main wurde
damals nicht gestartet. Das abgeschlossene MECH-002-Paket wird nicht fortgesetzt.

NIGHT-002 erhält eine neue globale Datei unter
`local/night-002/program-budget.json`, eine eigene Tokenvariable und ausschließlich
die neue erlaubte Route MECH-004-SPLIT-R0. Die globale Begrenzung ist2048Main,
192technische Plätze,3600kumulierte beaufsichtigte Phase-Childsekunden und eine
unveränderliche absolute Frist `2026-11-15T07:00:00+00:00`. Negative Abweisungen
werden konservativ ebenfalls als technische Plätze gezählt. Der technische
Studienvertrag ist enger:33Plätze/512Main/900Childsekunden/5400UTCsekunden.

Die geerbte Zeitdefinition berechnet die vollständige Laufzeit des beaufsichtigten
Phasenprozesses einschließlich Pythonvorbereitung und Audits. Vier parallele
Engineaufrufe zählen darin als parallele Zeit, nicht als vierfach aufsummierte
CPUzeit. Summierte Einzelaufrufzeiten müssen gegebenenfalls zusätzlich ausgewiesen
werden; sie dürfen nicht mit dem ausdrücklich dokumentierten Ledgerwert
verwechselt werden.

## Wiederverwendete Sicherheitsgrenzen

- `NativeBudget` reserviert vor Ausführung exklusiv; belegte Operationen, Seeds
  und Jobkeys werden nicht zurückerstattet. Ein unterbrochener oder fehlgeschlagener
  Prozess sperrt weitere Admissionen.
- `NativeLease` verwendet weiterhin denselben gemeinsamen Ort
  `local/global-native`. Die Lease ist eine Kooperationssperre, keine eigene
  Betriebssystembegrenzung. Ein anderer Besitzer wird niemals automatisch entfernt.
- `ColdScheduler` zählt maximal vier gleichzeitig zugelassene Aufrufe. Der
  unveränderte Host erlaubt je Aufruf nur einen Engineprozess; das ist ein
  geprüfter Prozessgrenzbeleg, kein gemessener PID-Peak.
- `native_process005.contained_call` ordnet die zunächst wartende Pythonkapsel
  vor Freigabe des Hoststarts einem Windows-Jobobjekt zu. Limit3, Kill-on-close,
  kein Breakaway,90Sekunden Fortschrittswatchdog und explizite Gesamtdauer.
  Eine bestätigte Bereinigung verlangt Kapselende und Kernelprozesszahl null.
- Die Studienlease bleibt bei offenem Budget, Pendingmarker oder unbestätigter
  Bereinigung erhalten. Es gibt keinen automatischen Takeover.
- Frische fehlende Cachepräfixe vor Projektimports vermeiden alte Bytecodeimporte;
  readonly Windowshandles schützen Host, Fixture und eingefrorene Eingaben während
  der Phase. Es werden keine fremden Runtimequellen importiert, um dort Code zu starten.

Alle neuen privaten Studienartefakte liegen im gemeinsamen Missionsbaum.
`check_artifacts` prüft dessen Gesamtgröße vor Admissionen, lehnt Symlinks,
Reparsepunkte und Pfadflucht ab und sperrt ab4GiB. Die neue Studie besitzt zusätzlich
2GiB und20GiB freien Plattenplatz als engere Bedingungen. Diese Größenprüfung
ist eine Admission-/Nachkontrolle, keine Betriebssystem-Diskquota; tatsächlich
erzeugte Bytes sind im Ergebnisbericht auszuweisen.

## Offline-Abnahme des neuen Controllers

`tests.test_night002_control`: neun Tests bestanden. Geprüft sind feste Frist,
neue Missionsidentität, Ablehnung alter Budgets, unveränderte Caps beim Wiederöffnen,
keine Rückerstattung/Retry, authentifizierter lebender Elternprozess, exakte
geordnete Keylisten, getrennte NIGHT002-Tokenvariable, globale Artefaktsumme,
genau32+1Technikkeys und64vollständige Mainblöcke sowie Ausschluss alter Routen
und nativer Preparephasen. Weitergereicht werden ausschließlich exakte
Publikations-SHA-/CI-Argumente; insbesondere keine abgekürzten Child-Schalter.
Tests verwenden temporäre Dateien und Mocks;
kein Test startete einen nativen Host.

Der Director prüft diese Controllerdateien unabhängig. Der Validation Agent
prüft separat den neuen Studienrunner und konkrete Inputs, bevor native Technik
freigegeben werden darf. Dieses Dokument allein ist keine Ausführungsfreigabe.

## Bekannte konservative Grenze

Ein nicht erfolgreicher Phasenprozess setzt derzeit das globale NIGHT-002-Ledger
auf `halted`, auch wenn ein einzelner Studienfehler technisch sauber bereinigt
wurde. Damit können weitere unabhängige Studien strenger als im Nutzerauftrag
blockiert sein. Es gibt bewusst keinen ungeprüften Budgetreset oder generellen
Fehlerbypass. Ein anderer Pfad würde eine eigene vorab geprüfte Admission für
bereinigte terminale Studien erfordern. Die betroffene Studie darf dadurch
keinesfalls wiederholt oder umbenannt werden.

Keine Karrieredatei, Spieluhr oder UI wurde bedient. Private Ressourcen, Dumps,
Pfade mit Personenbezug und Zugangsdaten gehören nicht zur Veröffentlichung.
