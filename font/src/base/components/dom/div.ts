
import { DivFactory } from "./base/div_factory"
import { Div } from "./base/div"


export class Container extends Div {
    main: Div
    render_option() {
        this.main = DivFactory.new_div(
            this.option.type, this.option.key
        ).set_option(this.option)
        this.clear().add_child(this.main)
    }
    get_value() {
        return this.main.get_value()
    }
}
export { Div, DivFactory }