import { GNode } from "../gnode";
import web_dom from "../../../web/web_dom"
import { Line, line } from "../line";
import { Rect, rect } from "../rect";
import { Circle, circle } from "../circle";
import { Text, text } from "../text";
import { Node } from "../../../web/cls";
import { Svg } from "../svg";
import Constant from "../../../web/constant";
class ProgrePoint extends GNode {
    rect: Rect
    text: Text

    init_node(): void {

    }
}

export class Progress extends GNode {
    main_line: Line
    cur_point: Circle
    points: ProgrePoint[]
    progre_points: GNode
    bg: Rect
    cur_point_x:number
    cur_point_y:number
    init_node(): void {
        this.points = []
        this.bg = this.add_child(new Rect())
        this.main_line = this.add_child(new Line().with_arrow())
        this.cur_point = this.add_child(new Circle())
        this.progre_points = this.add_child(new GNode())
    }
    init_event() {
        web_dom.bind_drag(this.el, (state: string, x: number, y: number) => {
            if(state == 'start'){
                //this.cur_point.set_color(Constant.COLOR_YELLOW)
                this.cur_point.x=this.cur_point.get_x()
                this.cur_point.y=this.cur_point.get_y()
            }
            else if(state=='move'){
                this.cur_point.set_x(
                    this.cur_point.x+x
                )
            }else{
                // this.cur_point.set_color(Constant.COLOR_BALCK)
            }
        })

    }
    draw() {
        let rect = this.parent.get_rect()
        let margin = 10
        let height = rect.height / 2
        this.bg.set_wh(rect.width, rect.height)
        this.main_line.set_d([
            { x: margin, y: height },
            { x: rect.width - margin * 2, y: height }
        ])
        this.cur_point.set_pos(margin, height).set_r(5)
    }
    on_mount(): void {
        this.draw()
    }
    set_option(option: Node): this {
        return this
    }

}
export function progress_dev() {
    return new Progress()
}
export function progress() {
    return new Progress()
}