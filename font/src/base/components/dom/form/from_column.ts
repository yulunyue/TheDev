import { FormContainer } from "./container";
import { FormRow } from "./form_row";
import { not_null, Node } from "../../../web/cls"
export class FormColumn extends FormRow {
    get_form_view_url() {
        return "/to_form_column_view"
    }
    init_style(): void {
        this.set_style({ display: "flex", flexDirection: "row", alignItems: "center" })
        this.body.set_style({ display: "flex", flexDirection: "row" }).set_size(1)
    }
    get_row(o: Node): FormContainer {
        return super.get_row(o).set_style({
            display: "flex", flexDirection: "row", alignItems: "center"
        })
    }
}