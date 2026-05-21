import {
    web_dom, FlexColumn, FlexRow,
    Button, Pre, Title, FormColumn
} from "../../base/components/export";
import { CubeGrid } from "./cube_grid";
import { Cube3D } from "./cube_3d";

export abstract class CubeBase extends FlexColumn {
    cube_grid: CubeGrid
    cube_3d: Cube3D
    title: Title
    action_pre: Pre
    toggle_btn: Button
    current_grid: number[] = []
    current_n: number = 2
    action_history: string[] = []
    is_3d: boolean = true

    toggle_view(): void {
        this.is_3d = !this.is_3d
        if (this.is_3d) {
            this.cube_grid.hide()
            this.cube_3d.show()
            this.toggle_btn.set_html("2D")
            this.cube_3d.set_cube_data(this.current_grid, this.current_n)
            this.cube_3d.resize()
        } else {
            this.cube_grid.show()
            this.cube_3d.hide()
            this.toggle_btn.set_html("3D")
        }
    }

    handle_new(): void {
        web_dom.post("/cube/new", { n: 2 }, (data: any) => {
            this.update_state(data.value)
            this.cube_3d.reset(this.current_n)
            this.action_history = []
        })
    }

    handle_rotate(): void {
        let param = this.control_form.get_value()
        param.grid = this.current_grid
        web_dom.post("/cube/rotate", param,
            (data: any) => {
                this.update_state(data.value)
                const desc = data.value.action?.description || "旋转完成"
                this.action_history.push(desc)
                this.title.set_html(desc)
                this.action_pre.set_html(this.action_history.join('\n'))
                if (this.is_3d) {
                    const a = data.value.action
                    this.cube_3d.animate_rotate(a.axis, a.layer, a.rotate, () => {
                        this.cube_3d.set_cube_data(this.current_grid, this.current_n)
                    })
                }
            }
        )
    }

    update_state(data: any): void {
        this.current_grid = data.grid
        this.current_n = data.n
        this.cube_grid.set_cube_data(data.grid, data.n)
        if (this.is_3d) {
            this.cube_3d.show()
            this.cube_3d.resize()
        }
        if (data.game_over) {
            this.title.set_html("已完成!")
        }
    }

    delay(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms))
    }

    abstract control_form: any
}
