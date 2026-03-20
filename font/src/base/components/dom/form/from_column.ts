import { FormContainer } from "./container";
import { FormRow } from "./form_row";
export class FormColumn extends FormRow {
    init_style(): void {
        this.set_style({ display: "flex", flexDirection: "row", alignItems: "center" })
        this.body.set_style({ display: "flex", flexDirection: "row" })
    }
    get_row(): FormContainer {
        return new FormContainer().set_style({
            display: "flex", flexDirection: "row", alignItems: "center"
        })
    }
}