
import {
    Div, Node, web_dom, MeraGraph, to_node
} from "../base/components/export";

export class Graph extends Div {
    mera: MeraGraph
    init_node(): void {
        this.mera = this.add_child(new MeraGraph().full())
    }
    on_mount(): void {
        let path = web_dom.get_param("json_path")
        if (path) {
            web_dom.post('/app/tool/file/read', {
                path
            }, (v: any) => {
                this.mera.set_option(to_node({ data: v.value }))
            })
        } else {
            this.mera.set_option(this.get_test_data())
        }
    }
    get_test_data() {
        return new Node().set_data({
            edges: [
                ['A', 'B', 'AB'],
                ['A', 'C'],
                ['B', 'C'],
                ['C'],
                ['D']
            ],
            nodes: {
                C: [{
                    title: "C1",
                    color: "#888"
                }, {
                    title: "C2",
                    color: "#ddd",
                    value: "xxx"
                }],
                B: {
                    title: "BT",
                }
            }
        })
    }
}
export default function () {
    return new Graph()
}