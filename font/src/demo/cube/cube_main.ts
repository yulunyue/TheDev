import {
    web_dom, FlexColumn, FlexRow, FormColumn,
    Button, Pre, Title, FormRow
} from "../../base/components/export";
import { CubeGrid } from "./cube_grid";
import { Cube3D } from "./cube_3d";
import { CubeBase } from "./cube_base";

const DELAY_TIME = 300;

export class CubeMain extends CubeBase {
    control_form: FormRow
    random_step_from: FormColumn
    button_row: FlexRow
    new_btn: Button
    solve_btn: Button
    title: Title
    right_panel: FlexColumn
    left_panel: FlexColumn
    main_body: FlexRow

    init_node(): void {
        super.init_node()

        this.title = new Title()
        this.title.set_html("魔方可视化")
        this.cube_grid = new CubeGrid()
        this.cube_3d = new Cube3D()
        this.control_form = new FormRow()
        this.random_step_from = new FormColumn()
        this.button_row = new FlexRow()
        this.new_btn = new Button().set_html("重置")
        this.solve_btn = new Button().set_html("求解")
        this.toggle_btn = new Button().set_html("2D")
        this.button_row.add_children([this.new_btn, this.solve_btn, this.toggle_btn])
        this.action_pre = new Pre()

        this.right_panel = new FlexColumn()
        this.right_panel.add_children([
            this.button_row,
            this.control_form,
            this.random_step_from,
            this.action_pre
        ])
        this.left_panel = new FlexColumn()
        this.left_panel.add_children([this.cube_grid, this.cube_3d])
        this.main_body = new FlexRow()
        this.main_body.add_children([this.left_panel, this.right_panel])
        this.add_children([this.title, this.main_body])
    }

    init_style(): void {
        super.init_style()
        this.set_style({
            overflow: 'hidden',
            backgroundColor: '#e8ecf1'
        })
        this.set_style({ width: "100%", height: "100%" })

        this.title.set_style({
            textAlign: 'center',
            padding: '8px 0',
            backgroundColor: '#fff',
            borderBottom: '1px solid #ddd',
            margin: 0,
            flexShrink: 0,
            fontSize: '16px',
            height: '36px',
            lineHeight: '20px',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
        })

        this.cube_grid.set_style({ margin: '10px' })
        this.cube_3d.set_style({
            width: '400px',
            height: '400px',
        })
        this.cube_grid.hide()

        this.action_pre.set_style({
            backgroundColor: '#fafafa',
            padding: '10px',
            borderRadius: '8px',
            border: '1px solid #e0e0e0',
            maxHeight: '300px',
            overflow: 'auto',
            fontFamily: 'monospace',
            fontSize: '13px',
            lineHeight: '1.6'
        })

        this.control_form.set_style({
            backgroundColor: '#fff',
            padding: '16px',
            borderRadius: '8px',
            border: '1px solid #e0e0e0',
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
        })
        this.random_step_from.set_style({
            backgroundColor: '#fff',
            padding: '16px',
            borderRadius: '8px',
            border: '1px solid #e0e0e0',
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
        })
        this.button_row.set_style({
            gap: '8px'
        })

        this.right_panel.set_style({
            width: '240px',
            minWidth: '200px',
            padding: '16px',
            gap: '12px',
            overflow: 'auto',
            backgroundColor: '#f5f5f5',
            borderLeft: '1px solid #ddd'
        })

        this.left_panel.set_flex(1)
        this.left_panel.set_style({
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px',
            minWidth: 0
        })

        this.main_body.set_flex(1)
        this.main_body.set_style({ overflow: 'hidden' })
    }

    init_event(): void {
        this.new_btn.on_click(() => this.handle_new())
        this.solve_btn.on_click(() => this.handle_solve())
        this.toggle_btn.on_click(() => this.toggle_view())
        this.control_form.on_submit(() => this.handle_rotate())
        this.random_step_from.on_submit(() => this.handle_scramble())
    }

    render(): void {
        this.control_form.set_uri("/cube/scheme_rotate")
        this.random_step_from.set_uri("/cube/scheme_random")
        this.handle_new()
    }

    async handle_scramble(): Promise<void> {
        const steps = parseInt(this.random_step_from.get("steps", "10"))
        web_dom.post("/cube/random", { steps, show_process: true }, async (data: any) => {
            this.title.set_html(`正在打乱 ${steps} 步...`)
            const actions = data.children || []

            for (const action_node of actions) {
                const action = action_node.value
                await this.animate_step(action)
                this.delay(DELAY_TIME)
            }

            this.update_state(data.value)
            this.title.set_html(`打乱完成 - 共 ${steps} 步`)
            this.action_pre.set_html(`打乱步骤:\n${actions.map((a: any) => a.value.description).join('\n')}`)
        })
    }

    async handle_solve(): Promise<void> {
        web_dom.post("/cube/solve", { grid: this.current_grid }, async (data: any) => {
            if (data.value.solved) {
                this.title.set_html("魔方已完成!")
                this.action_pre.set_html("魔方已经处于完成状态")
                return
            }

            this.title.set_html(`正在求解 - 共 ${data.value.steps} 步`)
            const actions = data.value.actions

            for (const action of actions) {
                await this.animate_step(action)
                this.delay(DELAY_TIME * 2)
            }

            this.title.set_html(`求解完成 - 共 ${data.value.steps} 步`)
            this.action_pre.set_html(`求解步骤:\n${actions.map((a: any) => a.description).join('\n')}`)
        })
    }

    animate_step(action: any): Promise<void> {
        return new Promise((resolve) => {
            if (this.is_3d) {
                this.cube_3d.animate_rotate(action.axis, action.layer, action.rotate, () => {
                    this.cube_3d.set_cube_data(action.grid, this.current_n)
                    this.title.set_html(action.description)
                    resolve()
                })
            } else {
                this.cube_grid.set_cube_data(action.grid, this.current_n)
                this.title.set_html(action.description)
                resolve()
            }
        })
    }
}

export default function () {
    return new CubeMain()
}
