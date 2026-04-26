
import web_dom from "../web/web_dom"
import { Node } from "../web/cls"
export class UtilCls {
    url_to_json(s: string) {
        var ret = {}
        var s1 = s.split('&')
        for (var i = 0; i < s1.length; i++) {
            var s2 = s1[i].split('=')
            if (s2.length == 2) {
                ret[s2[0]] = s2[1]
            }
        }
        return ret
    }
    str_match(s: string, key: string) {
        return s.indexOf(key) != -1
    }
    url_parse(s: string) {
        let idx = s.indexOf("?")
        if (idx == -1) {
            return { path: s, param: {} }
        }
        let path = s.slice(0, idx + 1)
        return {
            path: path,
            param: this.url_to_json(s.slice(idx + 1,))
        }
    }
    filter_json_array(src: any[], s: string) {
        if (!s) {
            return src
        }
        var sb = this.url_to_json(s)
        let ret = []
        console.log(sb)
        for (var i = 0; i < src.length; i++) {
            if (Object.keys(sb).length != 0 && !this.match_json_by_json(src[i], sb)) {
                continue
            }
            if (!this.match_json_by_key(src[i], s)) {
                continue
            }
            ret.push(src[i])
        }
        return ret
    }
    match_json_by_key(src: any, search_key: string) {

        for (var key in src) {
            let v: string = src[key] + ""
            if (v.indexOf(search_key) != -1) {
                return true
            }
        }
        return false
    }
    match_json_by_json(src: any, filter: any) {
        return false
    }
    extend(a: any, b: any) {
        if (Array.isArray(a)) {
            return a.concat(b)
        }
        else {
            for (var key in b) {
                a[key] = b[key]
            }
        }
        return a
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
        for (var i = 0; i < array.length; i++) {
            let v = array[i]
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