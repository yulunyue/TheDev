import { Div,div } from "./div";
import web from "../../web/web_dom"
import { Node } from "../export";
import { Input,input } from "./input";
import Constant from "../../web/constant"
export class Row extends Div {
    title: Div
    body: Div
    input:Input
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
    get_input(){
        if(!this.input){
            this.input=this.body.add_child(input())
        }
        return this.input
    }
    render_option(): this {
        this.title.set_html(this.option.title)
        if(this.option.type=='text'){
            this.body.set_html(this.option.value)
        } else if(this.option.type=='search'){

        }else{
            this.get_input().set_value(this.option.value)
        }
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
