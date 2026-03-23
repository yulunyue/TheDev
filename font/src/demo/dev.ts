import data from "src/base/tool/data";
import {
    Div, Search, Button, TextAreaRich,
    Table, Util, dialog,
    Ct, Node, to_node, Chart,
    Svg,
    Grid,
    web_dom,
    Row, Column,
    FileInput,
    FormColumn, FormRow,
    Constant,
    Pre
} from "../base/components/export";
import { D3Chart, MeraGraph } from "../third/export"
let DEV_FUNC = {
    form() {
        let op = {
            childs: [
                { type: Constant.DOM_TYPE_INPUT, title: "a", key: "a" },
                { type: Constant.DOM_TYPE_FILE, title: "b", key: "b" },
                {
                    type: Constant.DOM_TYPE_SELECT, title: "c", key: "c", childs: [{
                        title: "a",
                        value: "a"
                    }, {
                        title: "b",
                        value: "b"
                    }]
                }
            ]
        }
        let pre = new Pre().set_html("pre")
        function fm_init(fm: FormRow, ops: Node) {
            fm.on_submit((type: string, value: any) => {
                pre.set_value({ type: type, value: fm.get_value(), d: value })
            })
            fm.on_change((key: string, value: any, data: any) => {
                if (typeof data == "object") {
                    fm.set_value(data)
                }
                pre.set_value({ key: key, value: value, data: data })
            })
            ops && fm.set_option(ops)
            return fm
        }

        return new Row().add_childs([
            fm_init(new FormColumn(), op),
            new Column().add_childs([
                fm_init(new FormRow(), op),
                pre.set_size(1),
                fm_init(new FormRow().set_uri("/app/user"), null)
            ]),

        ])
    },
    layout() {
        return new Column().set_option({
            childs: [
                {
                    type: Constant.DOM_TYPE_ROW,
                    childs: [{
                        type: Constant.DOM_TYPE_STRING,
                        value: "12",
                    }, {
                        type: Constant.DOM_TYPE_STRING,
                        value: "34",

                    }]
                },
                {
                    type: Constant.DOM_TYPE_STRING,
                    value: "56",
                    size: 1
                }
            ]
        }).set_height(200).set_center()
    },
    table() {
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
            body: Util.array(2, (i: number) => {
                return {
                    a: i,
                    b: "value" + i
                }
            })
        })
        return table
    },
    grid() {
        let p1 = new Pre().set_html("p1")
        let p2 = new Pre().set_html("p2")
        let g = new Grid().set_style({
            width: 300,
            height: 300,
            margin: 40
        }).set_option({
            data: {
                x: 6, y: 6
            }
        }).on_move((y: number, x: number, i: number, j: number) => {
            p1.set_value({ x, y, i, j })
        }).on_click((y: number, x: number, i: number, j: number) => {
            p2.set_value({ x, y, i, j })
        })
        return new Column().add_childs([
            g,
            new Row().add_childs([
                p1,
                p2
            ])
        ])
    }
}
export class Dev extends Div {
    svg: Svg


    get_window_info() {
        let d = new Div()
        let size = web_dom.get_window_size()
        d.set_html(`width:${size.width};height:${size.height}`)
        return d
    }
    test_open_edit_dialog() {
        dialog.open_form({ a: "input" }, (v: any) => {
            console.log(v)
        })
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


    on_mount(): void {

    }
    render(): void {
        let method = web_dom.get_param("method")
        this.add_childs([DEV_FUNC[method]()])
    }

}
export default function () {
    return new Dev()
}