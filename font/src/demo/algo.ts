
import {
    Div, Svg, svg, Constant, Node,web_dom,
    svg_node_factory, line, gnode, GNode, button, progress, div, input, Input,Progress
} from "../base/components/export";
class Algo extends Div {
    div: Div
    pro: Progress
    svg_nodes:Svg[]
    init_style(): void {
        this.full()
    }
    init_node() {
        this.div = div()
        this.pro=progress().set_size(1).change((v:number)=>this.goto(v))
        this.add_childs([
            this.div.set_size(1),
            div().add_childs([
                this.pro,
                button().set_html("setting"),
                button().set_html("run").click(()=>this.load())
            ]).set_height(Constant.DEFAULT_LINE_HEIGHT)
        ]).flex_horizontal_layout()
    }
    set_option(option: Node): this {
        this.option=option
        this.svg_nodes=[]
        this.div.clear().add_grid_childs(
            option.childs[0].childs.map(v => {
                let node= svg_node_factory(v.type)
                this.svg_nodes.push(node)
                return svg().add_childs([node]).set_size(1)    
            })
        ).flex_horizontal_layout().emit_mount()
        return this
    }
    goto(idx:number){
        if(!this.option || !this.option.childs[idx]){
            return
        }
        for(var i=0;i<this.option.childs[idx].childs.length;i++){
            console.log(this.option.childs[idx].childs[i])
            this.svg_nodes[i].set_option(this.option.childs[idx].childs[i])
        }
    }
    test() {
        this.set_option(new Node().set_childs([Constant.MOCK_NODE_3_3.set_type("tree")]))
    }
    load(){
        web_dom.post('/app/yly/manage/execute',{},(node:Node)=>{
            //console.log(node)
            this.set_option(node)
            this.pro.set_max_value(node.childs.length)
        })
    }
    on_mount() {
        //this.test()
        this.load()
    }
}
export default function () {
    return new Algo()
}