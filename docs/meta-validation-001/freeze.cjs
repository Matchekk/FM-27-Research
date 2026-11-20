// Run with the path to the clean, pinned FMSuperScout checkout. No player data required.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const { execFileSync } = require('node:child_process');
const root = path.resolve(process.argv[2]);
const git = (...args) => execFileSync('git', ['-C', root, ...args]);
const commit = '977ecefe623a3d4081871a0f558ab12d9bce850d';
if (git('rev-parse', 'HEAD').toString().trim() !== commit || git('status','--porcelain','--untracked-files=no').length)
  throw new Error('Model checkout differs from freeze');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const api = require(path.join(root, 'app/outfield-meta27.js'));
const files = ['app/outfield-meta27.js','app/app.js','test/harness.js','test/outfield-v21.test.js',
  'docs/fm27-outfield-meta-v2-model.json','docs/fm27-meta-score-v2-1.md','tools/rank-outfield-meta.js','core/Dumper.cs','core/Fields.cs'];
const normalized = fn => fn.toString().replaceAll('\r\n','\n');
const component = value => hash(JSON.stringify(value));
const design = JSON.parse(fs.readFileSync(path.join(__dirname,'profile-config.json'),'utf8'));
console.log(JSON.stringify({
  commit, commit_payload_sha256:hash(git('cat-file','commit',commit)),
  git_blob_content_sha256:Object.fromEntries(files.map(f=>[f,hash(git('show',commit+':'+f))])),
  coefficients_sha256:component(api.model.profiles),
  utility_sha256:hash(normalized(api.jumpingReachUtility)),
  positions_sha256:component([api.model.positions,api.model.defaultPositionOrder,normalized(api.defaultPosition)]),
  params_sha256:component([api.version,api.model.sourceShares,api.evaluate(Object.fromEntries(
    api.model.profiles.ST.requiredAttributes.map(k=>[k,10])),'ST').nonlinearity,
    Array.from({length:20},(_,i)=>api.jumpingReachUtility(i+1))]),
  profile_config_sha256:component(design),
}, null, 2));
