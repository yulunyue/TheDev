import {
    Div, Row, Column
} from "../../base/components/export";

const CUBE_COLORS = ['#3498db', '#e67e22', '#ecf0f1', '#e74c3c', '#f1c40f', '#2ecc71'];
const FACE_LABELS = ['上', '左', '前', '右', '後', '下'];

export class CubeGrid extends Div {
    grid_data: number[] = []
    n: number = 2

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
        const blockSize = 50

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

        const createLabel = (text: string) => {
            const lb = new Div()
            lb.set_style({
                fontSize: '12px',
                color: '#666',
                textAlign: 'center',
                fontWeight: 'bold',
                margin: '2px 0'
            })
            lb.set_html(text)
            return lb
        }

        const faceContainer = (faceIndex: number, labelPos: 'top' | 'bottom' | 'none' = 'none') => {
            const col = new Row()
            col.set_style({ alignItems: 'center', margin: '0 6px' })
            if (labelPos === 'top') {
                const c = new Row()
                c.add_child(createLabel(FACE_LABELS[faceIndex]))
                c.add_child(createFace(faceIndex))
                col.add_child(c)
            } else {
                col.add_child(createFace(faceIndex))
                if (labelPos === 'bottom') {
                    col.add_child(createLabel(FACE_LABELS[faceIndex]))
                }
            }
            return col
        }

        const topRow = new Column()
        topRow.set_style({ justifyContent: 'center' })
        topRow.add_child(faceContainer(0, 'top'))

        const midRow = new Column()
        midRow.set_style({ justifyContent: 'center' })
        const midFaces = [4, 1, 2, 3]
        for (const fi of midFaces) {
            midRow.add_child(faceContainer(fi, 'bottom'))
        }

        const bottomRow = new Column()
        bottomRow.set_style({ justifyContent: 'center' })
        bottomRow.add_child(faceContainer(5, 'bottom'))

        this.add_childs([topRow, midRow, bottomRow])
    }
}

export default function () {
    return new CubeGrid()
}
