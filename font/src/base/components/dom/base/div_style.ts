import web_dom from "../../../web/web_dom"
import { Style, Dom } from "../../../web/cls"

export class DivStyle {
    el: HTMLElement

    set_style(style: Style) {
        web_dom.set_el_style(this.el, style)
        return this
    }
    set_div_style(style: Style) {
        web_dom.set_el_style(this.el, style)
        return this
    }
    set_style_ab_full() {
        return this.set_style({
            position: "fixed",
            width: 1,
            height: 1
        })
    }
    set_style_center_by_position() {
        return this.set_style({
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%,-50%)"
        })
    }
    set_style_text_center() {
        this.set_style({ textAlign: "center" })
    }
    set_flex_style_column() {
        return this.set_style({
            display: "flex",
            flexDirection: "row",
            alignItems: "center"
        })
    }
    set_flex_style_row() {
        return this.set_style({
            display: "flex",
            flexDirection: "column",
        })
    }
    set_border() {
        return this.set_style({ border: "1px solid #ccc" })
    }

    get_x() {
        return this.el.clientLeft
    }
    get_y() {
        return this.el.clientTop
    }
    get_width() {
        return this.el.clientWidth
    }
    get_height() {
        return this.el.clientHeight
    }
    get_abs_x() {
        return this.el.offsetLeft
    }
    get_abs_y() {
        return this.el.offsetTop
    }
    get_a_x() {
        return (this.el as HTMLElement).getBoundingClientRect().x;
    }
    get_a_y() {
        return (this.el as HTMLElement).getBoundingClientRect().y
    }
    get_rect() {
        return {
            left: this.get_x(),
            top: this.get_y(),
            width: this.get_width(),
            height: this.get_height()
        }
    }

    set_pos(x: number, y: number) {
        return this
    }
    set_size(size: number) {
        this.size = size
        this.set_style({ flex: size + "" })
        return this
    }
    set_flex(size: number) {
        this.size = size
        this.set_style({ flexGrow: size + "" })
        return this
    }
    set_height(h: number) {
        return this.set_style({ height: h })
    }
    set_width(h: number) {
        return this.set_style({ width: h })
    }

    set_attr(key: string, value: any) {
        this.el.setAttribute?.(key, value)
        return this
    }
    get_attr(key: string) {
        return this.el.getAttribute(key)
    }
    set_class(name: string) {
        return this.set_attr("class", name)
    }
    set_color(s: string) {
        this.set_style({ backgroundColor: s })
    }
    full() {
        return this.set_style({
            width: 1,
            height: 1,
        })
    }

    size: number = 0
}
