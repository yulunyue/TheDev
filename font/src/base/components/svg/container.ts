import { GNode } from "./gnode";
import { Circle } from "./circle";
import { DivFactory } from "../export";
import Ct from "../../../base/web/constant"
DivFactory.register_svg(Ct.SVG_TYPE_CIRCLE, () => new Circle())
export class GComponent extends GNode {
    main: GNode
    render_option(): void {
        this.main = DivFactory.new_svg(
            this.option.type, this.option.key
        ).set_option(this.option)
        this.clear().add_child(this.main)
    }
}