import {
    web_dom, Row, Column,
    Button, Pre, Title, Input, FormRow
} from "../../base/components/export";
import { CubeGrid } from "./cube_grid";

export class CubePhone extends Row {
    cube_grid: CubeGrid
    title: Title
    control_form: FormRow
    btn_scramble: Button
    btn_reset: Button
    btn_solve: Button
    steps_input: Input
    action_pre: Pre
    current_state: number = 0
    current_grid: number[] = []
    current_n: number = 2
    action_history: string[] = []

    init_node(): void {
        super.init_node()

        this.title = new Title().set_html("魔方")
        this.cube_grid = new CubeGrid().set_block_size(32)
        this.control_form = new FormRow()

        this.steps_input = new Input().set_value("3")
        this.steps_input.set_style({
            width: '50px',
            textAlign: 'center',
            fontSize: '14px',
            padding: '4px',
            border: '1px solid #ccc',
            borderRadius: '4px'
        })

        this.btn_scramble = new Button().set_html("打乱")
        this.btn_reset = new Button().set_html("重置")
        this.btn_solve = new Button().set_html("求解")

        this.action_pre = new Pre()

        const steps_row = new Row()
        steps_row.set_style({ alignItems: 'center', gap: '6px' })
        steps_row.add_childs([new Title().set_html("步数:"), this.steps_input])

        const btn_row = new Column()
        btn_row.set_style({ gap: '8px', justifyContent: 'center' })
        btn_row.add_childs([this.btn_scramble, this.btn_reset, this.btn_solve])

        this.add_childs([this.title, this.cube_grid, this.control_form, steps_row, btn_row, this.action_pre])
    }

    init_style(): void {
        super.init_style()
        this.set_style({
            overflow: 'auto',
            backgroundColor: '#e8ecf1',
            padding: '12px',
            gap: '10px',
            alignItems: 'center'
        })

        this.title.set_style({
            textAlign: 'center',
            padding: '8px 0',
            backgroundColor: '#fff',
            borderBottom: '1px solid #ddd',
            width: '100%',
            flexShrink: 0,
            fontSize: '16px',
            height: '36px',
            lineHeight: '20px',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
        })

        this.cube_grid.set_style({ margin: '4px' })

        this.control_form.set_style({ width: '100%' })

        this.btn_scramble.set_style({
            padding: '10px 20px',
            fontSize: '14px',
            borderRadius: '6px',
            border: 'none',
            backgroundColor: '#3498db',
            color: '#fff',
            cursor: 'pointer'
        })
        this.btn_reset.set_style({
            padding: '10px 20px',
            fontSize: '14px',
            borderRadius: '6px',
            border: 'none',
            backgroundColor: '#95a5a6',
            color: '#fff',
            cursor: 'pointer'
        })
        this.btn_solve.set_style({
            padding: '10px 20px',
            fontSize: '14px',
            borderRadius: '6px',
            border: 'none',
            backgroundColor: '#2ecc71',
            color: '#fff',
            cursor: 'pointer'
        })

        this.action_pre.set_style({
            backgroundColor: '#fafafa',
            padding: '8px',
            borderRadius: '6px',
            border: '1px solid #e0e0e0',
            maxHeight: '120px',
            overflow: 'auto',
            fontFamily: 'monospace',
            fontSize: '12px',
            lineHeight: '1.5',
            width: '100%'
        })
    }

    init_event(): void {
        this.btn_scramble.on_click(() => this.handle_scramble())
        this.btn_reset.on_click(() => this.handle_new())
        this.btn_solve.on_click(() => this.handle_solve())
        this.control_form.on_submit(() => this.handle_rotate())
    }

    render(): void {
        this.control_form.set_uri("/cube/scheme_rotate")
        this.handle_new()
    }

    handle_new(): void {
        web_dom.post("/cube/new", { n: 2 }, (data: any) => {
            this.update_state(data.value)
            this.action_history = []
            this.title.set_html("魔方")
            this.action_pre.set_html("")
        })
    }

    async handle_scramble(): Promise<void> {
        const steps = parseInt(this.steps_input.get_value()) || 3
        web_dom.post("/cube/random", { steps, show_process: true }, async (data: any) => {
            this.title.set_html(`打乱中...`)
            const actions = data.childs || []
            for (const action_node of actions) {
                const action = action_node.value
                this.cube_grid.set_cube_data(action.grid, this.current_n)
                this.title.set_html(action.description)
                await this.delay(200)
            }
            this.update_state(data.value)
            this.title.set_html(`打乱 ${steps} 步`)
            this.action_pre.set_html(actions.map(a => a.value.description).join('\n'))
        })
    }

    handle_rotate(): void {
        let param = this.control_form.get_value()
        param.state = this.current_state
        web_dom.post("/cube/rotate", param,
            (data: any) => {
                this.update_state(data.value)
                const desc = data.value.action?.description || "旋转完成"
                this.action_history.push(desc)
                this.title.set_html(desc)
                this.action_pre.set_html(this.action_history.join('\n'))
            }
        )
    }

    async handle_solve(): Promise<void> {
        web_dom.post("/cube/solve", { state: this.current_state }, async (data: any) => {
            if (data.value.solved) {
                this.title.set_html("已完成!")
                this.action_pre.set_html("魔方已完成")
                return
            }
            this.title.set_html(`求解中...`)
            const actions = data.value.actions
            for (const action of actions) {
                this.cube_grid.set_cube_data(action.grid, this.current_n)
                this.title.set_html(action.description)
                await this.delay(200)
            }
            this.title.set_html(`求解完成 ${data.value.steps} 步`)
            this.action_pre.set_html(actions.map(a => a.description).join('\n'))
        })
    }

    update_state(data: any): void {
        this.current_state = data.state
        this.current_grid = data.grid
        this.current_n = data.n
        this.cube_grid.set_cube_data(data.grid, data.n)
        if (data.game_over) {
            this.title.set_html("已完成!")
        }
    }

    delay(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms))
    }
}

export default function () {
    return new CubePhone()
}
