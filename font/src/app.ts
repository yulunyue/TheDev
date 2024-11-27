import constant from "./model/constant"
import web_dom from "./base/web/web_dom";
import dev from "./demo/dev";
import algo from "./demo/algo";
import guss_num from "./demo/game/guss_num";
import "./app.css"
constant.init()
let route = { dev, algo, guss_num }[constant.get_route('main')]().mount(web_dom.get_body()).emit_mount()
// constant.init_body(route.div_el)
