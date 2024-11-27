import { dialog, form } from "../components/export"
import web_dom from "../web/web_dom"
export class Data {
    get_user_name(call_back: any) {
        let user_name = web_dom.get_local("user_name")
        if (!user_name) {
            dialog.open_form({
                user_name: "text"
            }, (data: any) => {
                web_dom.set_local("user_name", data.user_name)
                call_back(data.user_name)
            })
        } else {
            call_back(user_name)
        }

    }
}
export default new Data()
