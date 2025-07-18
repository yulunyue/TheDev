import { Style, Node, Fn1, to_node, not_null, node } from "../../../web/cls"
import { Div } from "./div"

export class DivFactory {
    static fac_map = {}
    static instance = {}
    static set(key: string, value: any) {
        DivFactory.instance[key] = value
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

    static new_div(key: string): Div {
        // console.log(key, DivFactory.fac_map)
        return this.fac_map[key]()
    }
}