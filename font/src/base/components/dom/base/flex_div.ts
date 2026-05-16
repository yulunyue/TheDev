import { Div } from "./div";
import Constant from "../../../web/constant"
import { FlexRow } from "./row";
import { DivFactory } from "./div_factory";
export class FlexDiv extends Div {
    show(): this {
        return this.set_style({ display: "flex" })
    }
    get_direction() {
        return ""
    }
    init_style() {
        this.set_div_style({
            flexDirection: this.get_direction(),
            display: "flex",
            // justifyContent: "space-between",
            alignContent: "center",
            //alignItems: "center",
            overflow: "auto",
            // minHeight: 0
        })
    }
    set_align_start() {
        this.set_style({
            "alignItems": "flex-start"
        })
        return this
    }
    set_align_space_around() {
        this.set_style({
            justifyContent: "space-around"
        })
    }
    set_center() {
        this.set_div_style({
            alignItems: "center"
        })
        return this
    }

    render_option(): void {
        if (this.option.children && this.option.children.length) {
            this.clear()
            let children = []
            for (var i = 0; i < this.option.children.length; i++) {
                let o = this.option.children[i]
                children.push(DivFactory.new_div(o.type, o.key).set_option(o))
            }
            this.add_children(children)
        }

    }

} 