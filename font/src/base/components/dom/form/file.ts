import { Input } from "./input";
import { Button } from "./button";
import { FlexRow } from "../base/row";
import web_dom from "../../../web/web_dom"
import { Node } from "../../../web/cls"
import { FlexColumn } from "../base/column";
export class FileInput extends FlexRow {
    inp: Input
    btn: Button
    path: any
    init_node() {
        this.inp = new Input().set_attr("type", "file")
        this.btn = new Button().set_html("upload")
        this.add_children([this.inp, this.btn])
    }
    init_event(): void {
        this.inp.el.onchange = ((v: any) => {
            this.on_file_change()
        })
        this.btn.on_click(() => this.upload())
    }
    upload() {
        let formData = new FormData()
        formData.append('file', this.inp.el.files[0]);
        web_dom.post_file("/app/manage/post_file", formData, (v: Node) => {
            this.path = v.value
        })
    }
    on_file_change() {

    }
    get_value() {
        return this.path
    }
}