
import { DivFactory } from "./base/div_factory"
import { Div } from "./base/div"


export class Container extends Div {
    main: Div
    init_style(): void {
        this.set_style({
            overflow: "auto",
            minHeight: 0,
        })
    }
    render_option() {
        this.main = DivFactory.new_div(
            this.option.type, this.option.key
        ).set_option(this.option)
        this.clear().add_child(this.main)
    }
    get_value() {
        return this.main.get_value()
    }
    set_value(value: any): this {
        this.main.set_value(value)
        return this
    }
}
export { Div, DivFactory }