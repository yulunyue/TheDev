import { Style, Fn1Void, Dom, Node, Fn2Void } from "./cls"
import Ut from "../tool/util"
import Ct from "./constant"
class WebDom {
    HTTP_GET_METHOD: string = "GET"
    HTTP_POST_METHOD: string = "POST"
    HTTP_CONTENT_TYPE_KEY: string = "Content-type"
    HTTP_CONTENT_TYPE_JSON: string = "application/json"
    HTTP_STATE_FINISH: number = 4
    constructor() {

    }
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
        return localStorage.getItem("yly_" + key)
    }
    get_param(key: string, defult_value?: any) {
        if (!(key in this.url_param)) {
            return defult_value
        }
        return this.url_param[key]
    }
    set_local(key: string, value: any) {
        if (value == undefined || value == null) {
            return
        }
        if (typeof value == "object") {
            localStorage.setItem("yly_" + key, JSON.stringify(value))
        } else {
            localStorage.setItem("yly_" + key, value)
        }
    }
    web_host: string
    web_port: number
    bk_port: string = "9999"
    url_param: any
    prefix: string
    init_href() {
        this.url_param = {}
        var location_href2 = this.get_location().split('?')
        var hrefs = location_href2[0].split('/')
        var ip_ports = hrefs[2].split(':')
        this.web_host = ip_ports[0]
        this.web_port = parseInt(ip_ports[1])
        Ut.extend(this.url_param, Ut.url_to_json(location_href2[1]))
        let bk_host = this.web_host
        if (bk_host.endsWith('github.io')) {
            bk_host = '1.14.93.140'
        }
        console.log(this.url_param)
        this.prefix = 'http://' + bk_host + ":" + this.bk_port
    }
    url(path: string) {
        return this.prefix + path
    }
    get_wh_scale() {
        return window.innerWidth / window.innerHeight
    }
    headers = {}
    xml_http_request(method: string, path: string, data: any, call_back?: Fn1Void<Node>) {
        let url = this.url(path)
        let mock_data = Ct.get_mock_data(url, data)
        if (mock_data) {
            return call_back(mock_data)
        }
        let req = new XMLHttpRequest()
        if (method == this.HTTP_GET_METHOD) {
            req.open(method, Ut.object_to_get_param(data, path));
            req.send();
        } else if (method == this.HTTP_POST_METHOD) {
            req.open(method, url);
            req.setRequestHeader(this.HTTP_CONTENT_TYPE_KEY, this.HTTP_CONTENT_TYPE_JSON)
            for (var key in this.headers) {
                if (this.headers[key]) {
                    req.setRequestHeader(key, this.headers[key]);
                }
            }
            try {
                let dt = JSON.stringify(data)
                req.send(dt)
            } catch (e: any) {
                alert('post:' + path + data)
            }

        }
        req.onreadystatechange = (ev: any) => {
            if (req.readyState == this.HTTP_STATE_FINISH) {

                let data = this.hander_res(JSON.parse(req.responseText))
                if (data && data.code > 300) {
                    alert(data.code + '->' + data.title)
                }
                else if (data) {
                    // call_back(new Node().set_option(data))
                    call_back(data)
                }
            }
        }

    }
    hander_res(node: Node) {
        return node
    }
    post(url: string, data: any, call_back?: Fn1Void<Node>) {
        this.xml_http_request(this.HTTP_POST_METHOD, url, data, call_back)
    }
    get(url: string, data: any, call_back?: Fn1Void<Node>) {
        this.xml_http_request(this.HTTP_GET_METHOD, url, data, call_back)
    }
    bind_click(dom: Dom, call_back: any) {
        dom.onclick = (e) => {
            e.stopPropagation()
            call_back()
        }
    }
    next_frame(callback: any) {
        requestAnimationFrame(callback)
    }
    bind_key(call_back: Fn2Void<string, KeyboardEvent>) {
        window.document.body.onkeydown = (e: KeyboardEvent) => {
            call_back("keydown", e)
        }
        window.document.body.onkeyup = (e: KeyboardEvent) => {
            call_back("up", e)
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
    body_click(call_back: any) {
        this.get_body().onclick = () => {
            call_back()
        }
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
export default new WebDom()