import {
    FlexRow, FlexColumn, Node, web_dom,
    Input, Pre, Span, Button,
    web_socket, Ct, Search,
} from "../../base/components/export"

const SCROLL_DELAY_MS = 200

export class AgentMain extends FlexColumn {
    agent_search: Search
    command_input: Input
    reset_btn: Button
    output_panel: Pre
    status_bar: Span
    top_bar: FlexRow
    current_agent: string = ""
    is_executing: boolean = false
    private _viewport_bound = false

    private get _vv(): VisualViewport | null {
        return (window as any).visualViewport
    }

    init_node(): void {
        this.agent_search = new Search().set_title("搜索 Agent")
        this.command_input = new Input().set_placeholder("输入命令")
        this.reset_btn = new Button().set_value("重置")
        this.output_panel = new Pre()
        this.status_bar = new Span()

        this.top_bar = new FlexRow().add_children([
            this.agent_search,
            this.status_bar,
            this.reset_btn,
        ])

        this.add_children([
            this.top_bar,
            this.output_panel.set_size(1),
            this.command_input,
        ])
    }

    init_style(): void {
        super.init_style()
        this.full()
        this.set_style({
            height: "100vh",
            overflow: "hidden"
        })
        this.top_bar.set_style({
            alignItems: "center",
        })
        this.agent_search.set_style({
            width: 200,
        })
        this.reset_btn.set_style({
            cursor: "pointer",
            fontSize: "13px",
        })
        this.output_panel.set_style({
            overflow: "auto",
            whiteSpace: "pre-wrap",
            fontFamily: "monospace",
            fontSize: "12px",
            minHeight: 0,
        })
        this.status_bar.set_style({
            minWidth: 100,
            flex: 1,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
        })
        this.command_input.set_style({
            width: "100%",
        })
    }

    init_event(): void {
        this.agent_search.on_change((key: string, src: any, value: any) => {
            this.switch_agent(value)
        })
        this.command_input.on_key_down((e: KeyboardEvent) => {
            if (e.key === "Enter") {
                this.exec_command()
            }
        })
        this.command_input.on_click(() => {
            this.scroll_input_into_view()
        })
        this.reset_btn.on_click(() => {
            this.output_panel.set_html("")
            this.is_executing = false
            this.status_bar.set_html("已重置")
            if (this.current_agent) {
                web_dom.post("/agent/kill", { agent_id: this.current_agent })
            }
        })
    }

    switch_agent(agent_id: string): void {
        if (this.current_agent) {
            web_socket.un_sub(`${Ct.TOPIC_AGENT_OUTPUT}.${this.current_agent}`)
        }
        this.current_agent = agent_id
        this.status_bar.set_html(`选中: ${agent_id}`)
        this.output_panel.set_html("")
        this.is_executing = false
        if (!agent_id) return

        web_socket.sub(`${Ct.TOPIC_AGENT_OUTPUT}.${agent_id}`, (msg: any) => {
            this.handle_output(msg)
        })
        this.load_history(agent_id)
    }

    load_history(agent_id: string): void {
        web_dom.post("/agent/history", { agent_id, limit: 60 }, (data: Node) => {
            const records = data.children || []
            for (const r of records) {
                const d = r.data
                this.append_output(`$ ${d.command}\n`)
                if (d.output) {
                    this.append_output(d.output)
                }
                this.append_output(`exit_code: ${d.exit_code}  (${new Date(d.start_time * 1000).toLocaleTimeString()})\n\n`)
            }
        }, () => { })
    }

    exec_command(): void {
        if (this.is_executing) {
            this.status_bar.set_html("正在执行中，请先停止")
            return
        }

        if (!this.current_agent) {
            this.status_bar.set_html("请先选择 Agent")
            return
        }
        const command = this.command_input.get_value()
        if (!command) {
            this.status_bar.set_html("请输入命令")
            return
        }
        this.is_executing = true
        web_dom.post("/agent/exec", {
            agent_id: this.current_agent,
            command: command,
            timeout: 60
        }, (o: Node) => {
            if (o.ok) {
                this.append_output(`$ ${command}\n`)
                this.command_input.set_value("")
                this.status_bar.set_html("执行中")
            } else {
                this.is_executing = false
                this.status_bar.set_html(`错误: ${o.title}`)
            }
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
            this.is_executing = false
            const timeStr = new Date().toLocaleTimeString()
            this.status_bar.set_html(`完成: exit_code=${exitCode}  (${timeStr})`)
            this.append_output(`exit_code: ${exitCode}\n\n`)
        }
    }

    append_output(text: string): void {
        const pre = this.output_panel.el
        pre.insertAdjacentText("beforeend", text)
        pre.scrollTop = pre.scrollHeight
    }

    scroll_input_into_view(): void {
        setTimeout(() => {
            const inputEl = this.command_input.el
            const rect = inputEl.getBoundingClientRect()
            const vv = this._vv
            if (vv && rect.bottom > vv.height) {
                window.scrollTo(0, window.scrollY + rect.bottom - vv.height + 10)
            }
        }, SCROLL_DELAY_MS)
    }

    render(): void {
        this.agent_search.set_option({ url: "/agent/list", key: "agent_id", id: "agent_search" })
        const vv = this._vv
        if (vv) {
            this.set_style({ height: `${vv.height}px` })
            if (this._viewport_bound) return
            this._viewport_bound = true
            vv.addEventListener("resize", () => {
                this.set_style({ height: `${vv.height}px` })
                if (document.activeElement === this.command_input.el) {
                    this.scroll_input_into_view()
                }
            })
        }
    }
}

export default function () {
    return new AgentMain()
}
