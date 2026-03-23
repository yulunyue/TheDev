import { Div } from "../div";
import { Constant } from "../../export";
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
export class SeOption extends Div {
    el: HTMLOptionElement
    constructor() {
        super("option")
    }
    render_option(): void {
        this.set_html(this.option.title)
    }
    select(v: any) {
        this.el.selected = v
        return this
    }
}
export class Select extends Div {
    el: HTMLSelectElement
    constructor() {
        super("select")
    }
    init_node(): void {

    }
    init_style(): void {

        this.set_style({
            minWidth: Constant.INPUT_STRING_MIN_WIDTH,
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING,
            border: "1px solid #ccc",
            maxWidth: Constant.WIDTH_TEXT,
            width: `calc(100% - ${Constant.DEFAULT_MARGIN * 2}px)`
        })
    }
    init_event(): void {
        web.bind_change(this.el, () => {
            this.do_change(this.option.key, null, this.get_value())
        })
    }

    select(key: string) {
        if (key == null || key == undefined) {
            return this
        }
        for (var i = 0; i < this.childs.length; i++) {
            let so = this.childs[i]
            if (so.option.key == key) {
                so.do_select(true)
                // this.do_change()
            } else {
                so.do_select(false)
            }
        }
        return this

    }
    get_value() {
        for (var i = 0; i < this.option.childs.length; i++) {
            if (this.option.childs[i].title == this.el.value) {
                return this.option.childs[i].value
            }
        }
        return this.option.childs[0].value
    }
    render_option(): void {
        if (this.option.url) {
            web.post(this.option.url, {}, (node: Node) => {
                this.option.childs = to_node(node).childs
                this.set_childs(this.option.childs, (v: any) => new SeOption().set_option(v))
            })
        } else if (this.option.childs) {
            this.set_childs(this.option.childs, (v: any) => new SeOption().set_option(v))
        }
    }
}