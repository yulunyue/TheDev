import { FormContainer } from "./container";
import { FormRow } from "./form_row";
export class FormColumn extends FormRow {
    get_form_view_url() {
        return "/to_form_column_view"
    }
    init_style(): void {
        this.set_style({ display: "flex", flexDirection: "row", alignItems: "center" })
        this.body.set_style({ display: "flex", flexDirection: "row" }).set_size(1)
    }
    get_row(): FormContainer {
        return new FormContainer().set_style({
            display: "flex", flexDirection: "row", alignItems: "center"
        })
    }
}