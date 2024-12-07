import { Div } from "../../dom/div";
import mermaid from "mermaid";
export class MeraUtil extends Div {
    constructor() {
        super("pre")
    }
    init_node(): void {
        this.set_class("mermaid")
    }
    load_mermaid() {
        mermaid.initialize({
            theme: 'default',
            // themeCSS: '.node rect { fill: red; }',
            logLevel: 3,
            securityLevel: 'loose',
            flowchart: { curve: 'basis' },
            gantt: { axisFormat: '%m/%d/%Y' },
            sequence: { actorMargin: 50 },
            // sequenceDiagram: { actorMargin: 300 } // deprecated
        });
    }
    on_mount(): void {
        this.load_mermaid()
    }
}
export class MeraGraph extends MeraUtil {
    render_option(): void {
        let lines = ['graph']
        let g = this.option.data.g
        for (var src in g) {
            for (var i = 0; i < g[src].length; i++) {
                lines.push("   " + src + '-->' + g[src][i] + ';')
            }
        }
        //this.set_html(lines.join("\n"))
        this.load_mermaid()
    }
}
export function mera_util() {
    return new MeraUtil()
}