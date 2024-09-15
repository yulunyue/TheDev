import { Node } from "../web/cls";
function draw_tree_view(root: Node,w:number,h:number) {
    this.svg_node.clear()
    let nodes: Node[] = []
    let store_tmp = {}
    let max_depth = 0
    root.dfs((n: Node, i: number, j: number) => {
        if (!store_tmp[i]) {
            store_tmp[i] = 0
        }
        store_tmp[i] += 1
        max_depth = i > max_depth ? i : max_depth
        n.type = n.type || 'text'
        n.data = { i: i, j: store_tmp[i] - 1, r: 5 }
        nodes.push(n)
    }, 0, 0)
    for (var i = 0; i < nodes.length; i++) {
        nodes[i].data.y = h * ((nodes[i].data.i + 0.5) / (max_depth + 1))
        nodes[i].data.x = w * ((nodes[i].data.j + 0.5) / store_tmp[nodes[i].data.i])
        // let n = svg_node_factory(nodes[i])
        // this.svg_node.add_child(n)
        // if (nodes[i].parent) {
        //     this.svg_node.add_child(line().set_d([
        //         { x: nodes[i].parent.data.x, y: nodes[i].parent.data.y },
        //         { x: nodes[i].data.x, y: nodes[i].data.y }
        //     ]).with_arrow())
        // }

    }
}
export class SegTree extends Node {
    left:SegTree
    right:SegTree
    o:number
    l:number
    r:number
    m:number
    build(o:number,l:number,r:number){
        this.o=o
        this.l=l
        this.r=r
        this.value=0
        if(l==r){
            return this
        }
        this.m=Math.floor((l+r)/2)
        this.left = new SegTree().build(o*2,l,this.m)
        this.right = new SegTree().build(o*2,this.m+1,r)
        this.set_childs([this.left,this.right])
        return this
    }
    update(i:number,value:number){
        if(this.l==this.r){
            this.value=value
            return this
        }
        if(i<=this.m){
            this.left.update(i,value)
        }else{
            this.right.update(i,value)
        }
        this.value=Math.max(this.left.value,this.right.value)
        return this
    }
    get_title(): string {
        return `[${this.o}]:[${this.l},${this.r}]:[${this.value}]`
    }
}