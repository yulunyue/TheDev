import { FormContainer } from "./container";
import { FormColumn } from "./form_column";
import { not_null, Node } from "../../../web/cls"
import { Div } from "../div";
import { Constant } from "../../export";
export class FormRow extends FormColumn {
    init_style(): void {
        this.set_style({ display: "flex", flexDirection: "column" })
        this.body.set_style({
            display: "flex", flexDirection: "column",
            justifyContent: "space-between",
            // borderBottom: "1px solid #000"
        }).set_size(1)
        this.footer.set_style({ justifyContent: "space-between" })
    }

    render_chilld(d: Div, o: Node) {
        if (o.type == Constant.DOM_TYPE_SELECT || o.type == Constant.DOM_TYPE_BOOL) {
            return d.set_flex_style_column()
        }
        return d.set_flex_style_row()
    }
}