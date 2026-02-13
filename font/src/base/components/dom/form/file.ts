import { Input } from "./input";
import web_dom from "../../../web/web_dom"
export class FileInput extends Input {
    init_node() {
        this.set_attr("type", "file")
    }
    init_event(): void {
        this.el.onchange = ((v: any) => {
            this.on_file_change()
        })
    }
    on_file_change() {
        console.log(this.get_form_data())
    }
    get_form_data() {
        let formData = new FormData()
        formData.append('file', this.el.files[0]);
        return formData
    }
}