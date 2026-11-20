// Read privately matched rows from stdin. Only aggregate results leave this process.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const readline = require('node:readline');
const modelPath = path.resolve(process.argv[2]);
const source = Buffer.from(fs.readFileSync(modelPath, 'utf8').replace(/\r\n/g, '\n'));
const blob = crypto.createHash('sha1').update('blob ' + source.length + '\0').update(source).digest('hex');
if (blob !== '181eab2ae56bacdf32cff6b4c93e6b604f0fc1db') throw Error('Unexpected model source');
const model = require(modelPath);
if (model.version !== 'FM27_OUTFIELD_META_V2_1') throw Error('Unexpected model version');

function group() {
  return {n: 0, up: 0, equal: 0, down: 0, sumDelta: 0};
}
function tally(target, delta) {
  target.n += 1;
  target[delta > 1e-12 ? 'up' : delta < -1e-12 ? 'down' : 'equal'] += 1;
  target.sumDelta += delta;
}
async function main() {
  const result = {modelBlob: blob, modelVersion: model.version, scoreable: group(),
    caGain: group(), byPosition: {}, positionUnavailable: 0, positionChanged: 0, cannotScore: 0};
  const withCA = process.argv.includes('--with-ca');
  if (withCA) Object.assign(result, {pairedCA: group(), caUnchanged: group(), caLoss: group()});
  for await (const line of readline.createInterface({input: process.stdin})) {
    const [a, b, deltaCA] = JSON.parse(line);
    const position = model.defaultPosition(a);
    const endPosition = model.defaultPosition(b);
    if (!position || !endPosition) { result.positionUnavailable++; continue; }
    if (position !== endPosition) { result.positionChanged++; continue; }
    const start = model.score(a.attrs, position);
    const end = model.score(b.attrs, position);
    if (!Number.isFinite(start) || !Number.isFinite(end)) { result.cannotScore++; continue; }
    const delta = end-start;
    tally(result.scoreable, delta);
    tally(result.byPosition[position] ??= group(), delta);
    if (deltaCA > 0) tally(result.caGain, delta);
    if (withCA) {
      tally(result.pairedCA, deltaCA);
      if (deltaCA === 0) tally(result.caUnchanged, delta);
      if (deltaCA < 0) tally(result.caLoss, delta);
    }
  }
  process.stdout.write(JSON.stringify(result));
}
main().catch(e => { console.error(e.message); process.exitCode = 1; });
