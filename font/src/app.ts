import constant from "./model/constant"
import web_dom from "./base/web/web_dom";
import algo from "./demo/algo";
import api from "./demo/api";
import dev from "./demo/dev";
import talk from "./demo/talk";
import chess from "./demo/game/chess";
import todo from "./demo/todo/todo_main";
import task from "./demo/task/task_main";
import { Data } from "./base/components/export";
import "./app.css"
constant.init()
let route = {
    algo, api, dev, chess, talk, todo, task
}[constant.get_route('main')]
route().mount(web_dom.get_body()).render()
// constant.init_body(route.div_el)
