import { Style, Fn1Void } from "./cls"

class WebDom {
    HTTP_GET_METHOD: string = "GET"
    HTTP_POST_METHOD: string = "POST"
    HTTP_CONTENT_TYPE_KEY: string = "Content-type"
    HTTP_CONTENT_TYPE_JSON: string = "application/json"
    HTTP_STATE_FINISH: number = 4

    get_body() {
        return document.body
    }
    set_el_style(el: any, style: Style) {
        for (var key in style) {
            let v = style[key]
            if (typeof (v) == 'number') {
                if (0 < v && v <= 1) {
                    v = v * 100 + "%"
                } else {
                    v = v + "px"
                }
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
    get_local(key: string) {
        return localStorage.getItem(key)
    }
    set_local(key: string, value: any) {
        if (typeof value == "object") {
            localStorage.setItem(key, JSON.stringify(value))
        } else {
            localStorage.setItem(key, value)
        }
    }
    xml_http_request(method: string, path: string, data: any, call_back: any) {
        let req = new XMLHttpRequest()
        req.open(method, path)
        if (method == this.HTTP_POST_METHOD) {

        } else if (method == this.HTTP_POST_METHOD) {
            req.setRequestHeader(this.HTTP_CONTENT_TYPE_KEY, this.HTTP_CONTENT_TYPE_JSON)
        }
        req.send(data)
        req.onreadystatechange = (ev: any) => {
            if (req.readyState == this.HTTP_STATE_FINISH) {
                if (req.getResponseHeader(this.HTTP_CONTENT_TYPE_JSON).includes(this.HTTP_CONTENT_TYPE_JSON)) {
                    call_back(JSON.parse(req.responseText))
                } else {
                    call_back(req.responseText)
                }
            }
        }
    }
    bind_click(dom: HTMLElement, call_back: any) {
        dom.onclick = call_back
    }
    bind_mousemove(dom: HTMLElement, call_back: any) {
        dom.onmousemove = call_back
    }
    bind_mouseup(dom: HTMLElement, call_back: any) {
        dom.onmouseup = call_back
    }
    bind_mousedown(dom: HTMLElement, call_back: any) {
        dom.onmousedown = call_back
    }
    loop_task = {}
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
export default new WebDom()