import { Fn3Void } from "../../../web/cls"
import Constant from "../../../web/constant"

export class Lifecycle {
    event_hander: any
    constructor() {
        this.event_hander = {}
    }
    init_node() {

    }
    init_style() {

    }
    init_event() {

    }
    on_render() {

    }
    on_mount() {

    }
    render() {

    }
    render_option() {

    }
    do_change(key: string, src?: any, dst?: any) {
        if (src == null && dst == null) {
            return this
        }
        this.event_hander[Constant.EVENT_CHANGE]?.(key, src, dst)
        return this
    }
    on_change(call: Fn3Void<string, any, any>) {
        this.event_hander[Constant.EVENT_CHANGE] = call
        return this
    }
    on_move(call: any) {
        this.event_hander[Constant.EVENT_MOVE] = call
        return this
    }
    do_select(arg: any) {
        this.event_hander[Constant.EVENT_CHANGE]?.((this as any)._value, arg)
        ;(this as any)._value = arg
        return this
    }
    on_select(call: any) {
        this.event_hander[Constant.EVENT_CHANGE] = call
        return this
    }
}
