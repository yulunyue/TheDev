import { GNode } from "./gnode";
let ARROW_WIDTH = 10
export let ARROW_KEY = 'arrow'
export let ARROW_START = 'start'
export let ARROW_END = 'end'
export class Marker extends GNode {
    key: string
    arg1: string
    arg2: string
    id: string
    constructor(key: string, arg1: string, arg2: string) {
        super("marker")
        this.key = key
        this.arg1 = arg1
        this.arg2 = arg2
        this.id = this.key + this.arg1 + this.arg2
        this.update_attr()
        this.update_node()
    }
    update_attr(): void {
        this.set_attrs({
            orient: "auto",
            id: this.id,
            markerWidth: this.get_width(),
            markerHeight: this.get_height(),
            refX: this.get_refy(),
            refY: this.get_refx(),
            viewBox: "0 0 20 20"
        })
    }
    update_node() {
        if (this.key == ARROW_KEY) {
            let l = new Line().set_style({
                stroke: Constant.COLOR_BLACK,
                fill: Constant.COLOR_BLACK
            })
            if (this.arg1 == ARROW_START) {
                l.set_d("M-20,5 L0,0 L-10,10 Z")
            } else {
                l.set_d("M0,5 L10,10 L0,15 Z")
            }
            this.add_child(l)
        }
    }
    get_width() {
        return 10
    }
    get_height() {
        return 10
    }
    get_refy() {
        if (this.key == ARROW_KEY) {
            return 5
        }
        return 10
    }
    get_refx() {
        if (this.key == ARROW_KEY) {
            if (this.arg1 == ARROW_START) {
                return 0
            } else {
                return 11
            }
        }
        return 0
    }
}
