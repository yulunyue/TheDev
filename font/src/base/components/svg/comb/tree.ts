import { Node } from "../../export";
import { GNode, gnode } from "../gnode";
import { Svg } from "../svg";
export class TreeNode extends GNode {

}
export class Tree extends Svg {
    width: number
    height: number
    max_xy: any
    set_option(option: Node): this {
        this.max_xy = option.init_layout()
        this.option = option
        this.draw()
        return this
    }
    draw() {
        if (!this.width || !this.height || !this.option) {
            return
        }
        this.option.dfs((node: Node) => {

        })
    }
    on_mount(): void {
        this.width = this.parent.get_width()
        this.height = this.parent.get_height()
        this.draw()
    }
}
export function tree() {
    return new Tree
}