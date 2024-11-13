import { Div,div } from "./div";
import Constant from "../../web/constant";
import web_dom from "../../web/web_dom"

export class Dialog extends Div {
    container:Div
    header:Div
    main:Div
    init_node() {
        web_dom.get_body().appendChild(this.el)
        this.main=this.add_child(div())
        this.header=this.add_child(div())
        this.container=this.main.add_child(div())
    }

    init_style(): void {
        this.set_style_ab_full().set_style({
            zIndex: "2",
            backgroundColor: "#8888"

        })
        this.main.set_style_ab_center().set_style({
            backgroundColor:"#fff",
        })
        this.hide()
    }
    init_event(): void {

    }
    open(c:any){
        this.container.clear().add_child(c)
        this.show()
        web_dom.bind_click(this.el,()=>{
            this.hide()
        })
        web_dom.bind_click(this.container.el,()=>{
        })
    }

}
export default new Dialog()