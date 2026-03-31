import { Div } from "../dom/div";
import { Span } from "../dom/base/label";
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
    left_btn: Button
    go_btn: Button
    right_btn: Button
    init_style(): void {
        this.page_size_select.set_style({
            width: Constant.INPUT_NUMBER_WIDTH
        })
        this.cur_page.set_style({
            width: Constant.INPUT_NUMBER_WIDTH,
            textAlign: "center"
        })
    }
    init_event(): void {
        this.left_btn.on_click(() => this.add(-1))
        this.right_btn.on_click(() => this.add(1))
        this.go_btn.on_click(() => this.jump(this.cur_page.get_int()))
        this.page_size_select.on_change(this.page_size_change.bind(this))
    }
    init_node(): void {
        this.page_size_select = new Select()
        this.cur_page = new Input()
        this.page_info = new Span()
        this.left_btn = new Button().set_html("<<")
        this.right_btn = new Button().set_html(">>")
        this.go_btn = new Button().set_html("go")
        this.add_childs([
            this.page_size_select,
            this.left_btn,
            this.cur_page,
            this.page_info,
            this.go_btn,
            this.right_btn,
        ])
    }
    add(v: number) {
        return this.jump(this.cur_page.get_int() + v)
    }
    page_size_change() {
        let max_page_size = Math.ceil(this.option.data.all_length / this.page_size_select.get_int())
        this.page_info.set_value(`/${max_page_size}-${this.option.data.all_length}`)
        this.jump(0)
    }
    jump(v: number) {
        let page_size = this.page_size_select.get_int()
        let cur_page = this.cur_page.get_int()
        let max_page = Math.ceil(this.option.data.all_length / page_size)
        if (v < 1) {
            v = 1
        }
        if (v > max_page) {
            v = max_page
        }
        this.cur_page.set_value(v)
        this.do_change(this.option.key, cur_page, v)
        return this
    }
    set_length(length: number) {
        return this.set_option({
            data: {
                all_length: length
            }
        })
    }
    render_page_size() {
        this.page_size_select.set_option(
            new Node().set_childs([10, 20, 50, 100].map((i: number) => {
                return new Node().set_option({
                    value: i,
                    title: i
                })
            }))
        )
    }
    render_option(): void {
        this.option.data.all_length = this.option.data.all_length || 0
        this.render_page_size()
        this.cur_page.set_value(1)
        let max_page_size = Math.ceil(this.option.data.all_length / this.page_size_select.get_int())
        this.page_info.set_value(`/${max_page_size}-${this.option.data.all_length}`)

    }
    get_cur_idxs() {
        let page_size = this.page_size_select.get_int()
        let cur_page = this.cur_page.get_int() - 1
        let ret = []
        for (var i = 0; i < page_size; i++) {
            if (i >= this.option.data.all_length) {
                break
            }
            ret.push(i + cur_page * page_size)
        }
        return ret
    }


}