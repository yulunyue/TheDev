import constant from "./model/constant"
import dev from "./demo/dev";
import "./app.css"
constant.init()
let route = { dev }[constant.get_route('main')]()
constant.init_body(route.div_el)
