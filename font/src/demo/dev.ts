
import {
    Div, search, Search, button, TextAreaRich, text_area
} from "../base/components/export";
export class Temaplate extends Div {
    search: Search
    text_area: TextAreaRich
    init_node(): void {
        this.search = search().set_title(
            "搜索"
        ).set_btns([
            button().set_html("测试")
        ])
        this.add_childs([
            this.search
        ])
    }
    on_mount(): void {

    }

}
export default function () {
    return new Temaplate()
}