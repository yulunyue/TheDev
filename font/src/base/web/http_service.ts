import { Style, Fn1Void, Dom, Node, Fn2Void, to_node } from "./cls"
import Ut from "../tool/util"
import F from "../tool/fun"
import Ct from "./constant"
import dlg from "../components/dom/dialog"

export class HttpService {
    HTTP_GET_METHOD: string = "GET"
    HTTP_POST_METHOD: string = "POST"
    HTTP_CONTENT_TYPE_KEY: string = "Content-type"
    HTTP_CONTENT_TYPE_JSON: string = "application/json"
    HTTP_STATE_FINISH: number = 4

    get_local(key: string, handler_after: any) {
        this.get_local_str(key, handler_after, (v: string) => JSON.parse(v))
    }
    get_local_str(key: string, handler_after: any, handler_pre?: any) {
        let ret = localStorage.getItem("yly_" + key)
        if (ret) {
            if (handler_pre) {
                ret = handler_pre(ret)
            }
            handler_after(ret)
        }
    }
    get_local_data(key: string, default_value?: any) {
        let ret = localStorage.getItem("yly_" + key)
        if (ret) {
            try {
                return JSON.parse(ret)
            }
            catch {
                return ret
            }
        }
        return default_value
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
        var data = Ut.url_parse(location.href)
        var hrefs = data.path.split('/')
        var ip_ports = hrefs[2].split(':')
        this.web_host = ip_ports[0]
        Ut.extend(this.url_param, data.param)
        this.web_port = this.url_param.remote_port || parseInt(ip_ports[1])
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

    headers: { [key: string]: any } = {}
    xml_http_request(method: string, path: string, data: any, call_back: any, callback_finish: any) {
        let d = Ut.url_parse(path)
        let url = this.url(d.path)
        let req = new XMLHttpRequest()
        if (method == this.HTTP_GET_METHOD) {
            let path = Ut.object_to_get_param(data, url)
            req.open(method, path);
            req.send();
        } else if (method == this.HTTP_POST_METHOD) {
            req.open(method, url);
            req.setRequestHeader(this.HTTP_CONTENT_TYPE_KEY, this.HTTP_CONTENT_TYPE_JSON)
            req.setRequestHeader(Ct.the_dev_user, this.get_local_data(Ct.username))
            for (var key in this.headers) {
                if (this.headers[key]) {
                    req.setRequestHeader(key, this.headers[key]);
                }
            }
            try {
                let dt = JSON.stringify(data)
                dt = Ut.extend(dt, d.param)
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
                let data: any = this.handler_res(JSON.parse(req.responseText))
                callback_finish?.(data)
                if (data && data.code > 300) {
                    this.alert(data.code + '->' + data.title)
                }
                else if (data) {
                    call_back(data)
                }
            }
        }
    }
    alert(s: string) {
        alert(s)
    }
    handler_res(node: Node) {
        return node
    }
    post(url: string, data: any, call_back?: Fn1Void<Node>, call_back_error?: any) {
        this.xml_http_request(this.HTTP_POST_METHOD, url, data, call_back, call_back_error)
    }
    post_wait(url: string, data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            this.xml_http_request(this.HTTP_POST_METHOD, url, data, (v: any) => resolve(v), (data: any) => {
                if (data && data.code > 300) {
                    reject(data)
                }
            })
        })
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
        xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                const data = JSON.parse(xhr.responseText);
                call_back(data)
            }
            dlg.close()
        });
        xhr.addEventListener('error', () => {
            dlg.close()
        });
        xhr.send(formData);
    }
    get(url: string, data: any, call_back?: Fn1Void<Node>, callback_finish?: any) {
        this.xml_http_request(this.HTTP_GET_METHOD, url, data, call_back, callback_finish)
    }
    get_wait(url: string, data: any): Promise<string> {
        return new Promise((resolve, reject) => {
            this.xml_http_request(this.HTTP_GET_METHOD, url, data, resolve, reject)
        })
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
