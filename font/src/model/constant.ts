import web_dom from "../base/web/web_dom"
class Constant {
    web_host: string
    web_port: number
    web_socket_port: string
    web_backend_port: number
    init() {
        this.init_href()
    }
    init_href() {
        console.log(web_dom.get_location())
    }
}
export default new Constant()