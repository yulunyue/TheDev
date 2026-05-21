import {
    Div, FlexColumn, FlexRow
} from "../../base/components/export";
import { CUBE_COLORS } from "./cube_3d_data";

export class CubeGrid extends Div {
    grid_data: number[] = []
    n: number = 2
    block_size: number = 50

    private static FACE_NET_LAYOUT: (number | null)[][]
    static init_cls() {
        CubeGrid.FACE_NET_LAYOUT = [
            [null, 0, null, null],
            [1, 2, 3, 4],
            [null, 5, null, null],
        ]
    }
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
        this.add_children(this.build_net())
    }

    private build_net(): FlexRow[] {
        const blockSize = this.block_size
        const slotWidth = this.n * blockSize

        return CubeGrid.FACE_NET_LAYOUT.map(rowIndices => {
            const row = new FlexRow()
            row.set_style({ justifyContent: 'center' })
            for (const faceIndex of rowIndices) {
                if (faceIndex === null) {
                    row.add_child(this.create_spacer(slotWidth))
                } else {
                    row.add_child(this.build_face(faceIndex, blockSize))
                }
            }
            return row
        })
    }

    private build_face(faceIndex: number, blockSize: number): FlexColumn {
        const face = new FlexColumn()
        const faceData = this.get_face_data(faceIndex)
        for (let j = 0; j < this.n; j++) {
            const row = new FlexRow()
            for (let k = 0; k < this.n; k++) {
                const colorIndex = faceData[j * this.n + k]
                row.add_child(this.create_block(colorIndex, blockSize))
            }
            face.add_child(row)
        }
        return face
    }

    private get_face_data(faceIndex: number): number[] {
        const faceSize = this.n * this.n
        return this.grid_data.slice(faceIndex * faceSize, (faceIndex + 1) * faceSize)
    }

    private create_block(colorIndex: number, blockSize: number): Div {
        const block = new Div()
        block.set_style({
            width: `${blockSize - 2}px`,
            height: `${blockSize - 2}px`,
            backgroundColor: CUBE_COLORS[colorIndex],
            border: '1px solid #444',
        })
        return block
    }

    private create_spacer(slotWidth: number): Div {
        const spacer = new Div()
        spacer.set_style({
            width: `${slotWidth}px`,
            height: '1px',
        })
        return spacer
    }
}

export default function () {
    return new CubeGrid()
}
CubeGrid.init_cls()