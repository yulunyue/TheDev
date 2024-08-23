import { Div } from "../base/components/export";
class Algo extends Div {
    init_style(): void {
        this.full()
    }
}
export default function () {
    return new Algo()
}