import web_dom from "../base/web/web_dom"
import util from "../base/tool/util"
import { Dialog } from "../base/tool/dialog"
class Constant {
    web_host: string
    web_port: number
    web_socket_port: string
    web_backend_port: number
    data: any
    init() {
        this.data = {}
        this.init_href()
    }
    get_route(route?: string) {
        return this.data["route"] || route
    }
    init_href() {
        var location_href = web_dom.get_location()
        var hrefs = location_href.split('/')
        var ip_ports = location_href[2].split(':')
        this.web_host = ip_ports[0]
        this.web_port = parseInt(ip_ports[1])
        util.extend(this.data, util.url_to_json(hrefs[hrefs.length - 1].split('?').pop()))
    }
    init_local() {

    }
    init_body(body: any) {
        let dialog = new Dialog().set_html(
            "xx"
        ).mount(
            web_dom.get_body()
        ).move_rb()
        web_dom.bind_mousemove(body, (e: any) => {
            dialog.set_html(e.x + "xx" + e.y)
        })

    }
}
export default new Constant()