import {
    Div, Row, Column
} from "../../base/components/export";

const CUBE_COLORS = ['#3498db', '#ff9800', '#ecf0f1', '#d32f2f', '#1a1a1a', '#2ecc71'];

export class CubeGrid extends Div {
    grid_data: number[] = []
    n: number = 2
    block_size: number = 50

    set_block_size(size: number): this {
        this.block_size = size
        return this
    }

    init_node(): void {
        super.init_node()
    }

    init_style(): void {
        super.init_style()
        this.set_style({
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px',
            backgroundColor: '#f0f0f0',
            borderRadius: '12px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
            minWidth: '300px'
        })
    }

    set_cube_data(grid: number[], n: number): void {
        this.grid_data = grid
        this.n = n
        this.render_cube()
    }

    render_cube(): void {
        this.clear()

        const faceSize = this.n * this.n
        const blockSize = this.block_size

        const faces = []
        for (let i = 0; i < 6; i++) {
            faces.push(this.grid_data.slice(i * faceSize, (i + 1) * faceSize))
        }

        const createBlock = (colorIndex: number) => {
            const block = new Div()
            block.set_style({
                width: `${blockSize - 2}px`,
                height: `${blockSize - 2}px`,
                backgroundColor: CUBE_COLORS[colorIndex],
                border: '1px solid #444',
            })
            return block
        }

        const reorderIdx = (faceIndex: number, j: number, k: number): number => {
            if (faceIndex === 3 || faceIndex === 4) {
                // 水平镜像：左右互换，用于背面(-Z)和左面(-X)
                return j * this.n + (this.n - 1 - k)
            }
            if (faceIndex === 5) {
                // 90° 顺时针旋转，用于底面(-Y)
                return (this.n - 1 - k) * this.n + j
            }
            return j * this.n + k
        }

        const createFace = (faceIndex: number) => {
            const col = new Row()
            for (let j = 0; j < this.n; j++) {
                const row = new Column()
                for (let k = 0; k < this.n; k++) {
                    const colorIndex = faces[faceIndex][reorderIdx(faceIndex, j, k)]
                    row.add_child(createBlock(colorIndex))
                }
                col.add_child(row)
            }
            return col
        }

        const faceContainer = (faceIndex: number) => {
            const col = new Row()
            col.add_child(createFace(faceIndex))
            return col
        }

        const slotWidth = this.n * this.block_size

        const faceRow = (faces_arr: (number | null)[]) => {
            const row = new Column()
            row.set_style({ justifyContent: 'center' })
            for (const fi of faces_arr) {
                if (fi === null) {
                    const spacer = new Div()
                    spacer.set_style({
                        width: `${slotWidth}px`,
                        height: '1px',
                    })
                    row.add_child(spacer)
                } else {
                    row.add_child(faceContainer(fi))
                }
            }
            return row
        }

        this.add_childs([
            faceRow([null, null, 0, null]),
            faceRow([4, 1, 2, 3]),
            faceRow([null, null, 5, null]),
        ])
    }
}

export default function () {
    return new CubeGrid()
}
