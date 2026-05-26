import { Dom, Style, Fn2Void, Node } from "./cls"
import { HttpService } from "./http_service"
import { DomService } from "./dom_service"

class WebDom extends HttpService {
    dom = new DomService()

    get_body!: () => HTMLElement
    set_el_style!: (el: any, style: Style) => void
    createElement!: (node_type: string) => HTMLElement
    createElementNS!: (node_type: string) => SVGElement
    get_location!: () => string
    bind_click!: (dom: Dom, call_back: any) => void
    bind_dbclick!: (dom: Dom, call_back: any) => void
    bind_input!: (dom: Dom, call_back: any) => void
    bind_change!: (dom: Dom, call_back: any) => void
    bind_mousemove!: (dom: Dom, call_back: any) => void
    bind_mouseenter!: (dom: Dom, call_back: any) => void
    bind_mouseleave!: (dom: Dom, call_back: any) => void
    bind_mouseup!: (dom: Dom, call_back: any) => void
    bind_mousedown!: (dom: Dom, call_back: any) => void
    bind_drag!: (dom: any, call_back: any) => void
    next_frame!: (callback: any) => void
    set_time_out!: (f: any, t: number) => void
    calc_text_width!: (s: string, family: any, size: any) => number

    bind_key(call_back: Fn2Void<string, KeyboardEvent>) {
        window.document.body.onkeydown = (e: KeyboardEvent) => {
            call_back("keydown", e)
        }
        window.document.body.onkeyup = (e: KeyboardEvent) => {
            call_back("up", e)
        }
    }
    body_click(call_back: any) {
        this.get_body().addEventListener('click', call_back)
    }

    loop_task: { [key: string]: any } = {}
    loop_state = "stop"
    loop_count = 0
    run_all_task() {
        for (var key in this.loop_task) {
            if (this.loop_task[key][1] == 0) {
                continue
            }
            if (this.loop_count % this.loop_task[key][1] == 0) {
                this.loop_task[key][1] = this.loop_task[key][0]() | 0
            }
        }
        if (this.loop_state == 'runing') {
            this.loop_count = (this.loop_count + 1) % 3600
            requestAnimationFrame(() => { this.run_all_task() })
        }
    }
    add_task(name: string, func: any, loop_count: number) {
        this.loop_task[name] = [func, loop_count]
        if (this.loop_state == 'stop') {
            this.loop_state = 'runing'
            this.run_all_task()
        }
    }
}

const proto = WebDom.prototype as any
const domProto = DomService.prototype as any
Object.getOwnPropertyNames(domProto).forEach(name => {
    if (name !== 'constructor') {
        proto[name] = domProto[name]
    }
})

export default new WebDom()
