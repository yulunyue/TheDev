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
function node_to_grapth_lines(node: Node) {
    let ret = [node.value]
    function arrow(f: string) {
        if (f) {
            return `--->|${f}|`
        }
        return '-----'
    }
    for (var key in node.data) { 
        let edges = node.data[key]
        if (edges) {
            for (var j = 0; j < edges.length; j++) {
                ret.push(`${key} ${arrow(edges[j][1])} ${edges[j][0]}`)
            }
        } else {
            ret.push(key)
        }
    }
    console.log(ret.join("\n"))
    return ret.join("\n")
}
export class MeraGraph extends Div {

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

        let svg = (this.el.children[0] as any)
        if (!svg || !svg.clientWidth) {
            return
        }
        let w = this.el.clientWidth - svg.clientWidth
        let h = this.el.clientHeight - svg.clientHeight
        svg.style.transform = `translate(${w / 2}px,${h / 2}px)`
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
    set_graph(lines: string) {
        this.el.removeAttribute("data-processed")
        this.set_html(lines)
        web_dom.next_frame(() => this.mermaid_run())
    }
    on_mount(): void {
    }
    render_option(): void {
        let lines = node_to_grapth_lines(this.option)
        this.set_graph(lines)
    }
}


export function mera_util() {
    return new MeraGraph()
}