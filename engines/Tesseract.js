// ✦ Codex 144:99 - preserve original intention
import * as THREE from 'three';

export default class TesseractEngine {
  constructor({ animate = false } = {}) {
    this.animate = animate;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
    this.camera.position.set(3, 3, 5);
    this.renderer = null;
    this.nodes = [];
    this.nodeMeshes = new Map();
    this.highlightColor = null;
    this.selectCallback = null;
    this.palette = null;
    this.raycaster = new THREE.Raycaster();
    this.pointer = new THREE.Vector2();
  }

  async loadPalette(url = 'data/palettes/visionary.json', use = 'visionary.core') {
    const res = await fetch(url);
    const json = await res.json();
    const path = use.split('.');
    this.palette = path.reduce((acc, key) => (acc ? acc[key] : undefined), json);
    this.highlightColor = this.palette ? this.palette.blue : '#ffffff';
  }

  mount(container) {
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(this.renderer.domElement);
    this.camera.aspect = container.clientWidth / container.clientHeight;
    this.camera.updateProjectionMatrix();
    container.addEventListener('pointerdown', e => this.onPointerDown(e));
    if (this.animate) this.startLoop();
    else this.render();
  }

  setNodes(nodeList = []) {
    this.nodes = nodeList;
    const group = new THREE.Group();
    const color = this.palette ? this.palette.indigo : '#888888';
    nodeList.forEach(node => {
      const geom = new THREE.SphereGeometry(0.05, 16, 16);
      const mat = new THREE.MeshBasicMaterial({ color });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set(node.x, node.y, node.z);
      mesh.userData.id = node.id;
      group.add(mesh);
      this.nodeMeshes.set(node.id, mesh);
    });
    this.scene.add(group);
    this.render();
  }

  transform(matrix) {
    if (matrix instanceof THREE.Matrix4) {
      this.scene.applyMatrix4(matrix);
      this.render();
    }
  }

  highlight(nodeId) {
    const mesh = this.nodeMeshes.get(nodeId);
    if (mesh && this.highlightColor) {
      mesh.material.color.set(this.highlightColor);
      this.render();
    }
  }

  onSelect(callback) {
    this.selectCallback = callback;
  }

  onPointerDown(event) {
    if (!this.renderer) return;
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    this.raycaster.setFromCamera(this.pointer, this.camera);
    const intersects = this.raycaster.intersectObjects(Array.from(this.nodeMeshes.values()));
    if (intersects.length > 0) {
      const id = intersects[0].object.userData.id;
      if (this.selectCallback) this.selectCallback(id);
    }
  }

  startLoop() {
    const loop = () => {
      requestAnimationFrame(loop);
      this.renderer.render(this.scene, this.camera);
    };
    loop();
  }

  render() {
    if (this.renderer) {
      this.renderer.render(this.scene, this.camera);
    }
export default class Tesseract {
  constructor(config = {}) {
    this.config = Object.assign({ animate: false, palette: null }, config);
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(70, 1, 0.1, 1000);
    this.camera.position.z = 5;
    this.renderer = null;
    this.nodes = [];
    this.nodeMeshes = [];
    this.highlighted = null;
    this.selectCallback = null;
  }

  async loadPalette() {
    if (this.config.palette) {
      return this.config.palette;
    }
    try {
      const res = await fetch('data/palettes/visionary.json');
      const json = await res.json();
      this.config.palette = json.visionary.core;
    } catch (err) {
      this.config.palette = {
        indigo: '#280050',
        violet: '#460082',
        blue: '#0080FF',
        green: '#00FF80',
        amber: '#FFC800',
        light: '#FFFFFF'
      };
    }
    return this.config.palette;
  }

  async mount(container) {
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    container.appendChild(this.renderer.domElement);
    this.resize(container);
    window.addEventListener('resize', () => this.resize(container));
    const palette = await this.loadPalette();
    this.scene.background = new THREE.Color(palette.light);
    this._createHypercube(palette);
    this.renderFrame();
  }

  resize(container) {
    if (!this.renderer) return;
    const w = container.clientWidth;
    const h = container.clientHeight;
    this.renderer.setSize(w, h);
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
  }

  _createHypercube(palette) {
    const verts4 = [];
    for (let i = 0; i < 16; i++) {
      const x = (i & 1) ? 1 : -1;
      const y = (i & 2) ? 1 : -1;
      const z = (i & 4) ? 1 : -1;
      const w = (i & 8) ? 1 : -1;
      verts4.push({ x, y, z, w });
    }
    const edges = [];
    for (let i = 0; i < 16; i++) {
      for (let j = i + 1; j < 16; j++) {
        if (((i ^ j) & (i ^ j) - 1) === 0) {
          edges.push([i, j]);
        }
      }
    }
    const vertices = [];
    edges.forEach(([a, b]) => {
      const va = this._project(verts4[a]);
      const vb = this._project(verts4[b]);
      vertices.push(va.x, va.y, va.z, vb.x, vb.y, vb.z);
    });
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    const material = new THREE.LineBasicMaterial({ color: palette.indigo });
    const lines = new THREE.LineSegments(geometry, material);
    this.scene.add(lines);
  }

  _project(v) {
    const k = 1 / (2 - v.w);
    return { x: v.x * k, y: v.y * k, z: v.z * k };
  }

  renderFrame() {
    this.renderer.render(this.scene, this.camera);
    if (this.config.animate) {
      this.scene.rotation.x += 0.01;
      this.scene.rotation.y += 0.01;
      requestAnimationFrame(() => this.renderFrame());
    }
  }

  setNodes(nodeList) {
    this.nodes = nodeList || [];
    this.nodeMeshes.forEach(m => this.scene.remove(m));
    this.nodeMeshes = this.nodes.map(n => {
      const geom = new THREE.SphereGeometry(0.05, 16, 16);
      const mat = new THREE.MeshBasicMaterial({ color: this.config.palette ? this.config.palette.blue : '#0080FF' });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set(n.x, n.y, n.z);
      mesh.userData.id = n.id;
      this.scene.add(mesh);
      return mesh;
    });
  }

  transform(matrixOrPreset) {
    let matrix = null;
    if (typeof matrixOrPreset === 'string') {
      if (matrixOrPreset === 'rotateX') {
        matrix = new THREE.Matrix4().makeRotationX(Math.PI / 4);
      } else if (matrixOrPreset === 'rotateY') {
        matrix = new THREE.Matrix4().makeRotationY(Math.PI / 4);
      } else if (matrixOrPreset === 'rotateZ') {
        matrix = new THREE.Matrix4().makeRotationZ(Math.PI / 4);
      }
    } else if (matrixOrPreset instanceof THREE.Matrix4) {
      matrix = matrixOrPreset;
    }
    if (matrix) {
      this.scene.applyMatrix4(matrix);
    }
  }

  highlight(nodeId) {
    if (this.highlighted) {
      this.highlighted.material.color.set(this.config.palette.blue);
    }
    const mesh = this.nodeMeshes.find(m => m.userData.id === nodeId);
    if (mesh) {
      mesh.material.color.set(this.config.palette.amber);
      this.highlighted = mesh;
    }
  }

  onSelect(cb) {
    this.selectCallback = cb;
    if (!this.renderer) return;
    const canvas = this.renderer.domElement;
    canvas.addEventListener('click', evt => {
      const rect = canvas.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((evt.clientX - rect.left) / rect.width) * 2 - 1,
        -((evt.clientY - rect.top) / rect.height) * 2 + 1
      );
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, this.camera);
      const hits = raycaster.intersectObjects(this.nodeMeshes);
      if (hits.length > 0) {
        const id = hits[0].object.userData.id;
        this.highlight(id);
        if (this.selectCallback) {
          this.selectCallback(id);
        }
      }
    });
  }
}

