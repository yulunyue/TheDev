
import {
    Div, Constant, Node, web_dom, oj_to_node, FormColumn, to_node, Search, Container,
    Button, Progress,
    Svg,
    Grid,
    Row,
    Pre,
    Column,
} from "../../base/components/export";
export class Chess extends Column {
    g: Grid
    right: Div
    middle: Div
    algo: Search
    top_control: Div
    pro: Progress
    top_form: FormColumn
    user: Search
    chess_width: number
    pre: Pre
    init_style(): void {
        super.init_style()
        this.full().set_center()
        this.chess_width = 400
        this.middle.set_width(this.chess_width)
        this.g.set_style({
            // width: this.chess_width - 2,
            // height: this.chess_width - 2,
            border: "1px solid #000"
        })
    }
    fight() {

    }
    execute() {

    }
    rollback() {

    }
    init_node(): void {
        this.g = new Grid()
        this.top_form = new FormColumn()
        this.pro = new Progress()
        this.user = new Search()
        this.algo = new Search()
        this.pre = new Pre()

        this.right = new Row().add_childs([
            new Column().add_childs([
                this.user,
                new Button().set_html("对战").on_click(this.fight.bind(this))
            ]),

            new Column().add_childs([
                this.algo,
                new Button().set_html("分析").on_click(this.execute.bind(this)),
            ]),
            this.pre.set_size(1),

        ])
        this.middle = new Div().add_childs([
            this.g,
            this.pro,
        ])
        this.add_childs([
            new Div().set_size(1),
            new Row().add_childs([
                this.top_form,
                new Column().add_childs([
                    this.middle,
                    this.right
                ])
            ]),
            new Div().set_size(1)
        ])
    }
    init_event(): void {
        this.top_form.on_submit(this.hander_sub.bind(this))
    }
    hander_sub(key: string, op: any) {
        console.log(key, op)
    }
    render(): void {
        this.top_form.set_uri("/game/chess/bd").set_id("game_chess")
        this.user.set_option({
            url: "/game/f5chess/get_user",
            title: "用户"
        })
        this.algo.set_option({
            url: "/game/f5chess/get_algo",
            title: "算法"
        })
    }

}
export default function () {
    return new Chess()
}