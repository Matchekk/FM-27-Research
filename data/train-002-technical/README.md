# TRAIN-002 technische Diagnosen – Runde3

`archive-diagnostic.json`: offline aus allen660öffentlichen TRAIN-001-Zeilen und
Manifest/Kalender/A-A rekonstruiert. Neue deskriptive Kontrollrechnung, keine
neue Trainingsstudie. Unbekannte Teilnahme, Ausfalltage, Kalibrierung und
unabhängiges Treatment-n sind `null`, nie0.

`reader-inventory.json`: tatsächliche statische Inspektion des installierten
fmsave0.9.0. Nur eigene Metadaten/Quellhashes/Signaturen, kein Paketquelltext,
kein Save, keine Namen/Quell-IDs/privaten Pfade. Keine erfolgreiche Saveauslese
oder native Kompatibilität behauptet. Der frühere Reader0.10.0 ist dadurch
nicht erneut ausgeführt oder als identisch bestätigt.

Reproduktion ohne Simulation:

```powershell
python analysis/audit_train002.py
python analysis/inspect_train002_reader.py
python -m unittest discover -s tests -p test_training002.py -v
```

Für neue Ausgabedatei `audit_train002.py --output data/train-002-technical/NEU.json`;
CLI überschreibt keine vorhandenen Dateien. Plattformabhängige CRLF-Dateibytes
können andere Quellhashes ergeben; die Diagnosen dokumentieren die tatsächlich
gelesenen lokalen Bytes und nicht eine behauptete plattformübergreifende SHA.
Synthetische Testdaten entstehen nur temporär, sind ausdrücklich synthetisch und
schalten keine Karriere-/native Freigabe frei.

Alle neuen Artefakte:0nativeMatches,0Kalenderadvances,0Seeds. Kein Holdout gelesen.
Siehe [technische Grenzen](../../experiments/TRAIN-002-technical-round3.md).
