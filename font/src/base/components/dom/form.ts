import { Div, div } from "./div";
import web from "../../web/web_dom"
import { Node } from "../export";
import { Input, input } from "./input";
import { Search, search } from "./search";
import { Select } from "./select";
import Constant from "../../web/constant"
export class Row extends Div {
    title: Div
    body: Div
    content: Div
    input: Input
    search: Search
    select:Select
    init_style(): void {
        this.set_style({ margin: 4, fontSize: 20 })
    }
    init_node(): void {
        this.title = this.add_child(div().set_style({
            marginRight: 20,
            width: 100
        }))
        this.body = this.add_child(div())
        this.set_style_flex(Constant.VERTICAL)
    }
    get_input() {
        if (!this.input) {
            this.input = this.body.add_child(input())
        }
        return this.input
    }
    get_search() {
        if (!this.search) {
            this.search = this.body.add_child(new Search())
        }
        return this.search
    }
    get_content() {
        if (!this.content) {
            this.content = this.body.add_child(new Div())
        }
        return this.content
    }
    get_select() {
        if (!this.select) {
            this.select = this.body.add_child(new Select())
        }
        return this.select
    }
    render_option(): this {
        this.title.set_html(this.option.title)
        if (this.option.type == 'text') {
            this.get_content().set_option(this.option)
        } else if (this.option.type == 'search') {
            this.get_search().set_option(this.option)
        } else if(this.option.type == 'select'){
            this.get_select().set_option(this.option)
        } 
        else {
            this.get_input().set_option(this.option)
        }
        return this
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


}
export function form() {
    return new Form()
}
