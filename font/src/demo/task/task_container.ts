import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, Util
} from "../../base/components/export";
import { TaskRow } from "./task_row";

export class TaskContainer extends Div {
    task_rows: TaskRow[] = []
    init_style(): void {
        this.set_style({
            flex: "1",
            overflow: "auto",
            width: "100%"
        })
        super.init_style()
    }
    init_node(): void {
    }
    set_tasks(data: Node, on_change: any): this {
        this.clear()
        this.task_rows = []
        for (let task of data.childs) {
            this.add_task_row(task).on_change(on_change)
        }
        return this
    }
    add_task_row(task: any): TaskRow {
        let row = new TaskRow().set_task(task)
        this.add_child(row)
        this.task_rows.push(row)
        return row
    }
    filter(key: string) {
        for (var i = 0; i < this.task_rows.length; i++) {
            var task = this.task_rows[i]
            var s = task.task_data.name + task.task_data.fun_path
            if (Util.str_match(s, key)) {
                task.show()
            } else {
                task.hide()
            }
        }
    }
}