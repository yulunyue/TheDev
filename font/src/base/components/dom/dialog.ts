import { Div } from "./div";
import Constant from "../../web/constant";
import web_dom from "../../web/web_dom"

export class Dialog extends Div {

    init_node() {
        web_dom.get_body().appendChild(this.div_el)
    }

    init_style(): void {
        this.set_div_style({
            position: "fixed",
            width: 1,
            height: 1,
            zIndex: "2",
            backgroundColor: "#8888"

        })
        this.hide()
    }


}
export default new Dialog()