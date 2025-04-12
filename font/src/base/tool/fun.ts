import { DivFactory } from "../components/export"
class Fun {
    ts_compile(s: string) {
        let ret = []
        let src = s.split("\n")

        for (var key in DivFactory.fac_map) {
            ret.push(`let ${key} = FN_MAP.${key}`)
        }
        for (var i = 0; i < src.length; i++) {
            let value = src[i]
            if (!value) {
                continue
            }
            if (value.startsWith("import")) {
                continue
            }
            if (value.startsWith("export default function")) {
                value = "var FN = function() {"
            }
            ret.push(value)
        }
        ret.push("FN")
        return ret.join("\n")
    }
    eval_ts(s: string) {
        let s1 = this.ts_compile(s)
        let FN_MAP = DivFactory.fac_map
        return eval(s1)

    }
}
export default new Fun()