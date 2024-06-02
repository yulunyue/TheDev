import { Div } from "../dom/div"
export class Layout extends Div {
    VERTICAL: number = 0
    HORIZONTAL: number = 1
    direction: number
    constructor(direction: number) {
        super()
        this.direction = direction
    }
}
export default function (direction: number) {
    return new Layout(direction)
}