import constant from "./model/constant"
import web_dom from "./base/web/web_dom";
import graph from "./demo/graph";
import algo from "./demo/algo";
import dyn from "./demo/dyn";
import api from "./demo/api";
import guss_num from "./demo/game/guss_num";
import game_ab from "./demo/game/game_ab";
import manage from "./demo/secmaster/manage";
import dev from "./demo/dev";
import user from "./demo/user";
import game_connect_four from "./demo/game/game_connect_four";
import "./app.css"
constant.init()
let route = {
    graph, algo, guss_num, game_ab, dyn,
    game_connect_four, api, dev,
    manage, user
}[constant.get_route('main')]().mount(web_dom.get_body()).emit_mount()
// constant.init_body(route.div_el)
