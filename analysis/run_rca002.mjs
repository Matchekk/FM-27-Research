// Executes only the pinned, locally supplied pure source calculator. No game access.
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const { estimateCaExact } = await import(pathToFileURL(process.argv[2]).href);
const requests = JSON.parse(readFileSync(0, 'utf8'));
const results = requests.map(request => {
  const before = JSON.stringify(request);
  const first = estimateCaExact(request);
  const second = estimateCaExact(request);
  if (!first || !Number.isInteger(first.estimated_ca)) throw Error('Invalid source output');
  if (before !== JSON.stringify(request)) throw Error('Source mutated request');
  if (JSON.stringify(first) !== JSON.stringify(second)) throw Error('A/A mismatch');
  return first;
});
process.stdout.write(JSON.stringify(results));
