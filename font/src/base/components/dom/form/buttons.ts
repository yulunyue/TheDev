import { Div } from "../div";
import { Button } from "./button";
export class Buttons extends Div {

    render_option(): void {
        this.clear().add_childs(this.option.childs.map(v => {
            return new Button().set_html(v.title)
        }))
    }
}
