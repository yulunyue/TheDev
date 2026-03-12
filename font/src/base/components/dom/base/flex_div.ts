import { Div } from "./div";
import Constant from "../../../web/constant"
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


} 