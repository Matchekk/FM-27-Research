// Execute unchanged scoring functions from the pinned app with a verified scan context.
'use strict';
const fs = require('node:fs');
const crypto = require('node:crypto');
const path = require('node:path');
const vm = require('node:vm');
const readline = require('node:readline');

function pinned(file, expected) {
  const source = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n');
  const bytes = Buffer.from(source);
  const blob = crypto.createHash('sha1').update(`blob ${bytes.length}\0`).update(bytes).digest('hex');
  if (blob !== expected) throw new Error('Unexpected app source at ' + path.basename(file));
  return source;
}
const app = pinned(process.argv[2], '870f970c1de46d77ccfc5d1662a017bd1edb6331');
const scorer = path.resolve(process.argv[3]);
pinned(scorer, '181eab2ae56bacdf32cff6b4c93e6b604f0fc1db');
function part(start, end) {
  const a = app.indexOf(start), b = app.indexOf(end, a + start.length);
  if (a < 0 || b < 0) throw new Error('Pinned app section unavailable');
  return app.slice(a, b);
}

const context = vm.createContext({ FMSSOutfieldMeta27: require(scorer), localStorage: { getItem: () => null } });
vm.runInContext([
  part('const state = {', '// Resten van het oude'),
  part('function getAge(p)', 'const parseGameDate'),
  part('const parseGameDate =', '\n'),
  part('const natPos =', '\n'),
  part('const isFm27Gk =', '\n'),
  part('function weightedMeta(p, attrs)', '// Pure position evaluator'),
  part('let metaMemos =', 'function outfieldEvidenceLabel'),
  part('const PHYS_ATTRS =', '// Profielweergave:'),
  part('    if (state.meta.gameDate) {', '    state.dumpStamp = st.dumpTime;').replace(/^/, 'function setMeta(meta) { state.meta = meta;\n') + '\n}',
  'globalThis.run = (p, meta) => { setMeta(meta); return [FMSSOutfieldMeta27.defaultPosition(p), metaScore(p), metaPaScore(p)]; };',
].join('\n'), context);

async function main() {
  const lines = readline.createInterface({input: process.stdin});
  let headers;
  for await (const line of lines) {
    const item = JSON.parse(line);
    if (!headers) { headers = item; continue; }
    const result = headers.map(meta => context.run(item, meta));
    process.stdout.write(JSON.stringify(result) + '\n');
  }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
