/*
  helix-renderer.mjs
  ND-safe static renderer for layered sacred geometry.

  Layers:
    1) Vesica field (intersecting circles)
    2) Tree-of-Life scaffold (10 sephirot + 22 paths; simplified layout)
    3) Fibonacci curve (log spiral polyline; static)
    4) Double-helix lattice (two phase-shifted sine strands)

  Why ND-safe: renders once, no motion; calm colors; each layer isolated for sensory clarity.

    4) Double-helix lattice (two phase-shifted sine waves with rungs)

  All geometry uses calm colors and no motion for ND safety.

*/

export function renderHelix(ctx, opts) {
  const { width, height, palette, NUM } = opts;
  ctx.save();

  // background

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

  drawHelix(ctx, width, height, palette.layers[4], palette.layers[5], NUM);
}

function drawVesica(ctx, w, h, color, NUM) {
  // Vesica Piscis: two circles intersecting; ratio uses 7 for gentle spacing
  const r = Math.min(w, h) / NUM.SEVEN;

    4) Double-helix lattice (two phase-shifted sine waves)

  No animation, no external deps. Pure functions for clarity.
*/
export function renderHelix(ctx, { width, height, palette, NUM }) {
  ctx.fillStyle = palette.bg;
  ctx.fillRect(0, 0, width, height);
  drawVesica(ctx, width, height, palette.layers[0]);
  drawTreeOfLife(ctx, width, height, palette.layers[1], NUM);
  drawFibonacci(ctx, width, height, palette.layers[2]);
  drawHelix(ctx, width, height, palette.layers[3], NUM);
}

// L1: Vesica field — two intersecting circles symbolizing primordial duality
function drawVesica(ctx, w, h, color) {
  const r = Math.min(w, h) / 3;

  const cx = w / 2;
  const cy = h / 2;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx - r / 2, cy, r, 0, Math.PI * 2);
  ctx.arc(cx + r / 2, cy, r, 0, Math.PI * 2);
  ctx.stroke();
}

function drawTreeOfLife(ctx, w, h, nodeColor, pathColor, NUM) {
  // Simplified sephirot layout; proportioned with numerology constants
  const nodes = [
    [0.5, 0.08],
    [0.33, 0.18], [0.67, 0.18],
    [0.33, 0.38], [0.67, 0.38],
    [0.33, 0.58], [0.67, 0.58],
    [0.33, 0.78], [0.67, 0.78],
    [0.5, 0.88]
  ];

  const paths = [
    [0, 1], [0, 2], [1, 2], [1, 3], [2, 4],
    [3, 4], [3, 5], [4, 6], [5, 6], [5, 7],
    [6, 8], [7, 8], [7, 9], [8, 9], [1, 4],
    [2, 3], [3, 8], [4, 7], [1, 6], [2, 5],
    [3, 9], [4, 9]
  ];

  ctx.strokeStyle = pathColor;
  ctx.lineWidth = 1;
  for (const [a, b] of paths) {
    const [ax, ay] = nodes[a];
    const [bx, by] = nodes[b];
    ctx.beginPath();
    ctx.moveTo(ax * w, ay * h);
    ctx.lineTo(bx * w, by * h);

    ctx.stroke();
  }

  ctx.fillStyle = nodeColor;
  const r = Math.min(w, h) / NUM.NINETYNINE; // small node size from numerology 99
  for (const [x, y] of px) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);

  const r = NUM.THREE; // small nodes for low visual load
  for (const [nx, ny] of nodes) {
    ctx.beginPath();
    ctx.arc(nx * w, ny * h, r, 0, Math.PI * 2);
    ctx.arc(cx - r/2, cy, r, 0, Math.PI * 2);
    ctx.arc(cx + r/2, cy, r, 0, Math.PI * 2);
    ctx.stroke();
   }

// L2: Tree-of-Life scaffold — ND-safe, static positions
function drawTreeOfLife(ctx, w, h, color, NUM) {
  // Simplified layout based on numerology constants
  const nodes = [];
  const levels = [0, 1/6, 2/6, 3/6, 4/6, 5/6, 1];
  const centerX = w / 2;
  const span = h * 0.8;
  for (let i = 0; i < 10; i++) {
    const level = levels[Math.floor(i/2)];
    const offset = (i % 2 === 0) ? -w/8 : w/8;
    nodes.push({ x: centerX + offset, y: h*0.1 + span*level });
  }
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 1;
  // paths: connect every node on different levels (simplified 22 paths)
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i+1; j < nodes.length; j++) {
      ctx.beginPath();
      ctx.moveTo(nodes[i].x, nodes[i].y);
      ctx.lineTo(nodes[j].x, nodes[j].y);
      ctx.stroke();
    }
  }
  for (const n of nodes) {
    ctx.beginPath();
    ctx.arc(n.x, n.y, NUM.THREE, 0, Math.PI*2);
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

function drawFibonacci(ctx, w, h, color, NUM) {
  // Log spiral using 99 points; phi controls growth (no motion)
  const cx = w / 2;
  const cy = h / 2;
  const steps = NUM.NINETYNINE;
  const turns = NUM.THREE; // three full turns
  const scale = Math.min(w, h) / NUM.TWENTYTWO; // gentle size
  const phi = (1 + Math.sqrt(5)) / 2;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps) * turns * Math.PI * 2;
    const r = scale * Math.pow(phi, t / (Math.PI * 2));
    const x = cx + r * Math.cos(t);
    const y = cy + r * Math.sin(t);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);

// L3: Fibonacci curve — static log spiral using golden ratio
function drawFibonacci(ctx, w, h, color) {
  const phi = (1 + Math.sqrt(5)) / 2; // golden ratio
  const cx = w * 0.2;
  const cy = h * 0.8;
  const turns = 10;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i < turns * 50; i++) {
    const t = i / 50;
    const r = Math.pow(phi, t) * 2; // static growth
    const ang = t * Math.PI / 2;
    const x = cx + r * Math.cos(ang);
    const y = cy - r * Math.sin(ang);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y)
  ctx.stroke();
}

function drawHelix(ctx, w, h, colorA, colorB, NUM) {
  // Static double helix: two sine waves with 22 rungs
  const steps = NUM.NINETYNINE;
  const amplitude = h / NUM.ELEVEN;
  const baseY = h / 2;
  ctx.lineWidth = 1.5;

  const wave = (color, phase) => {
    ctx.strokeStyle = color;
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      const x = t * w;
      const y = baseY + Math.sin(t * NUM.THIRTYTHREE + phase) * amplitude;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      ctx.stroke();
  }

  wave(colorA, 0);
  wave(colorB, Math.PI);
  ctx.strokeStyle = colorB;
  for (let i = 0; i <= NUM.TWENTYTWO; i++) {
    const t = i / NUM.TWENTYTWO;
    const x = t * w;
    const y1 = baseY + Math.sin(t * NUM.THIRTYTHREE) * amplitude;
    const y2 = baseY + Math.sin(t * NUM.THIRTYTHREE + Math.PI) * amplitude;

    ctx.beginPath();
    ctx.moveTo(x, y1);
    ctx.lineTo(x, y2);
    ctx.stroke();


// L4: Double-helix lattice — two sine waves offset by PI
function drawHelix(ctx, w, h, color, NUM) {
  const amp = h / 4;
  const step = w / NUM.NINETYNINE; // use numerology constant for spacing
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  for (let phase = 0; phase < 2; phase++) {
    ctx.beginPath();
    for (let x = 0; x <= w; x += step) {
      const y = h/2 + amp * Math.sin((x/step)/NUM.ELEVEN + phase*Math.PI);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
      ctx.stroke();

  }
}

