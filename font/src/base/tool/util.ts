export class Util {
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
}
export default new Util()