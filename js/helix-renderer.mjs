// Per Texturas Numerorum, Spira Loquitur.  // Codex 144:99 ↔ Ateliers ↔ Liber Arcanae
/*
  helix-renderer.mjs
  ND-safe static renderer for layered sacred geometry.

  Layers:
    1) Vesica field (intersecting circles)
    2) Tree-of-Life scaffold (10 sephirot + 22 paths; simplified layout)
    3) Fibonacci curve (log spiral polyline; static)
    4) Double-helix lattice (two phase-shifted sine curves with crossbars)

  No animation, no network. Each draw routine is pure.
  Palette layers: [0] vesica, [1] tree paths, [2] tree nodes,
                  [3] Fibonacci, [4] helix A, [5] helix B.
  Order matters: background to foreground to preserve depth without motion.
*/
export function renderHelix(ctx, { width, height, palette, NUM }) {
  ctx.fillStyle = palette.bg;
  ctx.fillRect(0, 0, width, height);
  const layers = palette.layers;

  drawVesica(ctx, width, height, layers[0], NUM);
  drawTree(ctx, width, height, layers[1], layers[2], NUM);
  drawFibonacci(ctx, width, height, layers[3], NUM);
  drawHelix(ctx, width, height, layers[4], layers[5], NUM);
}

// 1) Vesica field — foundational duality
function drawVesica(ctx, w, h, color, NUM) {
  const r = Math.min(w, h) / NUM.THREE;
  const cx1 = w / 2 - r;
  const cx2 = w / 2 + r;
  const cy = h / 2;
  ctx.strokeStyle = color;
  ctx.lineWidth = NUM.ELEVEN / 10; // 1.1: nod to 11 without heavy line
  // ND-safe: empty centers avoid visual overload
  ctx.beginPath();
  ctx.arc(cx1, cy, r, 0, Math.PI * 2);
  ctx.arc(cx2, cy, r, 0, Math.PI * 2);
  ctx.stroke();
}

// 2) Tree-of-Life scaffold — map of 10 nodes / 22 paths
function drawTree(ctx, w, h, colorPaths, colorNodes, NUM) {
  // three columns (left, center, right)
  const cols = [w / NUM.THREE, w / 2, w - w / NUM.THREE];
  const rowStep = h / NUM.NINE;
  // five rows to place Malkuth; start at rowStep to keep top margin
  const rows = Array.from({ length: 5 }, (_, i) => rowStep * (i + 1));
  const nodes = [
    [1,0],             // 0 Kether
    [0,1], [2,1],      // 1 Chokmah, 2 Binah
    [0,2], [1,2], [2,2], // 3 Chesed, 4 Tiphareth, 5 Geburah
    [0,3], [2,3],      // 6 Netzach, 7 Hod
    [1,3],             // 8 Yesod
    [1,4]              // 9 Malkuth
  ].map(([c,r]) => [cols[c], rows[r]]);
  // 22 simplified paths between nodes
  const paths = [
    [0,1],[0,2],[0,4],       // from Kether
    [1,2],[1,3],[1,4],[1,6], // from Chokmah
    [2,5],[2,4],[2,7],       // from Binah
    [3,5],[3,4],[3,6],       // from Chesed
    [5,4],[5,7],             // from Geburah
    [4,6],[4,7],[4,8],       // from Tiphareth
    [6,7],[6,8],             // lower connections
    [7,8],                   // Hod ↔ Yesod
    [8,9]                    // Yesod → Malkuth
  ];
  ctx.strokeStyle = colorPaths;
  ctx.lineWidth = 1.5;
  for (const [a,b] of paths) {
    ctx.beginPath();
    ctx.moveTo(...nodes[a]);
    ctx.lineTo(...nodes[b]);
    ctx.stroke();
  }
  ctx.fillStyle = colorNodes;
  for (const [x,y] of nodes) {
    ctx.beginPath();
    ctx.arc(x, y, NUM.THREE, 0, Math.PI * 2);
    // ND-safe: small disks keep focus without glare
    ctx.fill();
  }
}

// 3) Fibonacci curve — growth without flash
function drawFibonacci(ctx, w, h, color, NUM) {
  const fib = [1,1,2,3,5,8,13];
  const scale = Math.min(w, h) / NUM.ONEFORTYFOUR * NUM.THIRTYTHREE * (NUM.ELEVEN / NUM.NINETYNINE);
  // start nearer center: 33/99 reduces to 1/3 but keeps numerology visible
  let x = (w / NUM.NINETYNINE) * NUM.THIRTYTHREE;
  let y = h - h / NUM.SEVEN;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  // ND-safe: even stroke, no gradient, no motion
  ctx.beginPath();
  ctx.moveTo(x, y);
  let angle = 0;
  for (const n of fib) {
    const s = n * scale;
    ctx.arc(x, y, s, angle, angle + Math.PI / 2, false);
    x += s * Math.cos(angle + Math.PI / 2);
    y += s * Math.sin(angle + Math.PI / 2);
    angle += Math.PI / 2;
  }
  ctx.stroke();
}

// 4) Double-helix lattice — static sine weave
function drawHelix(ctx, w, h, colorA, colorB, NUM) {
  const turns = NUM.NINE;
  const amp = h / NUM.ELEVEN; // softer wave: 11 marks chromatic balance
  const step = w / NUM.TWENTYTWO; // 22 crossbars for path resonance
  ctx.lineWidth = 1;
  // ND-safe: single-pixel lines keep lattice quiet
  ctx.strokeStyle = colorA;
  ctx.beginPath();
  for (let x = 0; x <= w; x += 1) {
    const y = h / 2 + Math.sin((x / w) * Math.PI * turns) * amp;
    ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.strokeStyle = colorB;
  ctx.beginPath();
  for (let x = 0; x <= w; x += 1) {
    const y = h / 2 + Math.cos((x / w) * Math.PI * turns) * amp;
    ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.strokeStyle = colorA;
  for (let x = 0; x <= w; x += step) {
    const y1 = h / 2 + Math.sin((x / w) * Math.PI * turns) * amp;
    const y2 = h / 2 + Math.cos((x / w) * Math.PI * turns) * amp;
    ctx.beginPath();
    ctx.moveTo(x, y1);
    ctx.lineTo(x, y2);
    ctx.stroke();
  }
}

