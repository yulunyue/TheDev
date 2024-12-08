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
    on_load(){
        let svg=(this.el.children[0] as any)
        if(!svg || !svg.clientWidth){
            return
        }
        let w=this.el.clientWidth-svg.clientWidth
        let h=this.el.clientHeight-svg.clientHeight
        svg.style.transform=`translate(${w/2}px,${h/2}px)`
        // svg.style.position='fixed'
        // svg.style.top="50%"
        // svg.style.left="50%",
        // svg.style.transform="translate(-50%,-50%)"
    }
    mermaid_run() {
        mermaid.run({
            nodes:[this.el],
            postRenderCallback:()=>this.on_load(),
            suppressErrors:true
        });        
    }
    set_graph(lines:string[]){
        this.el.removeAttribute("data-processed")
        this.set_html(lines.join("\n"))
        web_dom.next_frame(()=>this.mermaid_run())
    }
    on_mount(): void {
    }
}
export class MeraGraph extends MeraUtil {
    render_option(): void {
        let lines = ['graph']
        let edges = this.option.data.edges
        if(!edges){
            return
        }
        for (var i=0;i<edges.length;i++) {
            let line_text="---"
            if(edges[i][2]!=null){
                line_text='<-->|'+edges[i][2]+'|'
            }
            lines.push("   " + edges[i][0] +  line_text+edges[i][1] + ';')
           
        }
        this.set_graph(lines)
    }
}
export function mera_util() {
    return new MeraUtil()
}