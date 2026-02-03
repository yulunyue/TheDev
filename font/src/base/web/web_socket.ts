import web_dom from "./web_dom"
import { Node } from "./cls"
import Data from "../tool/data"
export class NetKakfa {
    _client: WebSocket
    _login: any
    sub_call_back: any
    constructor() {
        this.sub_call_back = {}
    }
    get_client() {
        if (!this._client) {
            this._client = new WebSocket("ws://" + web_dom.web_host + ":" + web_dom.web_port + "/ws")
            this._client.onopen = () => {
                console.log("web_socket_open")
                this.do_login()

            }
            this._client.onclose = function () {
                console.log("web_socket_open");
            };
            this._client.onmessage = (evt) => {
                this.hander_msg(evt.data)
            };
        }
        return this._client
    }
    send_data(tp: string, data: any) {
        this._client.send(JSON.stringify({
            type: tp,
            data: data
        }))
    }
    do_login() {
        Data.get_user_name((user_name: string) => {
            this.send_data("login", { user_name })
        })
    }
    login(call_back: any) {
        this._login = call_back
        return this
    }
    hander_msg(data: any) {
        let obj = JSON.parse(data)
        if (obj.type == 'login') {
            this._login?.(obj.data.user_name)
        } else if (obj.type in this.sub_call_back) {
            this.sub_call_back[obj.type](obj.data)
        } else {
            console.log(data)
        }
    }
    sub(topic_name: string, call_back: any) {
        this.get_client()

        this.sub_call_back[topic_name] = call_back
        return this
    }
}
export default new NetKakfa()