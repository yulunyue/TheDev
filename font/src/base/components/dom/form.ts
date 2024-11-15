import { Div, div } from "./div";
import web from "../../web/web_dom"
import {not_null,Node} from "../../web/cls"
import { Input, input } from "./input";
import { Search, search } from "./search";
import { Select } from "./select";
import Constant from "../../web/constant"
export class Row extends Div {
    title: Div
    body: Div
    input: Div
    init_style(): void {
        this.set_style({ margin: 4, fontSize: 20 })
    }
    init_node(): void {
        this.title = this.add_child(div().set_style({
            // marginRight: 20,
            margin:Constant.DEFAULT_MARGIN
            // width: 100
        }))
        this.body = this.add_child(div())
        // this.set_style_flex(Constant.VERTICAL)
    }

    render_option(): this {
        this.title.set_html(this.option.title)
        if (this.option.type == 'text') {
            this.input = this.body.add_child(new Div())
        } else if (this.option.type == 'search') {
            this.input = this.body.add_child(new Search())
        } else if(this.option.type == 'select'){
            this.input = this.body.add_child(new Select())
        } 
        else {
            this.input = this.body.add_child(input())
        }
        this.input.set_option(this.option)
        return this
    }
    get_value() {
        return this.input.get_value()
    }
}
export class Form extends Div {
    init_style(): void {
        this.set_style({
            textAlign: "center"
        })
    }
    init_node(): void {

    }
    set_option(option: Node): this {
        this.option = option
        return this.clear().add_childs(option.childs.map(v => new Row().set_option(v)))
    }
    get_value() {
        let ret={}
        for(var i=0;i<this.childs.length;i++){
            ret[this.childs[i].option.key]=this.childs[i].get_value()
        }
        return ret
    }
    get(key:string ,default_value?:string){
        return not_null(this.get_value()[key],default_value)
    }

}
export function form() {
    return new Form()
}
