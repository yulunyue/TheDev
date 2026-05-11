import {
    Div, Row, Column
} from "../../base/components/export";

const CUBE_COLORS = ['#3498db', '#e67e22', '#ecf0f1', '#e74c3c', '#f1c40f', '#2ecc71'];

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
                width: `${blockSize}px`,
                height: `${blockSize}px`,
                backgroundColor: CUBE_COLORS[colorIndex],
                borderRadius: '6px',
                margin: '2px',
                boxShadow: 'inset 0 1px 2px rgba(255,255,255,0.3), 0 2px 4px rgba(0,0,0,0.2)'
            })
            return block
        }

        const createFace = (faceIndex: number) => {
            const col = new Column()
            col.set_style({ margin: '0 2px' })
            for (let j = 0; j < this.n; j++) {
                const row = new Row()
                for (let k = 0; k < this.n; k++) {
                    const colorIndex = faces[faceIndex][j * this.n + k]
                    row.add_child(createBlock(colorIndex))
                }
                col.add_child(row)
            }
            return col
        }

        const faceContainer = (faceIndex: number) => {
            const col = new Row()
            col.set_style({ alignItems: 'center', margin: '0 6px' })
            col.add_child(createFace(faceIndex))
            return col
        }

        const slotWidth = this.n * (this.block_size + 4) + 4

        const faceRow = (faces_arr: (number | null)[]) => {
            const row = new Column()
            row.set_style({ justifyContent: 'center' })
            for (const fi of faces_arr) {
                if (fi === null) {
                    const spacer = new Div()
                    spacer.set_style({
                        width: `${slotWidth}px`,
                        height: '1px',
                        margin: '0 6px'
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
