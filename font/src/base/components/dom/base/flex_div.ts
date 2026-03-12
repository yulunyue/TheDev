import { Div } from "./div";
import Constant from "../../../web/constant"
import { Row } from "./row";
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
    new_cls() {
        return new Row()
    }
    render_option(): void {
        if (this.option.childs) {
            this.set_childs(this.option.childs, this.new_cls)
        }
    }

} 