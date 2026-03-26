import { Div } from "./div";
import Constant from "../../../web/constant"
import { Row } from "./row";
import { DivFactory } from "./div_factory";
export class FlexDiv extends Div {

    get_direction() {
        return -1
    }

    init_style() {
        this.set_div_style({
            flexDirection: this.get_direction() == Constant.VERTICAL ? "row" : "column",
            display: "flex",
            justifyContent: "space-around",
            // alignContent: "center",

        })
    }
    set_center() {
        this.set_div_style({
            alignItems: "center"
        })
        return this
    }

    render_option(): void {
        if (this.option.childs && this.option.childs.length) {
            this.clear()
            let childs = []
            for (var i = 0; i < this.option.childs.length; i++) {
                let o = this.option.childs[i]
                childs.push(DivFactory.new_div(o.type, o.key).set_option(o))
            }
            this.add_childs(childs)
        }

    }

} 