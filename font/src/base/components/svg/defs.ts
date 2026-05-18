import { Constant } from "../export";
import { GNode } from "./gnode";
import { Line } from "./line";
import { Marker } from "./marker";



export class Defs extends GNode {
    node_uk: any
    static svgs: any[]
    static markers: { [key: string]: any }
    constructor() {
        super("defs")
        this.node_uk = {}
    }
    static init() {
        Defs.svgs = []
        Defs.markers = {}
    }
    init_node(): void {

    }
    add_marker(key: string, arg1: string, arg2: string = "") {
        let k = key + arg1 + arg2
        if (k in this.node_uk) {
            return this.node_uk[k]
        }
        this.node_uk[k] = this.add_child(new Marker(key, arg1, arg2))
        return this.node_uk[k]
    }
    set_parent(p: any): this {
        p.def = this
        Defs.svgs.push(p)
        Defs.update_marker()
        return super.set_parent(p)
    }
    static update_marker() {
        for (var i = 0; i < Defs.svgs.length; i++) {
            for (var k in Defs.markers) {
                let op = Defs.markers[k]
                Defs.svgs[i].def.add_marker(op[0], op[1], op[2])
            }
        }
    }
    static marker_id(key: string, arg1: string, arg2: string = "") {
        let k = key + arg1 + arg2
        Defs.markers[k] = [key, arg1, arg2]
        Defs.update_marker()
        return 'url(#' + k + ')'
    }
}
Defs.init()