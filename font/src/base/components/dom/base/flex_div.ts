import { Div } from "./div";
import Constant from "../../../web/constant"
export class FlexDiv extends Div {
    direction: number = -1

    flex_veritcal_layout() {
        this.set_size(1)
        return this.set_style_flex(Constant.VERTICAL).full()
    }
} 