class WebDom {
    HTTP_GET_METHOD: string = "GET"
    HTTP_POST_METHOD: string = "POST"
    HTTP_CONTENT_TYPE_KEY: string = "Content-type"
    HTTP_CONTENT_TYPE_JSON: string = "application/json"
    HTTP_STATE_FINISH: number = 4

    get_body() {
        return document.body
    }
    createElement(node_type: string) {
        return document.createElement(node_type)
    }
    get_location() {
        return location.href
    }
    get_local(key: string) {
        return localStorage.getItem(key)
    }
    set_local(key: string, value: any) {
        if (typeof value == "object") {
            localStorage.setItem(key, JSON.stringify(value))
        } else {
            localStorage.setItem(key, value)
        }
    }
    xml_http_request(method: string, path: string, data: any, call_back: any) {
        let req = new XMLHttpRequest()
        req.open(method, path)
        if (method == this.HTTP_POST_METHOD) {

        } else if (method == this.HTTP_POST_METHOD) {
            req.setRequestHeader(this.HTTP_CONTENT_TYPE_KEY, this.HTTP_CONTENT_TYPE_JSON)
        }
        req.send(data)
        req.onreadystatechange = (ev: any) => {
            if (req.readyState == this.HTTP_STATE_FINISH) {
                if (req.getResponseHeader(this.HTTP_CONTENT_TYPE_JSON).includes(this.HTTP_CONTENT_TYPE_JSON)) {
                    call_back(JSON.parse(req.responseText))
                } else {
                    call_back(req.responseText)
                }
            }
        }

    }
}
export default new WebDom()