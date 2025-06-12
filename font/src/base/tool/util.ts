
import web_dom from "../web/web_dom"
import { Node } from "../web/cls"
export class UtilCls {
    url_to_json(s: string) {
        var ret = {}
        var s1 = s.split('&')
        for (var i = 0; i < s1.length; i++) {
            var s2 = s1[i].split('=')
            ret[s2[0]] = s2[1]
        }
        return ret
    }
    extend(a: any, b: any) {
        for (var key in b) {
            a[key] = b[key]
        }
    }
    object_to_get_param(oj: any, rt?: string) {
        if (rt == undefined) {
            rt = "";
        }
        let flag = true;
        for (var key in oj) {
            if (flag == true) {
                flag = false;
                rt += "?";
            } else {
                rt += "&";
            }
            rt = rt + key + "=" + oj[key];
        }
        return rt;
    }

    hash_any(c: any) {
        let res = ""
        if (Array.isArray(c)) {
            for (var i = 0; i < c.length; i++) {
                res += this.hash_any(c[i])
            }
        } else if (c.constructor === Object) {
            let keys = Object.keys(c).sort()
            for (var i = 0; i < keys.length; i++) {
                res += keys[i] + this.hash_any(c[keys[i]])
            }
        } else {
            res += c
        }
        return res
    }
    uri_join(array: string[]) {
        let ret = ""
        for (var v in array) {
            if (ret.endsWith("/") && v.startsWith("/")) {
                ret += v.slice(1)
            } else if (ret.endsWith("/") || v.startsWith("/")) {
                ret += v
            } else {
                ret += "/" + v
            }
        }
        return ret
    }
    array(num: number, fun: any) {
        let ret = []
        for (var i = 0; i < num; i++) {
            ret.push(fun(i))
        }
        return ret
    }
}
export default new UtilCls()