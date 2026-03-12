import web_dom from "../base/web/web_dom"

import { Div } from "../base/components/dom/div"
class Constant {
    web_socket_port: string
    web_backend_port: number
    init() {
        web_dom.init_href()
    }
    get_route(route?: string) {
        return web_dom.url_param["route"] || route
    }

    init_local() {

    }
    init_body(body: any) {
        let dialog = new Div().set_html(
            "x"
        ).set_div_style({
            position: "fixed",
            right: 0,
            top: 0
        }).mount(
            web_dom.get_body()
        )
        web_dom.bind_mousemove(body, (e: any) => {
            dialog.set_html(e.x + "x" + e.y)
        })

    }
}
export default new Constant()