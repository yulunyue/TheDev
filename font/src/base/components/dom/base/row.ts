import { FlexDiv } from "./flex_div";
import Constant from "../../../web/constant"
export class FlexColumn extends FlexDiv {
    get_direction() {
        return Constant.HORIZONTAL
    }
}