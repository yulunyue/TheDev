import { Div } from "../dom/div"
export class GNode extends Div {
    init_node(): void {
        this.el = Div.create_element("g")
    }
}
export function gnode() {
    return new GNode()
}