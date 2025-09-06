/*
  helix-renderer.mjs
  ND-safe static renderer for layered sacred geometry.

  Layers:
    1) Vesica field (intersecting circles)
    2) Tree-of-Life scaffold (10 sephirot + 22 paths; simplified layout)
    3) Fibonacci curve (log spiral polyline; static)
    4) Double-helix lattice (two phase-shifted sine curves)
  The routines favor calm colors and avoid motion.
*/

export function renderHelix(ctx, opts) {
  const { width, height, palette, NUM } = opts;
  ctx.fillStyle = palette.bg;
  ctx.fillRect(0, 0, width, height);
  drawVesica(ctx, width, height, palette.layers[0], NUM);
  drawTree(ctx, width, height, palette.layers[1], palette.layers[2], NUM);
  drawFibonacci(ctx, width, height, palette.layers[3], NUM);
  drawHelix(ctx, width, height, palette.layers[4], palette.layers[5], NUM);
}

// Layer 1: Vesica grid
function drawVesica(ctx, w, h, color, NUM) {
  // ND-safe: thin lines and roomy spacing keep the field gentle.
  const step = w / NUM.TWENTYTWO;
  const r = step;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  for (let y = r; y < h; y += step) {
    for (let x = r; x < w; x += step) {
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.stroke();
    }
  }
}

// Layer 2: Tree-of-Life scaffold
function drawTree(ctx, w, h, pathColor, nodeColor, NUM) {
  // Simplified placement, centered to aid focus.
  const nodes = [
    { x: 0.5, y: 0.05 },
    { x: 0.7, y: 0.18 },
    { x: 0.3, y: 0.18 },
    { x: 0.7, y: 0.36 },
    { x: 0.3, y: 0.36 },
    { x: 0.5, y: 0.5 },
    { x: 0.7, y: 0.64 },
    { x: 0.3, y: 0.64 },
    { x: 0.5, y: 0.77 },
    { x: 0.5, y: 0.9 }
  ].map(n => ({ x: n.x * w, y: n.y * h }));
  const paths = [
    [0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 4], [3, 5], [4, 5],
    [3, 6], [4, 7], [6, 7], [6, 8], [7, 8], [8, 9], [5, 6], [5, 7],
    [5, 8], [1, 6], [2, 7], [0, 5], [2, 6], [1, 7]
  ];
  ctx.strokeStyle = pathColor;
  ctx.lineWidth = 2;
  paths.forEach(p => {
    ctx.beginPath();
    ctx.moveTo(nodes[p[0]].x, nodes[p[0]].y);
    ctx.lineTo(nodes[p[1]].x, nodes[p[1]].y);
    ctx.stroke();
  });
  ctx.fillStyle = nodeColor;
  const r = Math.min(w, h) / NUM.THIRTYTHREE;
  nodes.forEach(n => {
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fill();
  });
}

// Layer 3: Fibonacci curve
function drawFibonacci(ctx, w, h, color, NUM) {
  // Static log spiral using the golden ratio; no animation.
  const phi = (1 + Math.sqrt(5)) / 2;
  const cx = w / 2, cy = h / 2;
  const r0 = Math.min(w, h) / NUM.ONEFORTYFOUR;
  const maxTheta = NUM.NINE * Math.PI / NUM.THREE; // ~3π
  const step = maxTheta / NUM.NINETYNINE;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let theta = 0; theta <= maxTheta; theta += step) {
    const r = r0 * Math.pow(phi, theta / (Math.PI / 2));
    const x = cx + r * Math.cos(theta);
    const y = cy + r * Math.sin(theta);
    if (theta === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

// Layer 4: Double-helix lattice
function drawHelix(ctx, w, h, colorA, colorB, NUM) {
  // Two phase-shifted sine waves; vertical links create a lattice.
  const step = w / NUM.NINETYNINE;
  const amp = h / 4;
  const freq = NUM.TWENTYTWO * Math.PI / w;
  const helix = (phase, color) => {
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x = 0; x <= w; x += step) {
      const y = h / 2 + Math.sin(freq * x + phase) * amp;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    return x => h / 2 + Math.sin(freq * x + phase) * amp;
  };
  const y1 = helix(0, colorA);
  const y2 = helix(Math.PI, colorB);
  ctx.strokeStyle = colorB;
  ctx.lineWidth = 1;
  for (let x = 0; x <= w; x += step * NUM.ELEVEN) {
    ctx.beginPath();
    ctx.moveTo(x, y1(x));
    ctx.lineTo(x, y2(x));
    ctx.stroke();
  }
}
