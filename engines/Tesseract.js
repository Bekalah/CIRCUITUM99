// ✦ Codex 144:99 — preserve original intention
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
  }
}
