import {
    Div, Constant, Node, web_dom, Row, Column
} from "../../base/components/export";

const CUBE_COLORS = ['#3498db', '#e67e22', '#ecf0f1', '#e74c3c', '#f1c40f', '#2ecc71'];

export class CubeGrid extends Div {
    grid_data: number[] = []
    n: number = 2

    init_node(): void {
        super.init_node()
        this.set_style({
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            fontFamily: 'monospace',
            fontSize: '20px',
            padding: '20px',
            backgroundColor: '#f5f5f5',
            borderRadius: '10px'
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
        const blockSize = 40
        
        const faces = []
        for (let i = 0; i < 6; i++) {
            faces.push(this.grid_data.slice(i * faceSize, (i + 1) * faceSize))
        }
        
        const createFaceRow = (faceIndex: number) => {
            const row = new Row()
            for (let j = 0; j < this.n; j++) {
                const col = new Column()
                for (let k = 0; k < this.n; k++) {
                    const block = new Div()
                    const colorIndex = faces[faceIndex][j * this.n + k]
                    block.set_style({
                        width: `${blockSize}px`,
                        height: `${blockSize}px`,
                        backgroundColor: CUBE_COLORS[colorIndex],
                        border: '2px solid #333',
                        borderRadius: '4px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: colorIndex === 2 ? '#333' : '#fff',
                        fontWeight: 'bold',
                        fontSize: '14px',
                        margin: '1px'
                    })
                    block.set_html(CUBE_COLORS[colorIndex].toUpperCase().substring(0, 1))
                    col.add_child(block)
                }
                row.add_child(col)
            }
            return row
        }
        
        const topRow = new Row()
        topRow.set_style({ justifyContent: 'center' })
        topRow.add_child(createFaceRow(0))
        
        const spacerRow = new Row()
        spacerRow.set_style({ width: `${blockSize * this.n * 4}px` })
        
        this.add_child(spacerRow)
        this.add_child(topRow)
        
        const midRow = new Row()
        midRow.set_style({ justifyContent: 'center' })
        for (let i = 4; i >= 1; i--) {
            midRow.add_child(createFaceRow(i === 4 ? 4 : i))
        }
        this.add_child(midRow)
        
        const bottomRow = new Row()
        bottomRow.set_style({ justifyContent: 'center' })
        bottomRow.add_child(createFaceRow(5))
        
        this.add_child(bottomRow)
    }
}

export default function () {
    return new CubeGrid()
}