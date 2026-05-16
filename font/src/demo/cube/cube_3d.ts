import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Div } from "../../base/components/export";
import { CUBE_COLORS, GRID_MAP, FACE_ORDER, CUBIE_KEYS, CUBIE_MAP, VISIBLE_FACES, CubieData } from "./cube_3d_data";

export class Cube3D extends Div {
    private scene: THREE.Scene;
    private camera: THREE.PerspectiveCamera;
    private renderer: THREE.WebGLRenderer;
    private controls: OrbitControls;
    private cubies: CubieData[] = [];
    private grid: number[] = [];
    private animating: boolean = false;

    init_node(): void {
        super.init_node();

        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xe8ecf1);

        this.camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
        this.camera.position.set(3, 2.5, 3);
        this.camera.lookAt(0, 0, 0);

        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.el.appendChild(this.renderer.domElement);

        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.1;
        this.controls.rotateSpeed = 0.8;
        this.controls.target.set(0, 0, 0);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        this.scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
        dirLight.position.set(5, 8, 6);
        this.scene.add(dirLight);

        const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.3);
        dirLight2.position.set(-3, -2, -4);
        this.scene.add(dirLight2);

        this.add_axis();
        this.render_loop();
    }

    private add_axis(): void {
        const len = 1.8;
        this.scene.add(new THREE.AxesHelper(len));

        const makeLabel = (text: string, pos: THREE.Vector3, color: string) => {
            const c = document.createElement('canvas');
            c.width = 64; c.height = 64;
            const ctx = c.getContext('2d')!;
            ctx.font = 'Bold 48px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = color;
            ctx.fillText(text, 32, 32);
            const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
                map: new THREE.CanvasTexture(c), transparent: true, depthTest: false,
            }));
            sprite.position.copy(pos);
            sprite.scale.set(0.5, 0.5, 1);
            this.scene.add(sprite);
        };
        makeLabel('X', new THREE.Vector3(len + 0.3, 0, 0), '#ff0000');
        makeLabel('Y', new THREE.Vector3(0, len + 0.3, 0), '#00ff00');
        makeLabel('Z', new THREE.Vector3(0, 0, len + 0.3), '#0000ff');
    }

    init_style(): void {
        super.init_style();
        this.set_style({
            width: '400px',
            height: '400px',
        });
        this.hide();
    }

    private render_loop(): void {
        const loop = () => {
            this.controls.update();
            this.renderer.render(this.scene, this.camera);
            requestAnimationFrame(loop);
        };
        loop();
    }

    set_cube_data(grid: number[], n: number): void {
        this.grid = [...grid];

        if (this.cubies.length === 0) {
            this.rebuild_cubies(n);
        }

        this.update_stickers();
    }

    private rebuild_cubies(n: number): void {
        for (const c of this.cubies) {
            this.scene.remove(c.mesh);
            c.mesh.geometry.dispose();
            c.materials.forEach(m => m.dispose());
        }
        this.cubies = [];

        const cubeSize = 0.92;
        const geo = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
        const edgesGeo = new THREE.EdgesGeometry(geo);
        const lineMat = new THREE.LineBasicMaterial({ color: 0x444444 });
        const darkMat = new THREE.MeshStandardMaterial({
            color: 0x222222, roughness: 0.4, metalness: 0.1,
        });

        for (let x = 0; x < 2; x++) {
            for (let y = 0; y < 2; y++) {
                for (let z = 0; z < 2; z++) {
                    const key = `${x},${y},${z}`;
                    const visible = VISIBLE_FACES[key];
                    const materials: THREE.MeshStandardMaterial[] = FACE_ORDER.map(face =>
                        new THREE.MeshStandardMaterial({
                            color: visible.includes(face) ? 0x888888 : 0x222222,
                            roughness: 0.3,
                            metalness: 0.05,
                        })
                    );

                    const mesh = new THREE.Mesh(geo.clone(), materials);
                    mesh.position.set(x - 0.5, y - 0.5, z - 0.5);
                    const wireframe = new THREE.LineSegments(edgesGeo.clone(), lineMat);
                    mesh.add(wireframe);
                    this.scene.add(mesh);

                    this.cubies.push({ x, y, z, mesh, materials });
                }
            }
        }
    }

    private update_stickers(): void {
        for (const cubie of this.cubies) {
            const key = `${cubie.x},${cubie.y},${cubie.z}`;
            const stickers = CUBIE_MAP[key];
            for (let fi = 0; fi < FACE_ORDER.length; fi++) {
                const face = FACE_ORDER[fi];
                const idx = stickers[face];
                if (idx !== undefined) {
                    cubie.materials[fi].color.set(CUBE_COLORS[this.grid[idx]]);
                }
            }
        }
    }

    animate_rotate(axis: number, layer: number, rotate: number, onDone?: () => void): void {
        if (this.animating || this.cubies.length === 0) return;
        this.animating = true;

        const coord = ['y', 'x', 'z'][axis];
        const layerCubies = this.cubies.filter(c => c[coord] === layer);

        let angle: number;
        if (rotate === 2) {
            angle = Math.PI;
        } else {
            const dir = rotate === 1 ? 1 : -1;
            let base: number;
            switch (axis) {
                case 0: base = layer === 0 ? Math.PI / 2 : -Math.PI / 2; break;
                case 1: base = layer === 0 ? Math.PI / 2 : -Math.PI / 2; break;
                case 2: base = layer === 0 ? -Math.PI / 2 : Math.PI / 2; break;
                default: base = 0;
            }
            angle = base * dir;
        }

        const rotAxis = new THREE.Vector3(
            axis === 1 ? 1 : 0,
            axis === 0 ? 1 : 0,
            axis === 2 ? 1 : 0,
        );

        const pivot = new THREE.Group();
        this.scene.add(pivot);
        for (const cubie of layerCubies) {
            pivot.attach(cubie.mesh);
        }

        const startQuat = new THREE.Quaternion();
        const endQuat = new THREE.Quaternion().setFromAxisAngle(rotAxis, angle);
        const duration = 300;
        const startTime = performance.now();

        const animateFrame = () => {
            const t = Math.min((performance.now() - startTime) / duration, 1);
            const eased = t * (3 - 2 * t);

            pivot.quaternion.copy(startQuat).slerp(endQuat, eased);

            if (t < 1) {
                requestAnimationFrame(animateFrame);
            } else {
                pivot.quaternion.copy(startQuat).slerp(endQuat, 1);
                pivot.updateMatrixWorld(true);

                for (const cubie of layerCubies) {
                    this.scene.attach(cubie.mesh);
                    cubie.x = Math.round(cubie.mesh.position.x + 0.5);
                    cubie.y = Math.round(cubie.mesh.position.y + 0.5);
                    cubie.z = Math.round(cubie.mesh.position.z + 0.5);
                }
                this.scene.remove(pivot);

                this.animating = false;
                if (onDone) onDone();
            }
        };
        animateFrame();
    }

    resize(): void {
        const rect = this.el.getBoundingClientRect();
        const w = rect.width || 400;
        const h = rect.height || 400;
        this.camera.aspect = w / h;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(w, h);
    }
}

export default function () {
    return new Cube3D();
}
