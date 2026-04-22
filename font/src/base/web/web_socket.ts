import web_dom from "./web_dom"
import { Node } from "./cls"
import Data from "../tool/data"
import { Constant } from "../components/export"
export class NetKakfa {
    _client: WebSocket
    _login: any
    send_hock: any
    recv_hock: any
    sub_call_back: any
    connect_state: string
    constructor() {
        this.sub_call_back = {}

    }
    connect(call: any) {
        if (this.connect_state == 'ok') {
            call()
            return
        }
        if (this.connect_state == 'connecting') {
            return
        }
        this.connect_state = "connecting"
        this._client = new WebSocket("ws://" + web_dom.web_host + ":" + web_dom.web_port + "/ws")
        this._client.onopen = () => {
            console.log("web_socket_open")
            this.login(call)
            this.connect_state = "ok"
        }
        this._client.onclose = () => {
            console.log("web_socket_close");
            this.connect_state = ""
            setTimeout(() => {
                // this.retryCount++;
                this.connect(call);
            }, 1000);
        };
        this._client.onmessage = (evt) => {
            this.recv_hock?.(evt.data)
            this.hander_msg(evt.data)
        };

    }
    login(call: any) {
        Data.get_user_name((username: string) => {
            if (this.write_data(Constant.METHOD_LOGIN, username)) {
                call()
            }
        })
    }
    write_data(tp: string, value: any) {
        if (this._client && this._client.readyState === WebSocket.OPEN) {
            this._client.send(JSON.stringify({
                type: tp,
                value: value
            }))
            return true
        }
        return false
    }
    send_data(tp: string, value: any) {
        this.send_hock?.(tp, value)
        this.connect(() => {
            this.write_data(tp, value)
        })
    }
    hander_msg(data: any) {
        let obj = JSON.parse(data)
        if (obj.type in this.sub_call_back) {
            this.sub_call_back[obj.type](obj.from, obj.value)
        } else {
            console.log(data)
        }
    }
    sub(method: string, call_back: any) {
        this.send_data(Constant.METHOD_SUB, method)
        this.sub_call_back[method] = call_back
        return this
    }
}
export default new NetKakfa()