import { Div,div } from "./div";
import web from "../../web/web_dom"
import { Node } from "../export";
import Constant from "../../web/constant"
export class Row extends Div {
    title: Div
    body: Div
    init_style(): void {
        this.set_style({margin:4,fontSize:20})
    }
    init_node(): void {
        this.title = this.add_child(div().set_style({
            marginRight:20,
            width:100
        })) 
        this.body = this.add_child(div())      
        this.set_style_flex(Constant.VERTICAL) 
    }
    set_option(option: Node): this {
        this.title.set_html(option.title)
        this.body.set_html(option.value)
        return this
    }
}
export class Form extends Div {
    init_style(): void {
        this.set_style({
            textAlign:"center"
        })
    }
    init_node(): void {
        
    }
    set_option(option: Node): this {
        this.option=option
        return this.clear().add_childs(option.childs.map(v=>new Row().set_option(v)))
    }


}
export function form() {
    return new Form()
}
