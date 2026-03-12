import { Input } from "./input";
import { Button } from "./button";
import { Row } from "../base/row";
import web_dom from "../../../web/web_dom"
export class FileInput extends Row {
    inp: Input
    btn: Button
    path: string
    init_node() {
        this.inp = new Input().set_attr("type", "file")
        this.btn = new Button().set_html("upload")
        this.add_childs([this.inp, this.btn])
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
        web_dom.post_file("/app/manage/post_file", formData)
    }
    on_file_change() {

    }
    get_value() {
        return this.path
    }
}