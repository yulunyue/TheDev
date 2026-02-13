import { Div } from "../dom/div";
import { Span } from "../dom/label";
import { Select } from "../dom/form/select";
import { Dom, Node, to_node } from "../../web/cls";
import { Button } from "../dom/form/button";
import { Input } from "../dom/form/input";
import Util from "../../tool/util"
import Constant from "../../web/constant";
export class Pagination extends Div {
    page_size_select: Select
    page_info: Span
    cur_page: Input

    init_node(): void {
        this.option.data = { all_length: 0, cur_page: 0 }
        this.page_size_select = new Select().set_style({
            width: Constant.INPUT_NUMBER_WIDTH
        }).set_option({
            childs: [
                new Node().set_value(10)
            ]
        })
        this.cur_page = new Input().set_option(new Node().set_type(Constant.NUMBER)).set_style({
            textAlign: "center"
        }).set_value(this.option.data.cur_page)
        this.page_info = new Span()
        this.render_page_size()
        this.add_child(this.page_size_select)
        this.add_childs([
            new Button().set_html("<<").on_click(() => this.add(-1)),
            this.cur_page,
            this.page_info,
            new Button().set_html("go").on_click(() => this.jump(this.cur_page.get_int())),
            new Button().set_html(">>").on_click(() => this.add(1)),
        ])
    }
    add(v: number) {
        return this.jump(this.option.data.cur_page + v)
    }
    jump(v: number) {
        let page_size = this.page_size_select.get_value().value
        let max_page = Math.floor(this.option.data.all_length / page_size)
        v = (v + max_page) % max_page
        this.do_change(this.option.data.cur_page, v)
        this.option.data.cur_page = v
        this.render_option()
        return this
    }
    set_length(length: number) {
        this.option.data.all_length = length
        this.jump(0)
        return this
    }
    render_page_size() {
        this.page_size_select.set_option(
            new Node().set_childs([10, 20, 50, 100].map((i: number) => {
                return new Node().set_option({
                    value: i,
                    title: i
                })
            }))
        ).on_change(() => {
            this.jump(0)
        })
    }
    render_option(): void {
        let page_size = this.page_size_select.get_value().value
        this.cur_page.set_value(this.option.data.cur_page)
        let max_page_size = Math.floor(this.option.data.all_length / page_size)
        this.page_info.set_value(`/${max_page_size}-${this.option.data.all_length}`)

    }
    get_cur_idxs() {
        let page_size = this.page_size_select.get_value().value
        let cur_page = this.cur_page.get_int()
        let ret = []
        for (var i = 0; i < page_size; i++) {
            ret.push(i + cur_page * page_size)
        }
        return ret
    }
    on_mount() {
        // this.jump(0)
    }

}