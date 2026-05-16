import { Style, Node, Fn1, to_node, not_null, node } from "../../../web/cls"
import { GNode } from "../../export"
import { Div } from "./div"

export class DivFactory {
    static fac_map: { [key: string]: any }
    static fac_svg_map: { [key: string]: any }
    static instance: { [key: string]: any }
    static set(key: string, value: any) {
        DivFactory.instance[key] = value
        return value
    }
    static get(key: string) {
        if (!DivFactory.instance[key]) {
            console.log(DivFactory.instance)
        }
        return DivFactory.instance[key]
    }
    static register(key: string, fun: any) {
        DivFactory.fac_map[key] = fun
    }
    static register_svg(key: string, fun: any) {
        DivFactory.fac_svg_map[key] = fun
    }
    static new_svg(type: string, key: string): GNode {
        // console.log(key, DivFactory.fac_map)
        if (!DivFactory.fac_svg_map[type]) {
            console.error(key, type, Object.keys(DivFactory.fac_svg_map))
        }
        return DivFactory.set(key, DivFactory.fac_svg_map[type]())
    }
    static new_div(type: string, key: string): Div {
        // console.log(key, DivFactory.fac_map)
        if (!DivFactory.fac_map[type]) {
            console.error(key, type, Object.keys(this.fac_map))
        }
        return DivFactory.set(key, this.fac_map[type]())
    }
}
DivFactory.fac_map = {}
DivFactory.fac_svg_map = {}
DivFactory.instance = {}