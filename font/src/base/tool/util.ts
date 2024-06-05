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
}
export default new Util()