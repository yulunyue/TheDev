import { describe, expect, it } from 'vitest'
import {
    GRID_MAP, FACE_ORDER, CUBIE_KEYS, CUBIE_MAP, VISIBLE_FACES,
    CUBE_COLORS, calc_angle,
} from './cube_3d_data'

describe('GRID_MAP', () => {
    it('covers all 24 indices exactly once', () => {
        const indices = GRID_MAP.map(m => m.face + `${m.x},${m.y},${m.z}`)
        expect(indices.length).toBe(24)
        expect(new Set(indices).size).toBe(24)
    })

    it('has 4 entries per face', () => {
        const faceCount: Record<string, number> = {}
        for (const m of GRID_MAP) {
            faceCount[m.face] = (faceCount[m.face] || 0) + 1
        }
        for (const count of Object.values(faceCount)) {
            expect(count).toBe(4)
        }
    })
})

describe('FACE_ORDER', () => {
    it('matches Three.js BoxGeometry convention: +x, -x, +y, -y, +z, -z', () => {
        expect(FACE_ORDER).toEqual(['+X', '-X', '+Y', '-Y', '+Z', '-Z'])
    })
})

describe('CUBIE_MAP', () => {
    it('has entries for all 8 cubies', () => {
        expect(Object.keys(CUBIE_MAP).sort()).toEqual(CUBIE_KEYS.sort())
    })

    it('each cubie maps faces to correct grid indices', () => {
        // cubie (0,1,0): +Y=0, -X=4, -Z=17
        expect(CUBIE_MAP['0,1,0']).toEqual({ '+Y': 0, '-X': 4, '-Z': 17 })
        // cubie (1,1,1): +Y=3, +X=12, +Z=9
        expect(CUBIE_MAP['1,1,1']).toEqual({ '+Y': 3, '+X': 12, '+Z': 9 })
        // cubie (0,0,0): -X=6, -Z=19, -Y=22
        expect(CUBIE_MAP['0,0,0']).toEqual({ '-X': 6, '-Z': 19, '-Y': 22 })
        // cubie (1,0,1): +Z=11, +X=14, -Y=21
        expect(CUBIE_MAP['1,0,1']).toEqual({ '+Z': 11, '+X': 14, '-Y': 21 })
    })

    it('each cubie has 3 visible faces', () => {
        for (const key of CUBIE_KEYS) {
            expect(Object.keys(CUBIE_MAP[key]).length).toBe(3)
        }
    })
})

describe('VISIBLE_FACES', () => {
    it('matches CUBIE_MAP face keys for each cubie', () => {
        for (const key of CUBIE_KEYS) {
            const visible = VISIBLE_FACES[key].sort()
            const mapped = Object.keys(CUBIE_MAP[key]).sort()
            expect(visible).toEqual(mapped)
        }
    })
})

describe('calc_angle', () => {
    it('rotate=2 returns PI for any axis/layer', () => {
        for (let axis = 0; axis < 3; axis++) {
            for (let layer = 0; layer < 2; layer++) {
                expect(calc_angle(axis, layer, 2)).toBe(Math.PI)
            }
        }
    })

    it('Y axis (axis=0): clockwise direction', () => {
        expect(calc_angle(0, 0, 1)).toBe(Math.PI / 2)
        expect(calc_angle(0, 1, 1)).toBe(Math.PI / 2)
    })

    it('Y axis (axis=0): counter-clockwise direction', () => {
        expect(calc_angle(0, 0, -1)).toBe(-Math.PI / 2)
        expect(calc_angle(0, 1, -1)).toBe(-Math.PI / 2)
    })

    it('X axis (axis=1): layer 0 clockwise, layer 1 counter-clockwise', () => {
        expect(calc_angle(1, 0, 1)).toBe(Math.PI / 2)
        expect(calc_angle(1, 1, 1)).toBe(-Math.PI / 2)
    })

    it('X axis (axis=1): counter-clockwise reverses', () => {
        expect(calc_angle(1, 0, -1)).toBe(-Math.PI / 2)
        expect(calc_angle(1, 1, -1)).toBe(Math.PI / 2)
    })

    it('Z axis (axis=2): layer 0 clockwise, layer 1 counter-clockwise', () => {
        expect(calc_angle(2, 0, 1)).toBe(Math.PI / 2)
        expect(calc_angle(2, 1, 1)).toBe(-Math.PI / 2)
    })

    it('Z axis (axis=2): counter-clockwise reverses', () => {
        expect(calc_angle(2, 0, -1)).toBe(-Math.PI / 2)
        expect(calc_angle(2, 1, -1)).toBe(Math.PI / 2)
    })
})

describe('sticker lookup', () => {
    const SOLVED = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]

    function getFaceColor(grid: number[], x: number, y: number, z: number, face: string): string {
        const idx = CUBIE_MAP[`${x},${y},${z}`][face]
        return CUBE_COLORS[grid[idx]]
    }

    it('solved cube: each face has uniform color', () => {
        expect(getFaceColor(SOLVED, 0, 1, 0, '+Y')).toBe('#3498db')
        expect(getFaceColor(SOLVED, 1, 1, 0, '+Y')).toBe('#3498db')
        expect(getFaceColor(SOLVED, 1, 0, 0, '-Y')).toBe('#2ecc71')
        expect(getFaceColor(SOLVED, 0, 0, 1, '+Z')).toBe('#ecf0f1')
    })

    // fixture grids from backend python
    // U: axis=0, layer=1, rotate=1
    const U_GRID = [0, 0, 0, 0, 1, 1, 4, 4, 2, 2, 1, 1, 3, 3, 2, 2, 4, 4, 3, 3, 5, 5, 5, 5]

    it('after U: top layer cubies rotated, bottom unchanged', () => {
        // bottom face unchanged
        expect(getFaceColor(U_GRID, 0, 0, 1, '-Y')).toBe('#2ecc71')
        // top face still all blue (U rotate doesn't change +Y stickers)
        expect(getFaceColor(U_GRID, 0, 1, 0, '+Y')).toBe('#3498db')
        // side faces permuted: (0,1,0) -Z changed from yellow(4) to yellow(4) -> in this fixture it stays yellow
        expect(getFaceColor(U_GRID, 0, 1, 0, '-Z')).toBe('#1a1a1a')
    })

    // D: axis=0, layer=0, rotate=1
    const D_GRID = [0, 0, 0, 0, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5]

    it('after D: bottom layer cubies rotated', () => {
        // top face unchanged
        expect(getFaceColor(D_GRID, 0, 1, 0, '+Y')).toBe('#3498db')
        // bottom face still all green
        expect(getFaceColor(D_GRID, 0, 0, 1, '-Y')).toBe('#2ecc71')
    })
})
