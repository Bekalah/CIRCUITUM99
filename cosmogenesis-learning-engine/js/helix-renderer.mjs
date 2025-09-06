/*
  helix-renderer.mjs
  ND-safe static renderer for layered sacred geometry.

  Layers:
    1) Vesica field (intersecting circles)
    2) Tree-of-Life scaffold (10 sephirot + 22 paths; simplified layout)
    3) Fibonacci curve (log spiral polyline; static)
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
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

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
    }
    ctx.stroke();
  }
}
