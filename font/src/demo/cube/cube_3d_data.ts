import * as THREE from 'three'

export const CUBE_COLORS = ['#3498db', '#ff9800', '#ecf0f1', '#d32f2f', '#1a1a1a', '#2ecc71']

export interface StickerInfo {
    x: number; y: number; z: number;
    face: string;
}
export const GRID_MAP: StickerInfo[] = [
    { x: 0, y: 1, z: 0, face: '+Y' }, { x: 1, y: 1, z: 0, face: '+Y' }, { x: 0, y: 1, z: 1, face: '+Y' }, { x: 1, y: 1, z: 1, face: '+Y' },
    { x: 0, y: 1, z: 0, face: '-X' }, { x: 0, y: 1, z: 1, face: '-X' }, { x: 0, y: 0, z: 0, face: '-X' }, { x: 0, y: 0, z: 1, face: '-X' },
    { x: 0, y: 1, z: 1, face: '+Z' }, { x: 1, y: 1, z: 1, face: '+Z' }, { x: 0, y: 0, z: 1, face: '+Z' }, { x: 1, y: 0, z: 1, face: '+Z' },
    { x: 1, y: 1, z: 1, face: '+X' }, { x: 1, y: 1, z: 0, face: '+X' }, { x: 1, y: 0, z: 1, face: '+X' }, { x: 1, y: 0, z: 0, face: '+X' },
    { x: 1, y: 1, z: 0, face: '-Z' }, { x: 0, y: 1, z: 0, face: '-Z' }, { x: 1, y: 0, z: 0, face: '-Z' }, { x: 0, y: 0, z: 0, face: '-Z' },
    { x: 0, y: 0, z: 1, face: '-Y' }, { x: 1, y: 0, z: 1, face: '-Y' }, { x: 0, y: 0, z: 0, face: '-Y' }, { x: 1, y: 0, z: 0, face: '-Y' },
]

export const FACE_ORDER = ['+X', '-X', '+Y', '-Y', '+Z', '-Z']
export const CUBIE_KEYS = ['0,0,0', '0,0,1', '0,1,0', '0,1,1', '1,0,0', '1,0,1', '1,1,0', '1,1,1']

export type CubieStickers = Record<string, number>
export const CUBIE_MAP: Record<string, CubieStickers> = {}
for (const key of CUBIE_KEYS) CUBIE_MAP[key] = {}
for (let i = 0; i < GRID_MAP.length; i++) {
    const m = GRID_MAP[i]
    CUBIE_MAP[`${m.x},${m.y},${m.z}`][m.face] = i
}

export const VISIBLE_FACES: Record<string, string[]> = {}
for (const key of CUBIE_KEYS) {
    const [x, y, z] = key.split(',').map(Number)
    const faces: string[] = []
    if (x === 0) faces.push('-X')
    if (x === 1) faces.push('+X')
    if (y === 0) faces.push('-Y')
    if (y === 1) faces.push('+Y')
    if (z === 0) faces.push('-Z')
    if (z === 1) faces.push('+Z')
    VISIBLE_FACES[key] = faces
}

export function calc_angle(axis: number, layer: number, rotate: number): number {
    if (rotate === 2) return Math.PI;
    const dir = rotate === 1 ? 1 : -1;
    let base: number;
    switch (axis) {
        case 0: base = Math.PI / 2; break;
        case 1: base = layer === 0 ? Math.PI / 2 : -Math.PI / 2; break;
        case 2: base = layer === 0 ? Math.PI / 2 : -Math.PI / 2; break;
        default: base = 0;
    }
    return base * dir;
}

export interface CubieData {
    x: number; y: number; z: number;
    mesh: THREE.Mesh;
    materials: THREE.MeshStandardMaterial[];
    [key: string]: any;
}
