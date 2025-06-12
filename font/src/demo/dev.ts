
import {
    Div, search, Search, button, TextAreaRich, text_area,
    Table, Util
} from "../base/components/export";
export class Dev extends Div {
    search: Search
    text_area: TextAreaRich
    table: Table
    init_node(): void {
        this.search = search().set_title(
            "搜索"
        ).set_btns([
            button().set_html("测试")
        ])
        this.table = new Table()
        this.add_childs([
            this.search,
            this.table
        ])
    }
    on_mount(): void {

        this.table.set_data({
            header: [{
                key: "a",
                value: "a"
            }, {
                key: "b",
                value: "b",
                type: "input"
            }],
            body: Util.array(27, (i: number) => {
                return {
                    a: i,
                    b: "value" + i
                }
            })
        })
    }

}
export default function () {
    return new Dev()
}