import { Constant, dialog, FormRow } from "../components/export"
import web_dom from "../web/web_dom"
export class Data {
    get_user_name(call: any) {
        let user_name = web_dom.get_local_data(Constant.username)
        if (!user_name) {
            let t = new FormRow().set_option({
                childs: [{
                    type: Constant.DOM_TYPE_INPUT, key: Constant.username,
                    title: Constant.username
                }]
            }).set_btns({
                login: "登录"
            }).on_submit((type: string, data: any) => {
                web_dom.set_local(Constant.username, data.username)
                call(data.username)
                dialog.close()
            })
            dialog.open(t)
        } else {
            call(user_name)
        }


    }
}
export default new Data()
