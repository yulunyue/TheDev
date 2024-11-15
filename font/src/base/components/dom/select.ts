import { Div } from "./div";
import { Constant } from "../export";
import web from "../../web/web_dom"
import { Node, to_node } from "../../web/cls";
// export class Li extends Div {
//     constructor() {
//         super("li")
//     }
//     render_option() {
//         console.warn(this.option.get_title())
//         this.set_html(this.option.get_title())
//     }
// }
export class Select extends Div {
    el:HTMLSelectElement
    constructor() {
        super("select")
    }
    init_node(): void {

    }
    init_style(): void {
        this.set_style({
            minWidth: Constant.INPUT_STRING_MIN_WIDTH,
            margin:Constant.DEFAULT_MARGIN,
            padding:Constant.DEFAULT_PADDING,
            border:"1px solid #ccc"
        })
    }
    init_event(): void {
        web.bind_change(this.el, () => {
            this.option.value = this.get_value()
        })
    }
    set_uri(uri: string) {
        web.post(uri, {}, (node: Node) => {

            this.option.childs = to_node(node).childs
            this.render_child()
        })
    }
    render_child() {
        // this.clear().add_childs(this.option.childs.map(v => {
        //     return new Li().set_option(v)
        // }))
        
        for(var i=0;i<this.option.childs.length;i++){
            let op=this.option.childs[i]
            this.el.options.add(new Option(op.value,op.get_title()))
        }
    }
    render_option(): void {
        if (this.option.data.uri) {
            this.set_uri(this.option.data.uri)
        }
    }
}
export function select() {
    return new Select()
}