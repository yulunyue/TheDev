import { Div } from "../../dom/div";
import mermaid from "mermaid";
import { Svg, Node } from "../../export";
import { line, web_dom } from "../../export";
import createPanZoom from "panzoom";
mermaid.initialize({
    //theme: 'neutral',
    //look: "handDrawn",
    themeCSS: '.node rect { fill: white; }',

    logLevel: 3,
    securityLevel: 'antiscript',
    flowchart: { curve: 'basis' },
    gantt: { axisFormat: '%m/%d/%Y' },
    sequence: { actorMargin: 50 },

    // sequenceDiagram: { actorMargin: 300 } // deprecated
})
export class MeraUtil extends Div {

    constructor() {
        super("pre")
    }
    init_style(): void {
        this.full()
    }
    on_load_room() {
        const container = this.el;
        const svgElement = container.querySelector("svg");

        // Initialize Panzoom
        const panzoomInstance = createPanZoom(svgElement, {
            //maxScale: 5,
            // minScale: 0.5,
            // step: 0.1,
        });

        // Add mouse wheel zoom
        container.addEventListener("wheel", (event) => {
            // panzoomInstance.zoomWithWheel(event);
        });
    }
    on_load() {

        // let svg = (this.el.children[0] as any)
        // if (!svg || !svg.clientWidth) {
        //     return
        // }
        // let w = this.el.clientWidth - svg.clientWidth
        // let h = this.el.clientHeight - svg.clientHeight
        // svg.style.transform = `translate(${w / 2}px,${h / 2}px)`
        this.on_load_room()
        this.load_event()
    }
    load_event(): void {
        let ps = this.el.querySelectorAll('div')
        var register_click = (v: HTMLDivElement) => {
            let name = v.getAttribute("name")
            if (!name) {
                return
            }
            // console.error(this.option.data.nodes,name)
            let color = this.option.data.nodes[name].color
            v.style.background = color
            v.onclick = () => { this.do_select(name) }
        }
        for (var i = 0; i < ps.length; i++) {
            register_click(ps[i])
        }
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
                this.get_line_text(edges[i][1], edges[i][2], edges[i][3], edges[i][4]),

            ].join(" "))
        }
    }
    get_edges() {
        let edges = []
        this.option.data.nodes = {}

        let dfs = (op: Node) => {
            this.option.data.nodes[op.key] = op.data
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
        let dire = this.option.data.direction || 'TD'
        let lines = ['graph ' + dire]
        let edges = this.option.data.edges
        if (edges) {
            this.render_edges(edges, lines)
        } else (
            this.render_edges(this.get_edges(), lines)
        )
        //console.error(lines.join("\n"))
        this.set_graph(lines)
    }

    get_line_text(ss: string, s: any, s1: any, s2: any) {
        if (ss == undefined || ss == null) {
            return ""
        }
        let line_text = "-->"
        if (s != null) {
            line_text = '-->|' + s + '|'
        }
        return line_text + this.get_title(ss)
    }
    get_title(key: any) {
        if (key in this.render_tmp_store || !this.option.data.nodes) {
            return key
        }
        let data = this.option.data.nodes[key]
        if (data == undefined || data == null) {
            return key
        }
        if (!Array.isArray(data)) {
            data = [data]
        }
        let lines = [`<div name="${key}" style="width:90px">`]
        for (var i = 0; i < data.length; i++) {
            let title = data[i].title
            if (title) {
                title += ':'
            }
            lines.push(`<p>${title}
                <span style='color:${data[i].color};margin-left:4px'>${data[i].value}
                </span>
            </p>`)
        }
        lines.push('</div>')
        this.render_tmp_store[key] = `${key}(${lines.join("")})`
        return this.render_tmp_store[key]
    }
}
export function mera_util() {
    return new MeraGraph()
}