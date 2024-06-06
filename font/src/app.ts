import constant from "./model/constant"
import dev from "./demo/dev";
constant.init()
let route = { dev }[constant.get_route('main')]
route()
