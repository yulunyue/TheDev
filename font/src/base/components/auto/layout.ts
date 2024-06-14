import { Div, div } from "../dom/div"
export class Layout extends Div {
    static VERTICAL: number = 1
    static HORIZONTAL: number = 2
    static FLEX_LAYOUT: number = 1
    direction: number
    type: number
    constructor(direction?: number, type?: number) {
        super("div", "")
        this.direction = direction | Layout.VERTICAL
        this.type = type | Layout.FLEX_LAYOUT

    }
    render() {
        if (this.type == Layout.FLEX_LAYOUT) {
            this.render_flex()
        }
    }
    add_child(c: any) {
        if (c instanceof Layout) {
            c.direction = 1 - this.direction
        }
        return super.add_child(c)
    }
    render_flex() {
        this.set_div_style({
            flexDirection: "row",
            display: "flex"
        })
    }

}
export function layout(direction?: number) {
    return new Layout(direction)
}
export function layout_dev() {
    return layout().add_childs([
        div().set_html("div1"),
        div().set_html("div1")
    ])
}