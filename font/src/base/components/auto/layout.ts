import { Div, div } from "../dom/div"
export class Layout extends Div {
    static VERTICAL: number = 1
    static HORIZONTAL: number = 0
    static FLEX_LAYOUT: number = 1
    static RELATIVE_LAYOUT: number = 2
    direction: number
    type: number
    constructor(direction?: number, type?: number) {
        super("div")
        this.direction = direction | Layout.VERTICAL
        this.type = type | Layout.RELATIVE_LAYOUT

    }
    render() {
        if (this.type == Layout.FLEX_LAYOUT) {
            this.render_flex()
        } else if (this.type == Layout.RELATIVE_LAYOUT) {
            this.render_relative()
        }
    }
    render_relative() {
        this.set_style({
            width: 1,
            height: 1,
            position: "absolute"
        })

        for (var i = 0; i < this.childs.length; i++) {
            this.childs[i].set_div_style({
                left: this.direction == Layout.VERTICAL ? i / this.childs.length : 0,
                width: this.direction == Layout.VERTICAL ? 1 / this.childs.length : 1,
                height: this.direction == Layout.HORIZONTAL ? 1 / this.childs.length : 1,
                top: this.direction == Layout.HORIZONTAL ? i / this.childs.length : 0,
                position: "absolute"
            })
        }
        console.log(this.childs, this.direction)
    }
    add_child(c: any) {
        if (c instanceof Layout) {
            c.direction = 1 - this.direction
        }
        return super.add_child(c)
    }
    render_flex() {
        this.set_div_style({
            flexDirection: this.direction == Layout.HORIZONTAL ? "row" : "column",
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