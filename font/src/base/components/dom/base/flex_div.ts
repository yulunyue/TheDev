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
            justifyContent: "center",
            alignContent: "center",

        })
    }
    set_center() {
        this.set_div_style({
            alignItems: "center"
        })
        return this
    }

    render_option(): void {
        if (this.option.childs) {
            this.clear()
            let childs = []
            for (var i = 0; i < this.option.childs.length; i++) {
                let o = this.option.childs[i]
                childs.push(DivFactory.new_div(o.type).set_option(o))
            }
            this.add_childs(childs)
        }

    }

} 