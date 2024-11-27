import web_dom from "./web_dom"
import { Node } from "./cls"
import Data from "../tool/data"
export class NetKakfa {
    _client: WebSocket
    sub_call_back: any
    constructor() {
        this.sub_call_back = {}
    }
    get_client() {
        if (!this._client) {
            web_dom.web_host
            this._client = new WebSocket("ws://" + web_dom.web_host + ":" + web_dom.bk_port + "/ws")
            this._client.onopen = () => {
                console.log("web_socket_open")
                this.login()
                
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
    send_data(tp:string,data:any){
        
    }
    login(){
        Data.get_user_name((user_name:string)=>{
            this.send_data("login",{user_name})
        })
    }
    hander_msg(data: any) {
        let obj = JSON.parse(data)
        let node = new Node().set_option(obj)
        if (node.type in this.sub_call_back) {
            this.sub_call_back[node.type](node)
        } else {
            console.warn(data)
        }
    }
    sub(topic_name: string, call_back: any) {
        this.get_client()
        this.sub_call_back[topic_name] = call_back
        return this
    }
}
export default new NetKakfa()