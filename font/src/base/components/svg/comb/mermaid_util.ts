import { Div } from "../../dom/div";
import mermaid from "mermaid";
import { Svg, Node } from "../../export";
import { line, web_dom } from "../../export";
mermaid.initialize({
    //theme: 'neutral',
    //look: "handDrawn",
    themeCSS: '.node rect { fill: white; }',

    logLevel: 3,
    securityLevel: 'loose',
    flowchart: { curve: 'basis' },
    gantt: { axisFormat: '%m/%d/%Y' },
    sequence: { actorMargin: 50 },

    // sequenceDiagram: { actorMargin: 300 } // deprecated
})
export class MeraUtil extends Div {

    constructor() {
        super("pre")
    }
    init_node(): void {

    }
    on_load() {
        let svg = (this.el.children[0] as any)
        if (!svg || !svg.clientWidth) {
            return
        }
        let w = this.el.clientWidth - svg.clientWidth
        let h = this.el.clientHeight - svg.clientHeight
        svg.style.transform = `translate(${w / 2}px,${h / 2}px)`

    }
    mermaid_run() {
        mermaid.run({
            nodes: [this.el],
            postRenderCallback: () => this.on_load(),
            suppressErrors: true
        });
    }
    set_graph(lines: string[]) {
        this.el.removeAttribute("data-processed")
        this.set_html(lines.join("\n"))
        web_dom.next_frame(() => this.mermaid_run())
    }
    on_mount(): void {
    }
}
export class MeraGraph extends MeraUtil {
    render_tmp_store: any
    render_edges(edges: any, lines: string[]) {
        for (var i = 0; i < edges.length; i++) {
            lines.push([
                this.get_title(edges[i][0]),
                this.get_line_text(edges[i][2], edges[i][3], edges[i][4]),
                this.get_title(edges[i][1])
            ].join(" "))
        }
    }
    get_edges() {
        let edges = []
        this.option.data.nodes = {}

        let dfs = (op: Node) => {
            this.option.data.nodes[op.key] = op
            for (var i = 0; i < op.childs.length; i++) {
                edges.push([op.key, op.childs[i].key])
                dfs(op.childs[i])
            }
        }
        dfs(this.option)
        return edges
    }
    render_option(): void {
        this.render_tmp_store = {}
        let lines = ['graph']
        let edges = this.option.data.edges
        if (edges) {
            this.render_edges(edges, lines)
        } else (
            this.render_edges(this.get_edges(), lines)
        )
        console.log(lines.join("\n"))
        this.set_graph(lines)
    }

    get_line_text(s: any, s1: any, s2: any) {
        let line_text = "-->"
        if (s != null) {
            line_text = '<-->|' + s + '|'
        }
        return line_text
    }
    get_title(key: any) {
        if (key in this.render_tmp_store) {
            return key
        }

        let data = this.option.data.nodes[key].data
        if (!Array.isArray(data)) {
            data = [data]
        }
        let lines = []
        for (var i = 0; i < data.length; i++) {
            let title = data[i].title
            if (title) {
                title += ':'
            }
            lines.push(`<p>${title}<span style='color:${data[i].color};margin-left:4px'>${data[i].value}</span></p>`)
        }
        this.render_tmp_store[key] = `${key}(${lines.join("")})`
        return this.render_tmp_store[key]
    }
}
export function mera_util() {
    return new MeraUtil()
}