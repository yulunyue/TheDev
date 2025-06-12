import { Div } from "./div";
import { Select } from "./select";
import { Node, to_node } from "../../web/cls";
import { Button } from "./button";
import { Input } from "./input";
import Util from "../../tool/util"
import Constant from "../../web/constant";
export class Pagination extends Div {
    page_size_select: Select
    page_btns: Button[]
    cur_page: Input
    init_node(): void {
        this.page_size_select = new Select()
        this.page_btns = Util.array(5, (i: number) => {
            return new Button().set_html("btn" + i)
        })
        this.cur_page = new Input().set_option(new Node().set_type(Constant.NUMBER))
        this.render_page_size()
        this.add_child(this.page_size_select)
        this.add_childs(this.page_btns)
        this.add_childs([
            this.cur_page,
            new Button().set_html("go")
        ])
    }
    render_page_size() {
        this.page_size_select.set_option(
            new Node().set_childs(Util.array(3, (i: number) => {
                return new Node().set_option({
                    value: (i + 1) * 10,
                    title: (i + 1) * 10
                })
            }))
        )
    }
    render_option(): void {

    }
}