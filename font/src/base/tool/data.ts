import { dialog } from "../components/export"
import web_dom from "../web/web_dom"
export class Data {
    get_user_name() {
        let user_name = web_dom.get_local("user_name")
        if (!user_name) {
            dialog.open_form({
                user_name: "input"
            }, (data: any) => {
                web_dom.set_local("user_name", data.user_name)
                dialog.alart("登录成功请重试")
            })
        }
        return user_name

    }
}
export default new Data()
