
import data from "src/base/tool/data";
import {
    Div, Search, Button, TextAreaRich,
    Table, Util, dialog,
    Ct, Node, to_node, Chart,
    Svg,
    Grid,
    web_dom
} from "../base/components/export";
import { D3Chart, MeraGraph } from "../third/export"
export class Dev extends Div {
    svg: Svg

    init_node(): void {
        this.add_childs([
            this.get_window_info()
        ])
    }
    get_window_info() {
        let d = new Div()
        let size = web_dom.get_window_size()
        d.set_html(`width:${size.width};height:${size.height}`)
        return d
    }
    init_style(): void {

    }
    test_open_edit_dialog() {
        dialog.open_form({ a: "input" }, (v: any) => {
            console.log(v)
        })
    }
    test_table_data() {
        let table = new Table()
        table.set_data({
            header: [{
                key: "a",
                value: "a"
            }, {
                key: "b",
                value: "b",
                type: "input"
            }, {
                key: "method", title: "操作", type: "btns", value: ["remove", "add"]
            }],
            body: Util.array(27, (i: number) => {
                return {
                    a: i,
                    b: "value" + i
                }
            })
        })
        this.add_childs([table])
    }
    test_graph() {
        let node = to_node({
            value: "flowchart TD",
            data: {
                A: ["BC"],
                C: [["B"]]
            }
        })

        this.add_child(new MeraGraph().set_option(node))
    }
    test_graph_xy() {
        let node = to_node({
            value: MeraGraph.TYPE_XY,
            data: [[-32, 12], [-32, -94], [-32, -15], [-30, 88]]
        })
        this.add_child(new MeraGraph().set_option(node))
    }
    test_chart() {
        let chart = new D3Chart().set_option({

        })
        this.add_child(chart)
    }
    test_grid() {
        this.add_child(new Grid().set_option({
            childs: []
        }))
    }
    on_mount(): void {

    }

}
export default function () {
    return new Dev()
}