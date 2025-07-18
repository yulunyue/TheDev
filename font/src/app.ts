import constant from "./model/constant"
import web_dom from "./base/web/web_dom";
import graph from "./demo/graph";
import algo from "./demo/algo";
import dyn from "./demo/dyn";
import api from "./demo/api";
import manage from "./demo/secmaster/manage";
import dev from "./demo/dev";
import "./app.css"
constant.init()
let route = {
    graph, algo, dyn, api, dev,
    manage
}[constant.get_route('main')]().mount(web_dom.get_body()).emit_mount()
// constant.init_body(route.div_el)
