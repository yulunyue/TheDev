
import { AnyMxRecord } from "dns";
import {
    Div, Constant, Node, web_dom, oj_to_node, FormColumn, to_node, Search, Container,
    Button, Progress,
    Svg,
    Grid,
    Row,
    Pre,
    Column,
    Title,
    Data
} from "../../base/components/export";
import data from "src/base/tool/data";
let COLORS = [Constant.COLOR_BALCK2, Constant.COLOR_WHITE2]
export class Chess extends Column {
    g: Grid
    top_control: Div
    pro: Progress
    top_form: FormColumn
    chess_width: number
    pre: Pre
    title: Title
    init_style(): void {
        super.init_style()
        this.full().set_center()
        this.chess_width = 400
        this.top_form.set_input_width(60)
        // this.middle.set_width(this.chess_width)
        this.g.set_style({
            width: this.chess_width,
            height: this.chess_width,
            // border: "1px solid #000"
        })
    }
    init_node(): void {
        this.g = new Grid()
        this.top_form = new FormColumn()
        this.pro = new Progress()
        this.pre = new Pre()
        this.title = new Title()
        this.add_childs([
            new Div().set_size(1),
            new Row().add_childs([
                this.top_form,
                this.title,
                this.g,
                this.pro,

            ]),
            new Div().set_size(1)
        ])
    }
    hander_on_click(y: number, x: number, i: number, j: number) {
        let top_value = this.top_form.get_value()
        web_dom.post("/game/f5chess/play", {
            name: top_value.name,
            y: i, x: j,
        }, () => {
            this.draw()
        })

    }
    init_event(): void {
        this.top_form.on_submit(this.hander_sub.bind(this))
        this.top_form.on_change(this.hander_change.bind(this))
        this.g.on_click(this.hander_on_click.bind(this))
    }
    show_data(dst: any) {
        let players = [dst.player_0, dst.player_1]
        let colors = ["黑", "白"]
        let idx = dst.records.length % 2
        this.title.set_html(`[回合[${dst.records.length}] [${players[idx]}执${colors[idx]}] `)
        let childs = []
        for (var i = 0; i < dst.records.length; i++) {
            let v = dst.records[i]
            childs.push({
                y: Math.floor(v / dst.size),
                x: v % dst.size,
                type: Constant.SVG_TYPE_CIRCLE,
                color: COLORS[i % 2]
            })
        }
        this.g.set_option({
            x: dst.size,
            y: dst.size,
            childs: childs
        })
    }
    uri(path: string) {
        return "/game/f5chess" + path
    }
    draw() {
        web_dom.post(this.uri("/get"), {
            key: this.top_form.get_value().name
        }, (data) => {
            this.show_data(data)
        })
    }
    hander_change(key: string, src: any, dst: any) {
        if (key == "name") {
            this.draw()
        }
    }
    hander_sub(key: string, op: any) {
        console.log(key, op)
    }
    render(): void {
        this.top_form.set_option({
            url: "/game/f5chess",
            id: "game_chess"
        })
        this.title.set_html("info")

    }

}
export default function () {
    return new Chess()
}