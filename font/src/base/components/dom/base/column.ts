import { FlexDiv } from "./flex_div";
import Constant from "../../../web/constant"
export class Column extends FlexDiv {
    get_direction() {
        return Constant.VERTICAL
    }
}