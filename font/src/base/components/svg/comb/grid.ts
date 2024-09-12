import { GNode, gnode } from "../gnode";
import { line } from "../line";
export class Grid extends GNode {
    row: number
    col: number
    row_size: number
    col_size: number
    data: any
    grid_lines: GNode
    init_node(): void {
        this.row = 2
        this.col = 2
        this.row_size = 30
        this.col_size = 30
        this.data = {}
        this.grid_lines = this.add_child(gnode())
        this.draw()
    }
    draw_grid_line() {
        this.grid_lines.clear()
        for (var i = 0; i <= this.row; i += 1) {
            this.grid_lines.add_child(line().set_d([
                { x: 0, y: i * this.row_size },
                { x: this.col_size * this.col, y: i * this.row_size }
            ]))
        }
        for (var i = 0; i <= this.col; i += 1) {
            this.grid_lines.add_child(line().set_d([
                { x: i * this.col_size, y: 0 },
                { x: i * this.col_size, y: this.row_size * this.row }
            ]))
        }
        return this
    }
    draw() {
        this.draw_grid_line()
        return this
    }
    set_row(row: any) {
        this.row = row
        return this
    }

}
export function grid() {
    return new Grid()
}