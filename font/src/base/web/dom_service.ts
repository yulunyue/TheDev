import { Style, Dom } from "./cls"

export class DomService {
    get_body() {
        return document.body
    }
    set_el_style(el: any, style: Style) {
        for (var key in style) {
            let v = style[key]
            if (typeof (v) == 'number') {
                v = v + "px"
            }
            el.style[key] = v
        }
    }
    createElement(node_type: string) {
        return document.createElement(node_type)
    }
    createElementNS(node_type: string) {
        return document.createElementNS("http://www.w3.org/2000/svg", node_type)
    }
    get_location() {
        return location.href
    }
    bind_click(dom: Dom, call_back: any) {
        dom.onclick = (e) => {
            e.stopPropagation()
            call_back()
        }
    }
    bind_dbclick(dom: Dom, call_back: any) {
        dom.ondblclick = (e) => {
            e.stopPropagation()
            call_back()
        }
    }
    bind_input(dom: Dom, call_back: any) {
        dom.oninput = call_back
    }
    bind_change(dom: Dom, call_back: any) {
        dom.onchange = call_back
    }
    bind_mousemove(dom: Dom, call_back: any) {
        dom.onmousemove = call_back
    }
    bind_mouseenter(dom: Dom, call_back: any) {
        dom.onmouseenter = call_back
    }
    bind_mouseleave(dom: Dom, call_back: any) {
        dom.onmouseleave = call_back
    }
    bind_mouseup(dom: Dom, call_back: any) {
        dom.onmouseup = call_back
    }
    bind_mousedown(dom: Dom, call_back: any) {
        dom.onmousedown = call_back
    }
    bind_drag(dom: any, call_back: any) {
        dom.onmousedown = (e: any) => {
            dom._drag_state = true
            dom._drag_start_x = e.x
            dom._drag_start_y = e.y
            call_back("start")
        }
        document.body.onmousemove = (e: any) => {
            if (dom._drag_state) {
                call_back("move", e.x - dom._drag_start_x, e.y - dom._drag_start_y)
            }
        }
        document.body.onmouseup = (e: any) => {
            dom._drag_state = false
            if (dom._drag_state) {
                call_back("end")
            }
        }
    }
    next_frame(callback: any) {
        requestAnimationFrame(callback)
    }
    set_time_out(f: any, t: number) {
        setTimeout(f, t)
    }
    _text_cav: any
    _text_ctx: any
    calc_text_width(s: string, family: any, size: any) {
        if (!this._text_cav) {
            this._text_cav = document.createElement("canvas");
            this._text_ctx = this._text_cav.getContext("2d");
        }
        this._text_ctx.font = `${size} ${family}`;
        let metrics = this._text_ctx.measureText(s);
        let actual = Math.abs(metrics.actualBoundingBoxLeft) + Math.abs(metrics.actualBoundingBoxRight)
        return Math.max(metrics.width, actual)
    }
}
