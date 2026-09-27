import fs from 'node:fs';

const required = [
  'README.md',
  'METHODS.md',
  'HD189733b_Transit_Photometry.ipynb',
  'data/analysis-contract.json',
];
const failures = [];

for (const file of required) {
  if (!fs.existsSync(file)) failures.push(`${file} missing`);
}

const notebook = JSON.parse(
  fs.readFileSync('HD189733b_Transit_Photometry.ipynb', 'utf8'),
);
const contract = JSON.parse(
  fs.readFileSync('data/analysis-contract.json', 'utf8'),
);
const notebookText = notebook.cells
  .map((cell) => (cell.source || []).join(''))
  .join('\n');
const readme = fs.readFileSync('README.md', 'utf8');
const methods = fs.readFileSync('METHODS.md', 'utf8');

if (notebook.nbformat !== 4 || !Array.isArray(notebook.cells)) {
  failures.push('notebook must be valid nbformat 4 JSON');
}
for (const token of [
  'maximum valid cadences; lowest index breaks ties',
  'event_depths_with_local_baselines',
  'np.random.default_rng(189733)',
  'for _ in range(5000)',
  'per_transit_depths.csv',
]) {
  if (!notebookText.includes(token)) failures.push(`notebook contract missing: ${token}`);
}
for (const forbidden of [
  'good["score"] = np.abs(good["depth_percent"] - REFERENCE_DEPTH_PERCENT)',
  'chosen = good.sort_values("score")',
  'Research Quality Upgrade',
]) {
  if (`${notebookText}\n${readme}`.includes(forbidden)) {
    failures.push(`forbidden circular/upgrade text present: ${forbidden}`);
  }
}
if (contract.bootstrap.resamples !== 5000 || contract.bootstrap.seed !== 189733) {
  failures.push('bootstrap implementation and analysis contract disagree');
}
if (!methods.includes('published transit depth participates')) {
  failures.push('methods must state the product-selection exclusion');
}

if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(
  `Notebook contract valid: ${notebook.cells.length} cells; ` +
    `${contract.bootstrap.resamples} event-bootstrap resamples.`,
);
