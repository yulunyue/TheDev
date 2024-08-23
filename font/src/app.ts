import constant from "./model/constant"
import web_dom from "./base/web/web_dom";
import dev from "./demo/dev";
import algo from "./demo/algo";
import "./app.css"
constant.init()
let route = { dev, algo }[constant.get_route('main')]().mount(web_dom.get_body()).on_mount()
constant.init_body(route.div_el)
