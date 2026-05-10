import {
    web_dom, FormColumn, Row, Column,
    Button, Pre, Title
} from "../../base/components/export";
import { CubeGrid } from "./cube_grid";

const DELAY_TIME = 300;

export class CubeMain extends Row {
    cube_grid: CubeGrid
    control_form: FormColumn
    button_row: Column
    new_btn: Button
    solve_btn: Button
    title: Title
    action_pre: Pre
    right_panel: Row
    left_panel: Row
    main_body: Column
    current_state: number = 0
    current_grid: number[] = []
    current_n: number = 2
    action_history: string[] = []

    init_node(): void {
        super.init_node()

        this.title = new Title()
        this.title.set_html("魔方可视化")
        this.cube_grid = new CubeGrid()
        this.control_form = new FormColumn()
        this.random_step_from = new For
        this.button_row = new Column()
        this.button_row.add_childs([this.new_btn, this.scramble_btn, this.rotate_btn, this.solve_btn])
        this.action_pre = new Pre()

        this.right_panel = new Row()
        this.right_panel.add_childs([
            this.control_form,
            this.button_row,
            this.action_pre
        ])
        this.left_panel = new Row()
        this.left_panel.add_child(this.cube_grid)
        this.main_body = new Column()
        this.main_body.add_childs([this.left_panel, this.right_panel])
        this.add_childs([this.title, this.main_body])
    }

    init_style(): void {
        super.init_style()
        this.set_style({
            overflow: 'hidden',
            backgroundColor: '#e8ecf1'
        })
        this.set_style({ width: 1, height: 1 })

        this.title.set_style({
            textAlign: 'center',
            padding: '8px 0',
            backgroundColor: '#fff',
            borderBottom: '1px solid #ddd',
            margin: 0,
            flexShrink: 0,
            fontSize: '16px'
        })

        this.cube_grid.set_style({ margin: '10px' })

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

        this.button_row.set_style({
            gap: '8px'
        })

        this.right_panel.set_style({
            width: '320px',
            minWidth: '320px',
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
        this.scramble_btn.on_click(() => this.handle_scramble())
        this.rotate_btn.on_click(() => this.handle_rotate())
        this.solve_btn.on_click(() => this.handle_solve())
    }

    render(): void {
        this.control_form.set_uri("/cube/scheme_rotate")
        this.handle_new()
    }

    handle_new(): void {
        web_dom.post("/cube/new", { n: 2 }, (data: any) => {
            this.update_state(data.value)
            this.action_history = []
            this.title.set_html("新建魔方完成")
            this.action_pre.set_html("魔方已初始化")
        })
    }

    async handle_scramble(): Promise<void> {
        const steps = parseInt(this.control_form.child_map.steps.get_value()) || 10
        web_dom.post("/cube/random", { steps, show_process: true }, async (data: any) => {
            this.title.set_html(`正在打乱 ${steps} 步...`)
            const actions = data.childs || []

            for (const action_node of actions) {
                const action = action_node.value
                await this.animate_step(action)
                this.delay(DELAY_TIME)
            }

            this.update_state(data.value)
            this.title.set_html(`打乱完成 - 共 ${steps} 步`)
            this.action_pre.set_html(`打乱步骤:\n${actions.map(a => a.value.description).join('\n')}`)
        })
    }

    handle_rotate(): void {
        const axis = parseInt(this.control_form.child_map.axis.get_value())
        const layer = parseInt(this.control_form.child_map.layer.get_value())
        const rotate = parseInt(this.control_form.child_map.rotate.get_value())

        web_dom.post("/cube/rotate", {
            state: this.current_state,
            axis,
            layer,
            rotate
        }, (data: any) => {
            this.update_state(data.value)
            const action_desc = data.value.action?.description || "旋转完成"
            this.action_history.push(action_desc)
            this.title.set_html(action_desc)
            this.action_pre.set_html(this.action_history.join('\n'))
        })
    }

    async handle_solve(): Promise<void> {
        web_dom.post("/cube/solve", { state: this.current_state }, async (data: any) => {
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
            this.action_pre.set_html(`求解步骤:\n${actions.map(a => a.description).join('\n')}`)
        })
    }

    update_state(data: any): void {
        this.current_state = data.state
        this.current_grid = data.grid
        this.current_n = data.n
        this.cube_grid.set_cube_data(data.grid, data.n)

        if (data.game_over) {
            this.title.set_html("魔方已完成!")
        }
    }

    animate_step(action: any): Promise<void> {
        return new Promise((resolve) => {
            this.cube_grid.set_cube_data(action.grid, this.current_n)
            this.title.set_html(action.description)
            resolve()
        })
    }

    delay(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms))
    }
}

export default function () {
    return new CubeMain()
}
