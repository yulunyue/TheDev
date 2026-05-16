

import {
    Div, Constant, Node, web_dom, oj_to_node, FormColumn, to_node, Search, Container,
    Button, Progress,
    Svg,
    Grid,
    FlexColumn,
    Pre,
    FlexRow,
    Title,
    Data,
    web_socket
} from "../../base/components/export";
let COLORS = [Constant.COLOR_BLACK2, Constant.COLOR_WHITE2]
export class Chess extends FlexRow {
    g: Grid
    bottom_form: FormColumn
    chess_width: number
    name_search: Search
    head_column: FlexRow
    pre: Pre
    title: Title
    right_div: Div
    left_div: Div
    mid_main: FlexColumn
    init_style(): void {
        super.init_style()
        this.full().set_center()
        this.chess_width = 400
        this.bottom_form.set_input_width(80)
        this.g.set_style({
            width: this.chess_width,
            height: this.chess_width,
            // border: "1px solid #000"
        })
        this.name_search.set_width(96)
        this.title.set_size(1).set_style({ textAlign: "right" })
        this.right_div.set_size(1)
        this.left_div.set_size(1)
    }
    init_node(): void {
        this.g = new Grid()
        this.bottom_form = new FormColumn()
        this.pre = new Pre()
        this.left_div = new Div()
        this.right_div = new FlexColumn()
        this.title = new Title()
        this.name_search = new Search()
        this.head_column = new FlexRow().add_children([
            this.name_search,
            this.title,
        ])
        this.mid_main = new FlexColumn().add_children([
            this.head_column,
            this.g,
            this.bottom_form,
        ])
        this.add_children([
            this.left_div,
            this.mid_main,
            this.right_div
        ])
    }
    hander_on_click(y: number, x: number, i: number, j: number) {
        web_dom.post("/game/f5chess/play", {
            name: this.name_search.get_value(),
            y: i, x: j,
        }, (data) => {
            this.show_data(data)
        })

    }
    init_event(): void {
        this.g.on_click(this.hander_on_click.bind(this))
        this.name_search.on_change((key: string, src: any, dst: any) => {
            web_socket.un_sub(Constant.TOPIC_TASK_UPDATE_MSG + "." + src).sub(
                Constant.TOPIC_TASK_UPDATE_MSG + "." + dst,
                this.show_data.bind(this)
            )
        })
    }

    show_data(dst: any) {
        this.bottom_form.set_value(dst)
        let players = [dst.p0, dst.p1]
        let colors = ["黑", "白"]
        let done = dst.done
        if (done == null) {
            let idx = dst.records.length % 2
            this.title.set_html(`回合[${dst.records.length}] [${players[idx]}执${colors[idx]}]`)
        } else if (done == "NO_WIN") {
            this.title.set_html(`游戏结束 - 平局`)
        } else {
            let winner_idx = parseInt(done) - 1
            this.title.set_html(`游戏结束 - ${players[winner_idx]}(${colors[winner_idx]})获胜`)
        }
        let children = []
        for (var i = 0; i < dst.records.length; i++) {
            let v = dst.records[i]
            children.push({
                y: Math.floor(v / dst.width),
                x: v % dst.width,
                type: Constant.SVG_TYPE_CIRCLE,
                color: COLORS[i % 2]
            })
        }
        this.g.set_option({
            x: dst.width,
            y: dst.height,
            children: children
        })
    }
    draw() {
        web_dom.post("/game/f5chess/get", {
            key: this.bottom_form.get_value().name
        }, (data: any) => {
            this.show_data(data)
        })
    }

    hander_sub(key: string, op: any) {
        console.log(key, op)
    }
    render(): void {
        this.bottom_form.set_uri("/game/f5chess/to_form_column_view", () => {
            this.bottom_form.child_map.size.set_flex(1)
        })
        this.name_search.set_option({
            url: "/game/f5chess/search_name",
            id: "game_chess_form_search"
        })
        this.title.set_html("info")

    }

}
export default function () {
    return new Chess()
}