import { Div } from "../div";
import { TextArea } from "./text_area";
import { Button } from "./button";
import { Title } from "./title";
export class TextAreaRich extends Div {
    area: TextArea
    title: Title

    init_node(): void {
        this.title = this.add_child(new Title())
        this.area = this.add_child(new TextArea())
    }
    set_title(s: string) {
        this.title.title.set_html(s)
        return this
    }
    set_value(value: any): this {
        this.area.set_value(value)
        return this
    }
    get_value() {
        return this.area.get_value()
    }
    set_btns(btns: any) {
        this.title.set_btns(btns)
        return this
    }
    set_flex_style() {
        return this
    }
}
