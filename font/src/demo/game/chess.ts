
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
        this.g.set_height(this.chess_width)
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
        this.pre = new Pre()
        this.right = new Div().add_childs([
            this.user,
            new Column().add_childs([
                new Button().set_html("对战").on_click(this.fight.bind(this)),
                new Button().set_html("执行").on_click(this.execute.bind(this)),
                new Button().set_html("回滚").on_click(this.rollback.bind(this)),
            ]),
            this.pre
        ])
        this.middle = new Div().add_childs([
            this.top_form,
            this.g,
            this.pro,
        ])
        this.add_childs([
            new Div().set_size(1),
            new Column().add_childs([
                this.middle,
                this.right,
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
            url: "/game/chess/get_user"
        })
    }

}
export default function () {
    return new Chess()
}