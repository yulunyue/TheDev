import {
    Div, Constant, Node, web_dom, FormColumn, Row, Column,
    Button, Pre, Title, Select, Input, ListUi
} from "../../base/components/export";
import { CubeGrid } from "./cube_grid";

const DELAY_TIME = 300;

export class CubeMain extends Column {
    cube_grid: CubeGrid
    control_form: FormColumn
    axis_select: Select
    layer_select: Select
    rotate_select: Select
    steps_input: Input
    title: Title
    action_pre: Pre
    history_list: ListUi
    current_state: number = 0
    current_grid: number[] = []
    current_n: number = 2
    action_history: any[] = []

    init_node(): void {
        super.init_node()
        this.full().set_center()
        
        this.cube_grid = new CubeGrid()
        this.control_form = new FormColumn()
        this.axis_select = new Select()
        this.layer_select = new Select()
        this.rotate_select = new Select()
        this.steps_input = new Input()
        this.title = new Title()
        this.action_pre = new Pre()
        this.history_list = new ListUi()
        
        const button_row = new Row()
        const new_btn = new Button().set_html("新建魔方")
        const scramble_btn = new Button().set_html("随机打乱")
        const rotate_btn = new Button().set_html("执行旋转")
        const solve_btn = new Button().set_html("求解魔方")
        
        new_btn.on_click(() => this.handle_new())
        scramble_btn.on_click(() => this.handle_scramble())
        rotate_btn.on_click(() => this.handle_rotate())
        solve_btn.on_click(() => this.handle_solve())
        
        button_row.add_childs([new_btn, scramble_btn, rotate_btn, solve_btn])
        
        this.add_childs([
            this.title,
            this.cube_grid,
            this.control_form,
            button_row,
            this.action_pre
        ])
    }

    init_style(): void {
        super.init_style()
        this.cube_grid.set_style({ margin: '10px' })
        this.title.set_size(2).set_style({ textAlign: 'center' })
        this.action_pre.set_style({
            backgroundColor: '#f0f0f0',
            padding: '10px',
            borderRadius: '5px',
            maxHeight: '200px',
            overflow: 'auto'
        })
        this.control_form.set_style({
            backgroundColor: '#fff',
            padding: '15px',
            borderRadius: '8px',
            border: '1px solid #ddd'
        })
    }

    render(): void {
        this.control_form.set_uri("/cube/to_form_column_view", () => {
            this.control_form.child_map.axis.set_label("旋转轴")
            this.control_form.child_map.layer.set_label("层号")
            this.control_form.child_map.rotate.set_label("旋转方向")
            this.control_form.child_map.steps.set_label("打乱步数")
            this.control_form.child_map.steps.set_value("10")
        })
        this.title.set_html("魔方可视化 - 点击按钮开始")
        this.handle_new()
    }

    handle_new(): void {
        web_dom.post("/cube/new", { n: 2 }, (data: any) => {
            this.update_state(data.value)
            this.action_history = []
            this.title.set_html("新建魔方完成 - 开始操作")
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