import { Div } from "../../dom/div";
import mermaid from "mermaid";
import { Svg } from "../../export";
import { line, web_dom } from "../../export";
mermaid.initialize({
    theme: 'default',
    // themeCSS: '.node rect { fill: red; }',
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
    render_option(): void {
        let lines = ['graph']
        let edges = this.option.data.edges
        if (!edges) {
            return
        }
        for (var i = 0; i < edges.length; i++) {
            lines.push([
                this.get_title(edges[i][0]),
                this.get_line_text(edges[i][2], edges[i][3], edges[i][4]),
                this.get_title(edges[i][1])
            ].join(" "))
        }
        this.set_graph(lines)
    }
    get_line_text(s: any, s1: any, s2: any) {
        let line_text = "---"
        if (s != null) {
            line_text = '<-->|' + s + '|'
        }
        return line_text
    }
    get_title(key: string) {
        if (this.option.data && key in this.option.data.nodes) {
            return `${key}(${key}:${this.option.data.nodes[key]})`
        }
        return key
    }
}
export function mera_util() {
    return new MeraUtil()
}