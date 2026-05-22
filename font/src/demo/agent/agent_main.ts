import {
    FlexRow, FlexColumn, Div, Constant, Node, web_dom,
    Button, Input, Pre, Span, Label,
    web_socket, Ct,
} from "../../base/components/export"

export class AgentMain extends FlexColumn {
    agent_list: FlexColumn
    command_input: Input
    exec_btn: Button
    output_panel: Pre
    status_bar: Span
    current_agent: string = ""
    current_cmd_id: string = ""

    init_style(): void {
        this.full()
        this.set_style({
            height: "100vh",
            overflow: "hidden"
        })
        this.agent_list.set_style({
            width: 200,
            minWidth: 200,
            borderRight: "1px solid #ccc",
            overflowY: "auto"
        })
        this.command_input.set_style({
            flex: 1,
            minWidth: 200
        })
        this.output_panel.set_style({
            flex: 1,
            overflow: "auto",
            whiteSpace: "pre-wrap",
            fontFamily: "monospace",
            fontSize: "12px"
        })
        this.status_bar.set_style({
            minWidth: 100
        })
    }

    init_node(): void {
        this.agent_list = new FlexColumn()
        this.command_input = new Input().set_placeholder("输入命令")
        this.exec_btn = new Button().set_html("执行")
        this.output_panel = new Pre()
        this.status_bar = new Span()
        
        const header = new FlexRow().add_children([
            this.command_input,
            this.exec_btn,
            this.status_bar,
        ])
        
        const left_panel = new FlexColumn().add_children([
            new Span().set_html("Agent 列表"),
            this.agent_list,
        ])
        
        const right_panel = new FlexColumn().add_children([
            header,
            this.output_panel,
        ])
        
        this.add_children([
            new FlexRow().add_children([
                left_panel,
                right_panel.set_size(1),
            ]).set_size(1),
        ])
    }

    init_event(): void {
        this.exec_btn.on_click(() => this.exec_command())
        this.load_agents()
    }

    load_agents(): void {
        web_dom.post("/agent/list", {}, (data: Node) => {
            this.render_agents(data.data.agents || [])
        })
    }

    render_agents(agents: any[]): void {
        this.agent_list.clear_children()
        for (const agent of agents) {
            const item = new Label()
                .set_html(`${agent.agent_id} (${agent.platform || "unknown"})`)
                .set_style({
                    padding: "8px",
                    cursor: "pointer",
                    borderBottom: "1px solid #eee"
                })
            item.on_click(() => {
                this.current_agent = agent.agent_id
                this.status_bar.set_html(`选中: ${agent.agent_id}`)
                this.highlight_agent_item(item)
            })
            this.agent_list.add_child(item)
        }
    }

    highlight_agent_item(item: Label): void {
        for (const child of this.agent_list.childs) {
            if (child instanceof Label) {
                child.set_style({ background: "" })
            }
        }
        item.set_style({ background: "#e0e0e0" })
    }

    exec_command(): void {
        if (!this.current_agent) {
            this.status_bar.set_html("请先选择 Agent")
            return
        }
        const command = this.command_input.get_value()
        if (!command) {
            this.status_bar.set_html("请输入命令")
            return
        }
        
        this.output_panel.set_html("")
        web_dom.post("/agent/exec", {
            agent_id: this.current_agent,
            command: command,
            timeout: 60
        }, (data: Node) => {
            this.current_cmd_id = data.data.cmd_id
            this.status_bar.set_html(`执行中: ${this.current_cmd_id}`)
            this.subscribe_output(this.current_cmd_id)
        })
    }

    subscribe_output(cmd_id: string): void {
        const topic = `${Ct.TOPIC_AGENT_OUTPUT}.${cmd_id}`
        web_socket.sub(topic, (msg: any) => {
            this.handle_output(msg)
        })
    }

    handle_output(msg: any): void {
        const msgType = msg.type
        const data = msg.data?.data || ""
        const exitCode = msg.data?.exit_code
        
        if (msgType === Ct.MSG_EXEC_STDOUT) {
            this.append_output(data)
        } else if (msgType === Ct.MSG_EXEC_STDERR) {
            this.append_output(`[stderr] ${data}`)
        } else if (msgType === Ct.MSG_EXEC_DONE) {
            this.status_bar.set_html(`完成: exit_code=${exitCode}`)
            web_socket.un_sub(`${Ct.TOPIC_AGENT_OUTPUT}.${this.current_cmd_id}`)
        }
    }

    append_output(text: string): void {
        const current = this.output_panel.el.textContent || ""
        this.output_panel.set_html(current + text)
        this.output_panel.el.scrollTop = this.output_panel.el.scrollHeight
    }

    render(): void {
        this.load_agents()
    }
}

export default function () {
    return new AgentMain()
}