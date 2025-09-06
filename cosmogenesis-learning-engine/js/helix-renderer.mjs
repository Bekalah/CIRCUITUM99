/*
  helix-renderer.mjs
  ND-safe static renderer for layered sacred geometry.

  Layers:
    1) Vesica field (intersecting circles)
    2) Tree-of-Life scaffold (10 sephirot + 22 paths; simplified layout)
    3) Fibonacci curve (log spiral polyline; static)
    4) Double-helix lattice (two phase-shifted sine strands)

  Why ND-safe: renders once, no motion; calm colors; each layer isolated for sensory clarity.
*/

export function renderHelix(ctx, opts) {
  const { width, height, palette, NUM } = opts;
  ctx.save();

  // background
  ctx.fillStyle = palette.bg;
  ctx.fillRect(0, 0, width, height);

  drawVesica(ctx, width, height, palette.layers[0], NUM);
  drawTreeOfLife(ctx, width, height, palette.layers[1], palette.layers[2], NUM);
  drawFibonacci(ctx, width, height, palette.layers[3], NUM);
  drawHelix(ctx, width, height, palette.layers[4], palette.layers[5] || palette.ink, NUM);

  ctx.restore();
}

// L1 Vesica field
function drawVesica(ctx, w, h, color, NUM) {
  const r = Math.min(w, h) / NUM.THREE; // scale from numerology 3
  const offset = r;
  const cy = h / 2;

  ctx.strokeStyle = color;
  ctx.lineWidth = 2;

  // three pairs across the canvas (left, center, right)
  for (let i = -1; i <= 1; i++) {
    const cxL = w / 2 + i * offset - r / 2;
    const cxR = w / 2 + i * offset + r / 2;
    ctx.beginPath();
    ctx.arc(cxL, cy, r, 0, Math.PI * 2);
    ctx.arc(cxR, cy, r, 0, Math.PI * 2);
    ctx.stroke();
  }
}

// L2 Tree-of-Life scaffold (simplified geometry)
function drawTreeOfLife(ctx, w, h, pathColor, nodeColor, NUM) {
  const nodes = [
    [0.5, 0.05], // Keter
    [0.75, 0.18], [0.25, 0.18], // Chokmah, Binah
    [0.75, 0.35], [0.25, 0.35], // Chesed, Geburah
    [0.5, 0.5], // Tiferet
    [0.75, 0.65], [0.25, 0.65], // Netzach, Hod
    [0.5, 0.8], // Yesod
    [0.5, 0.95] // Malkuth
  ];

  const px = nodes.map(n => [n[0] * w, n[1] * h]);
  const edges = [
    [0,1],[0,2],[1,2],
    [1,3],[1,5],[2,4],[2,5],
    [3,4],[3,5],[4,5],
    [3,6],[4,7],[5,6],[5,7],
    [6,8],[7,8],
    [8,9],
    [3,7],[4,6]
  ];
  // add extra paths to reach 22 total connections (22 = Hebrew letters)
  edges.push([1,4],[2,3],[6,7]);

  ctx.strokeStyle = pathColor;
  ctx.lineWidth = 2;
  for (const [a, b] of edges) {
    ctx.beginPath();
    ctx.moveTo(px[a][0], px[a][1]);
    ctx.lineTo(px[b][0], px[b][1]);
    ctx.stroke();
  }

  ctx.fillStyle = nodeColor;
  const r = Math.min(w, h) / NUM.NINETYNINE; // small node size from numerology 99
  for (const [x, y] of px) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }
}

// L3 Fibonacci spiral (static polyline)
function drawFibonacci(ctx, w, h, color, NUM) {
  const cx = w / 2;
  const cy = h / 2;
  const points = [];
  const steps = NUM.ONEFORTYFOUR; // 144 = completion cycle
  const growth = 1.61803398875; // golden ratio

  for (let i = 0; i <= steps; i += NUM.THREE) { // step by 3 for smoothness
    const angle = (i / NUM.TWENTYTWO) * Math.PI * 2;
    const radius = Math.pow(growth, i / NUM.ELEVEN);
    points.push([cx + radius * Math.cos(angle), cy + radius * Math.sin(angle)]);
  }

  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i < points.length; i++) {
    const [x, y] = points[i];
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

// L4 Double-helix lattice (static, no motion)
function drawHelix(ctx, w, h, colorA, colorB, NUM) {
  const mid = h / 2;
  const amp = h / NUM.NINE;
  const turns = NUM.THREE; // triple twist
  const step = w / NUM.ONEFORTYFOUR; // resolution

  // strand A
  ctx.strokeStyle = colorA;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let x = 0; x <= w; x += step) {
    const t = (x / w) * turns * Math.PI * 2;
    const y = mid + amp * Math.sin(t);
    if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // strand B (phase shift by π)
  ctx.strokeStyle = colorB;
  ctx.beginPath();
  for (let x = 0; x <= w; x += step) {
    const t = (x / w) * turns * Math.PI * 2;
    const y = mid + amp * Math.sin(t + Math.PI);
    if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // lattice rungs using 22 segments
  ctx.strokeStyle = colorA;
  const rungStep = w / NUM.TWENTYTWO;
  for (let x = 0; x <= w; x += rungStep) {
    const t = (x / w) * turns * Math.PI * 2;
    const y1 = mid + amp * Math.sin(t);
    const y2 = mid + amp * Math.sin(t + Math.PI);
    ctx.beginPath();
    ctx.moveTo(x, y1);
    ctx.lineTo(x, y2);
    ctx.stroke();
  }
}

