
import {
    Div
} from "../base/components/export";
export class Temaplate extends Div {

    init_node(): void {
        this.set_html("template")
    }
    on_mount(): void {

    }

}
export default function () {
    return new Temaplate()
}