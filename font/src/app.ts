import constant from "./model/constant"
import web_dom from "./base/web/web_dom";
import algo from "./demo/algo";
import api from "./demo/api";
import dev from "./demo/dev";
import "./app.css"
constant.init()
let route = {
    algo, api, dev
}[constant.get_route('main')]().mount(web_dom.get_body()).emit_mount()
// constant.init_body(route.div_el)
