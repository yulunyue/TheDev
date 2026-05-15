import web_dom from "./web_dom"
import { Node } from "./cls"
import Data from "../tool/data"
import { Constant } from "../components/export"

export class NetKakfa {
    _client: WebSocket
    sub_call_back: any
    connect_state: string
    pending_calls: any[]

    constructor() {
        this.sub_call_back = {}
        this.pending_calls = []
    }

    connect(call: any) {
        if (this.connect_state == 'ok') {
            call()
            return
        }
        if (this.connect_state == 'connecting') {
            this.pending_calls.push(call)
            return
        }
        this.connect_state = "connecting"
        this._client = new WebSocket("ws://" + web_dom.web_host + ":" + web_dom.web_port + "/ws")

        this._client.onopen = () => {
            console.log("web_socket_open")
            this.login(() => {
                call()
                for (let c of this.pending_calls) {
                    c()
                }
                this.pending_calls = []
            })
            this.connect_state = "ok"
        }

        this._client.onclose = () => {
            console.log("web_socket_close")
            this.connect_state = ""
            setTimeout(() => {
                this.connect(call)
            }, 1000)
        }

        this._client.onmessage = (evt) => {
            this.handler_msg(evt.data)
        }
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
        this.connect(() => {
            this.write_data(tp, value)
        })
    }

    handler_msg(data: any) {
        let obj = JSON.parse(data)
        if (obj.type in this.sub_call_back) {
            this.sub_call_back[obj.type](obj.value, obj.from)
        } else {
            console.log(data)
        }
    }

    sub(key: string, fun: any) {
        let param = {}
        param[key] = fun
        this.sub_topics(param)
    }
    sub_topics(topics: any) {
        var methods = []
        for (var method in topics) {
            this.sub_call_back[method] = topics[method]
            methods.push(method)
        }
        this.send_data(Constant.METHOD_SUB, method)
        return this
    }
    un_sub(method: string) {
        this.send_data(Constant.METHOD_UN_SUB, method)
        this.sub_call_back[method] = null
        return this
    }
}

export default new NetKakfa()