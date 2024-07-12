import { Div, div } from "../dom/div"
export class Layout extends Div {
    static VERTICAL: number = 1
    static HORIZONTAL: number = 2
    static FLEX_LAYOUT: number = 1
    static RELATIVE_LAYOUT: number = 2
    direction: number
    type: number
    constructor(direction?: number, type?: number) {
        super("div")
        this.direction = direction === undefined ? Layout.VERTICAL : direction
        this.type = type === undefined ? Layout.RELATIVE_LAYOUT : type

    }
    add_grid_childs(childs: any[]) {
        let row = Math.ceil(Math.sqrt(childs.length))
        let col = Math.ceil(childs.length / row)
        for (var i = 0; i < row; i++) {

            for (var j = 0; j < col; j += 1) {
                if (i * col + j > childs.length) {
                    break
                }
            }
        }
        console.log(row, col, childs.length)
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
    }
    add_child(c: any) {
        if (c instanceof Layout) {
            c.direction = 3 - this.direction
            c.type = this.type
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