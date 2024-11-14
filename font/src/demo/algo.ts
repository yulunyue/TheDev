
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, node,
    line, gnode, GNode, button, progress, div, input, Input, Progress
} from "../base/components/export";

function algo_node_factory(n: string) {
    return {
        text: form,
        tree
    }[n]()
}
class Algo extends Div {
    div: Div
    pro: Progress
    algo_nodes: Div[]
    form: Form
    init_style(): void {
        this.set_style_ab_full()
    }
    init_node() {
        this.div = div()
        this.form = form().set_option(node().set_childs([
            node("moudule_name").set_type("select").set_data({
                uri: "/app/yly/algo/manage/query"
            }),
        ]))
        this.pro = progress().set_size(1).change((v: number) => this.goto(v))
        this.add_childs([
            this.div.set_size(1),
            div().add_childs([
                this.pro,
                button().set_html("setting").click(() => this.open_setting()),
                button().set_html("run").click(() => this.load())
            ]).set_height(Constant.DEFAULT_LINE_HEIGHT)
        ]).flex_horizontal_layout()
    }
    open_setting() {
        dialog.open(this.form)
    }
    set_option(option: Node): this {
        this.option = option
        this.draw_nodes()
        return this
    }
    draw_nodes() {
        this.algo_nodes = []
        this.div.clear().add_grid_childs(
            this.option.data.nodes.map((v: Node) => {
                let node = algo_node_factory(v.type)
                this.algo_nodes.push(node)
                return node.set_size(1)
            })
        ).flex_horizontal_layout().emit_mount()
    }
    goto(idx: number) {
        if (!this.option || !this.option.data.records[idx]) {
            return
        }
        for (var i = 0; i < this.option.data.records[idx].length; i++) {
            this.algo_nodes[i].set_option(this.option.data.records[idx][i])
        }
    }
    test() {
        this.set_option(new Node().set_childs([Constant.MOCK_NODE_3_3.set_type("tree")]))
    }
    load() {
        web_dom.post('/app/yly/algo/manage/execute', {

        }, (node: Node) => {
            this.set_option(node)
            this.pro.set_max_value(node.data.records.length)
        })
    }
    on_mount() {
        //this.test()
        //this.load()
        this.open_setting()

    }
}
export default function () {
    return new Algo()
}