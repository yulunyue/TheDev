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
    constructor() {
        this.sub_call_back = {}
    }
    get_client(call: any) {
        if (!this._client) {
            this._client = new WebSocket("ws://" + web_dom.web_host + ":" + web_dom.web_port + "/ws")
            this._client.onopen = () => {
                console.log("web_socket_open")
                this.login()
                call()
            }
            this._client.onclose = function () {
                console.log("web_socket_open");
            };
            this._client.onmessage = (evt) => {
                this.recv_hock?.(evt.data)
                this.hander_msg(evt.data)
            };
        } else {
            call()
        }
        return this._client
    }
    login() {
        Data.get_user_name((username: string) => {
            this.send_data(Constant.METHOD_LOGIN, username)
        })
    }
    send_data(tp: string, value: any) {
        this.send_hock?.(tp, value)
        this.get_client(() => {
            this._client.send(JSON.stringify({
                type: tp,
                value: value
            }))
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
        this.get_client(() => {
            this.sub_call_back[method] = call_back
        })
        return this
    }
}
export default new NetKakfa()