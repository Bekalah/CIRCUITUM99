import { readFile, writeFile } from 'fs/promises';

async function main() {
  const structure = JSON.parse(await readFile('data/structure.json', 'utf8'));
  const lineage = JSON.parse(await readFile('data/tree-of-fusion-artists.json', 'utf8'));
  const enriched = { ...structure, lineage };
  await writeFile('data/structure.enriched.json', JSON.stringify(enriched, null, 2) + '\n');
  console.log('data/structure.enriched.json written');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
