import { Style, Fn1Void, Dom, Node, Fn2Void, to_node } from "./cls"
import Ut from "../tool/util"
import F from "../tool/fun"
import Ct from "./constant"
import dlg from "../components/dom/dialog"

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
    get_local(key: string, call?: any) {
        let ret = to_node(JSON.parse(localStorage.getItem("yly_" + key)))
        if (ret) {
            call?.(ret)
        }
        return ret
    }
    get_loacl_str(key: string) {
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
        console.log("set_local", key, value)
        if (typeof value == "object") {
            localStorage.setItem("yly_" + key, JSON.stringify(value))
        } else {
            localStorage.setItem("yly_" + key, value)
        }
    }
    web_host: string
    web_port: number

    url_param: any
    prefix: string
    init_href() {
        this.url_param = {}
        var location_href2 = this.get_location().split('?')
        var hrefs = location_href2[0].split('/')
        var ip_ports = hrefs[2].split(':')
        this.web_host = ip_ports[0]
        this.web_port = parseInt(ip_ports[1])
        if (this.web_port == 8080) {
            this.web_port = 9999
        }
        Ut.extend(this.url_param, Ut.url_to_json(location_href2[1]))
        let bk_host = this.web_host
        this.prefix = 'http://' + bk_host + ":" + this.web_port
    }
    url(path: string) {

        return this.prefix + path
    }
    get_wh_scale() {
        return window.innerWidth / window.innerHeight
    }
    get_window_size() {
        return { width: window.innerWidth, height: window.innerHeight }
    }
    headers = {}
    xml_http_request(method: string, path: string, data: any, call_back: any) {

        let url = this.url(path)
        // dlg.open_loading()
        let req = new XMLHttpRequest()
        if (method == this.HTTP_GET_METHOD) {
            let path = Ut.object_to_get_param(data, url)
            req.open(method, path);
            req.send();
        } else if (method == this.HTTP_POST_METHOD) {
            req.open(method, url);
            req.setRequestHeader(this.HTTP_CONTENT_TYPE_KEY, this.HTTP_CONTENT_TYPE_JSON)
            req.setRequestHeader(Ct.the_dev_user, this.get_loacl_str(Ct.username))
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
                if (method == this.HTTP_GET_METHOD) {
                    call_back(req.responseText)
                    return
                }
                let data: any = this.hander_res(JSON.parse(req.responseText))
                if (data && data.code > 300) {
                    alert(data.code + '->' + data.title)
                }
                else if (data) {
                    // call_back(new Node().set_option(data))
                    call_back(data)
                }
                // dlg.close()
            }
        }

    }

    hander_res(node: Node) {
        return node
    }
    post(url: string, data: any, call_back?: Fn1Void<Node>) {
        this.xml_http_request(this.HTTP_POST_METHOD, url, data, call_back)
    }
    post_file(path: string, formData: FormData, call_back: any) {
        const xhr = new XMLHttpRequest();
        let url = this.url(path)
        xhr.open('POST', url, true);
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                dlg.open_progress_bar(percent)
            }
        });

        // 完成监听
        xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                const data = JSON.parse(xhr.responseText);
                call_back(data)
            } else {

            }
            dlg.close()
        });

        // 错误监听
        xhr.addEventListener('error', () => {
            dlg.close()
        });
        xhr.send(formData);

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
    bind_dbclick(dom: Dom, call_back: any) {
        dom.ondblclick = (e) => {
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
    get_file(path: string, call_back: any) {
        this.post("/app/tool/file/read", { path: path }, (ret) => {
            call_back(ret.value)
        })
    }
    get_json(path: string, call_back: any) {
        this.get_file(path, (data: any) => {
            call_back(JSON.parse(data))
        })
    }

    get_ts(path: string, call_back: any) {
        this.get_file(path, (data: any) => {
            call_back(F.eval_ts(data))
        })
    }
    put_json(path: string, data: any, call_back: any) {
        this.post("/app/tool/file/write", { path: path, data: data }, (ret) => {
            call_back(ret)
        })
    }

}
export default new WebDom()