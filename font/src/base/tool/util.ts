
import web_dom from "../web/web_dom"
import {Node} from "../web/cls"
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
    grid_size(sizes:any[]){
        let n=new Node().set_size(0)
        for(var i=0;i<sizes.length;i++){
            let tmp=null
            if(Array.isArray(sizes[i])){
                tmp=this.grid_size(sizes[i])    
            }else{
                tmp=new Node().set_size(sizes[i])
            }
            n.add_child(tmp)
            n.size+=tmp.size
        }
        return n
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

}
export default new UtilCls()