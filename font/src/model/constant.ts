import web_dom from "../base/web/web_dom"
import util from "../base/tool/util"
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
    init_locaol() {

    }
}
export default new Constant()