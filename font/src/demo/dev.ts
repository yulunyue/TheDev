
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
    Pre,
    Data,

} from "../base/components/export";
import { D3DagreUtil } from "../third/d3_dagre_util"

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
        let table = new Table().set_option({
            childs: [{
                key: "a",
                value: "a",
                type: Constant.DOM_TYPE_STRING
            }, {
                key: "b",
                value: "b",
                type: Constant.DOM_TYPE_INPUT
            }, {
                key: "c",
                value: "c",
                type: Constant.DOM_TYPE_PRE
            }, {
                key: "method", title: "操作",
                type: Constant.DOM_TYPE_BTNS,
                value: ["remove", "add"]
            }],
            value: Util.array(103, (i: number) => {
                return {
                    a: i,
                    b: "value" + i,
                    c: Util.array(303, (v: any) => v)
                }
            })
        })
        return table
    },
    default_color: Constant.COLOR_BALCK2,
    grid() {
        let p1 = new Pre().set_html("p1")
        let p2 = new Pre().set_html("p2")
        let g = new Grid().set_style({
            width: 300,
            height: 300,
            margin: 40
        }).set_option({
            x: 6, y: 6,
            childs: [{
                x: 0, y: 0, type: Constant.SVG_TYPE_CIRCLE, color: Constant.COLOR_WHITE2,
            }, {
                x: 0, y: 1, type: Constant.SVG_TYPE_CIRCLE, color: Constant.COLOR_BALCK2,
            }]
        }).on_move((y: number, x: number, i: number, j: number) => {
            p1.set_value({ x, y, i, j })
        })
        g.on_click((y: number, x: number, i: number, j: number) => {
            p2.set_value({ x, y, i, j })
            g.draw_child({
                y: i, x: j, type: Constant.SVG_TYPE_CIRCLE,
                color: DEV_FUNC.default_color
            })
            DEV_FUNC.default_color = DEV_FUNC.default_color == Constant.COLOR_BALCK2 ? Constant.COLOR_WHITE2 : Constant.COLOR_BALCK2
        })
        return new Column().add_childs([
            g,
            new Row().add_childs([
                p1,
                p2
            ])
        ])
    },

    sys() {
        let d = new Div()
        let d1 = new Div().set_html("xx")
        let size = web_dom.get_window_size()
        d.set_html(`width:${size.width};height:${size.height}`)
        Data.get_user_name((s: string) => {
            d1.set_html(s)
        })
        return new Div().add_childs([
            d, d1
        ])
    },
    dagre() {
        let dagre = new D3DagreUtil().set_style({
            width: 500,
            height: 500
        })
        web_dom.next_frame(() => {
            dagre.set_option({})
        })
        return new Div().add_childs([
            dagre
        ])
    }
}
export class Dev extends Div {
    svg: Svg
    init_style(): void {
        this.full()
    }
    render(): void {
        let method = web_dom.get_param("method")
        this.add_childs([DEV_FUNC[method]().full()])
    }

}
export default function () {
    return new Dev()
}