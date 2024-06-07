import { Div } from "../dom/div"
export class Svg extends Div {
    init_node(): void {
        this.el = Div.create_element("svg")
        this.set_attr("shape-rendering", "geometricPrecision")
    }
}