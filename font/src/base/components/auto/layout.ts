import { Div } from "../dom/div"
export class Layout extends Div {
    static VERTICAL: number = 0
    static HORIZONTAL: number = 1
    direction: number
    constructor(direction: number) {
        super("div")
        this.direction = direction
    }
}
export default function (direction: number) {
    return new Layout(direction)
}