import {
    FormRow, Constant, dialog
} from "../../base/components/export";
import { TodoData } from "./todo_types";

export class TodoForm {
    form: FormRow
    private submit_cb: ((type: string) => void) | null = null

    constructor() {
        this.form = new FormRow()
        this.form.on_submit((type: string) => {
            this.submit_cb?.(type)
        })
    }

    set_schema(schema: any) {
        this.form.set_option(schema)
    }

    set_on_submit(cb: (type: string) => void) {
        this.submit_cb = cb
    }

    open(method: string, data: Partial<TodoData>) {
        if (method == Constant.METHOD_INSERT) {
            this.form.set_btns({ [Constant.METHOD_INSERT]: "提交" })
            this.form.child_map.title.show()
        } else {
            this.form.child_map.title.hide()
            this.form.set_btns({
                [Constant.METHOD_EDIT]: "保存",
                [Constant.METHOD_CLONE]: "复制",
                [Constant.METHOD_DELETE]: "删除"
            })
        }
        this.form.set_value(data)
        dialog.open(this.form)
    }

    get_value(): any {
        return this.form.get_value()
    }

    set_style(style: any) {
        this.form.set_style(style)
        return this
    }
}
