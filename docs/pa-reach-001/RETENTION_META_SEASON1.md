# Beobachtete Meta-Entwicklung bis zum ersten Saisonstichtag

Vom 30.04. bis 30.06.2027 gewannen **acht der 15 auswertbaren Jugendfeldspieler** im Retentionszweig an gespeicherter CA. Zwei dieser acht Spieler blieben im Meta-v2.1-Index gleich, bei einem sank der Index. Die Jugendgruppe war vorab über 16 stabile Identitäten gebunden. Ein Torwart fällt außerhalb des Feldspielerindex. Für die übrigen 15 lagen an beiden Tagen dieselbe Bewertungsposition und alle zehn erforderlichen Anzeigeattribute vor. [Maschinenlesbare Abrechnung](../../research/pa-reach-001/manifests/retention-meta-0630.json)

| Auswahl | Paare | Mittlere ΔCA | Mittlere ΔMeta | Meta gestiegen / gleich / gesunken |
|---|---:|---:|---:|---:|
| Jugendfeldspieler | 15 | +0,8000 | −0,0109 | 6 / 6 / 3 |
| Davon mit CA-Gewinn | 8 | — | +0,0638 | 5 / 2 / 1 |
| Feldspieler unter 28 an der Baseline | 69.268 | +0,2772 | +0,0280 | 20.727 / 41.656 / 6.885 |
| Davon mit CA-Gewinn | 13.708 | — | +0,1241 | 9.244 / 3.260 / 1.204 |

Von 69.477 global qualifizierten Ausgangsprofilen fehlten 181 beim qualifizierten Folgetagsabgleich und 28 wechselten die vom Modell gewählte Bewertungsposition. Die CA der 69.268 gültigen Paare stieg in 13.708 Fällen, blieb in 53.336 gleich und sank in 2.224. Beide Gruppen gehören zu einem Karriereursprung. Die Ergebnisse sind deskriptiv. Zwischen Karrieren gültige Unsicherheit und ein isolierter Effekt der Vertragspolitik lassen sich daraus nicht schätzen.

Der 61-Tage-Kontrast gehört zu FM27 `27.1.0+2505117`. Gehashte Saves und jeweils beidseitige ruhende Kontextabfragen binden die beiden FMSuperScout-Exporte an den 30.04. und 30.06. Die Scout-Header melden abweichend den 28.04. und 30.05. Der Paarvergleich verlangt übereinstimmende Identität, CA/PA und Positionslisten je Stichtag, dieselbe Bewertungsposition über beide Tage und zehn validierte Anzeigeattribute. Die Originalfunktionen `defaultPosition` und `score` aus dem Fork verwenden die Indexskala 1–20. Identisch bedeutet einen numerischen Unterschied von höchstens 10⁻¹². Kleine Rohattributänderungen können unterhalb der Anzeigeauflösung bleiben. [App-Scorer bei 977ecef](https://github.com/Matchekk/FMSuperScout/blob/977ecefe623a3d4081871a0f558ab12d9bce850d/app/outfield-meta27.js) · [Reproduktion](../../research/pa-reach-001/analysis/retention_meta.py)
