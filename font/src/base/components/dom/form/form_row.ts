import { FormContainer } from "./container";
import { FormColumn } from "./form_column";
import { not_null, Node } from "../../../web/cls"
export class FormRow extends FormColumn {
    init_style(): void {
        this.set_style({ display: "flex", flexDirection: "column" })
        this.body.set_style({
            display: "flex", flexDirection: "column",
            justifyContent: "space-between",
            // borderBottom: "1px solid #000"
        }).set_size(1)
    }
    get_row(o: Node): FormContainer {
        return super.get_row(o).set_style({
            display: "flex", flexDirection: "column",
        })
    }
}