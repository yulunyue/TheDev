import { FlexDiv } from "./flex_div";
import Constant from "../../../web/constant"
export class Row extends FlexDiv {
    get_direction() {
        return Constant.HORIZONTAL
    }
}