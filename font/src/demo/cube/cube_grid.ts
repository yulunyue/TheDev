import {
    Div, FlexColumn, FlexRow
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

        const faces: number[][] = []
        for (let i = 0; i < 6; i++) {
            faces.push(this.grid_data.slice(i * faceSize, (i + 1) * faceSize))
        }

        const createBlock = (colorIndex: number): Div => {
            const block = new Div()
            block.set_style({
                width: `${blockSize - 2}px`,
                height: `${blockSize - 2}px`,
                backgroundColor: CUBE_COLORS[colorIndex],
                border: '1px solid #444',
            })
            return block
        }

        const createFace = (faceIndex: number): FlexColumn => {
            const faceColumn = new FlexColumn()
            for (let j = 0; j < this.n; j++) {
                const faceRow = new FlexRow()
                for (let k = 0; k < this.n; k++) {
                    const idx = j * this.n + k
                    const colorIndex = faces[faceIndex][idx]
                    faceRow.add_child(createBlock(colorIndex))
                }
                faceColumn.add_child(faceRow)
            }
            return faceColumn
        }

        const slotWidth = this.n * this.block_size

        const createFaceRow = (faceIndices: (number | null)[]): FlexRow => {
            const row = new FlexRow()
            row.set_style({ justifyContent: 'center' })
            for (const faceIndex of faceIndices) {
                if (faceIndex === null) {
                    const spacer = new Div()
                    spacer.set_style({
                        width: `${slotWidth}px`,
                        height: '1px',
                    })
                    row.add_child(spacer)
                } else {
                    row.add_child(createFace(faceIndex))
                }
            }
            return row
        }

        this.add_childs([
            createFaceRow([null, null, 0, null]),
            createFaceRow([1, 2, 3, 4]),
            createFaceRow([null, null, 5, null]),
        ])
    }
}

export default function () {
    return new CubeGrid()
}
