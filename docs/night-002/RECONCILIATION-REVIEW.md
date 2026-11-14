# NIGHT-002 – unabhängige Prüfung der administrativen Fortsetzung

15.11.2026 Europe/Berlin · Directorreview, getrennt vom Autor des neuen
Controllers. **Akzeptiert ausschließlich für die unabhängige TACT-003-Frage**
nach Veröffentlichung und erfolgreicher exakter CI; keine MECH-004-Fortsetzung.
Die [unabhängige Rohabschlussprüfung](SPLIT004-TERMINATION-REVIEW.md) zertifiziert
Bereinigung und erhaltene Belege, keine neue native Studienfreigabe.

| Geprüfte LF-Quelle | SHA256 |
| --- | --- |
| `research/night002_control.py` | `c4c34528041fc6e8ceb9a5ae4cc868cd977518b3863ce845f27826adcf13542f` |
| `analysis/night002_supervise.py` | `278b0d515180f902f3e53fa419037f10bf8f0ef7a43dcf900cdac23ec1489522` |
| `analysis/reconcile_night002.py` | `2d7189ba9ad8a84637e886b678616450829247f967d0054fae764c4b17b00487` |
| `tests/test_night002_control.py` | `0c8ac739eb676430b49107a0bc3efdeb31b18b08bc694f271825f5a27a0be24a` |

Die Transformation akzeptiert nur den exakten bisherigen globalen SHA256
`dad11f1be95f9bbccff8e9b62079d943af63cbd3828790e96f07809986bad114`,
589,7353507000007 belastete Sekunden,545 vorhandene Reservierungen und die
unveränderten beiden ursprünglichen Operationen einschließlich Fehlreturncode.
Caps, Frist, Seed-/Jobbelegung und alle früheren Zeitwerte werden vollständig
beibehalten. Nur die administrative globale Haltesperre wird für den anderen
Studienpfad aufgelöst; neue Metadaten dokumentieren diese einmalige Transition.
Der eigene MECH-004-Etat bleibt bytegleich `halted`. Beide Admissionebenen
verbieten MECH-004 in dieser neuen Epoche **unbedingt**, auch bei fehlender
Terminal-Metadatenliste; die einzige äußere Route ist TACT-003-STLESS-R0.

Vor Mutation verlangt die CLI veröffentlichte unveränderte Quellen/Abschluss-
belege und eine erfolgreiche CI desselben vollständigen Commits. Sie prüft
erneut alle257 Kernelbereinigungen, private Artefakthashes,1024 restaurierte
Archivdateien, fehlende Pendingmarker/Lease und die eigene alte Haltesperre.
Eine gemeinsame Budgetlockdatei verhindert konkurrierende Operationen.
Unveränderlicher Vorher-Snapshot und Receipt mit Vorher-/Nachher-SHA werden
**vor** atomarer Zustandsänderung geschrieben. Ein abgebrochener Versuch ist
nicht automatisch wiederholbar. Keine Rückerstattung oder neue Reservierung
geschieht in dieser Funktion; sie startet keinen nativen Prozess.

Die Rohabschlussfreigabe und diese Administration ersetzen nicht die getrennten
TACT-Input-/Runner-/Technik-/Main-/Publikationsgates. Die Nutzerautorisierung,
nach einem betroffenen Stopp andere unabhängige Fragen weiterzubearbeiten,
ist der Handlungsrahmen; sie erlaubt keinen Retry desselben Versuchs.

Vierzehn Controllertests durch den Director geprüft/ausgeführt:13 bestanden,
ein Windows-Symlinktest wegen fehlender lokaler Berechtigung übersprungen.
Der neue Scandir-Zähler prüft Root und alle Einträge auf Symlinks/Reparsepunkte
vor Traversierung, folgt keinen Links und zählt weiterhin sämtliche tatsächlichen
Missionsdateien. Lexikalisch stammen alle Einträge aus bereits geprüften
Elternverzeichnissen; einzelne verschwindende Pendingmarker brauchen keine
fehleranfällige Windows-Auflösung mehr. Read-only-Benchmark bei identischen
146.920.935Bytes:0,633s gegenüber0,013s. Keine weitere Livearchivierung.

Keine tatsächliche globale Zustandsänderung bei Verfassen dieses Reviews.
