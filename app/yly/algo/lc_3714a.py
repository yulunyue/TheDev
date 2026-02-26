from common.util.export import MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(s="abbac", result=4),
            case1=dict(s="aba", result=2),
            case2=dict(s="aabcc", result=3),
            case3=dict(s="accc", result=3),
        )

    def longestBalanced(self, s: str) -> int:
        n = len(s)
        ca = cb = cc = 0  # 当前前缀中 a,b,c 的计数
        pos = {}  # 状态 -> 首次出现位置的前一个索引
        ans = 1
        t = ""  # 当前前缀的去重顺序（按最后出现）
        sufs = [""] * n  # 每个位置的后缀去重顺序

        # 预处理所有后缀的去重顺序
        for i in range(n - 1, -1, -1):
            v = s[i]
            t = t.replace(v, "") + v
            sufs[i] = t

        t = ""
        for i, v in enumerate(s):
            # ---- 第一组状态：使用当前计数（未包含 s[i]）----
            suf = sufs[i]
            mask = 0
            min_ch = "c"
            # 从后向前遍历后缀中的每个字符（即每个可能的子状态）
            for j in range(len(suf) - 1, -1, -1):
                ch = suf[j]
                if ch < min_ch:
                    min_ch = ch

                # 获取最小字符对应的计数
                if min_ch == "a":
                    min_cnt = ca
                elif min_ch == "b":
                    min_cnt = cb
                else:
                    min_cnt = cc

                # 复制当前计数
                da, db, dc = ca, cb, cc
                # 对后缀从 j 开始的每个字符减去 min_cnt
                for idx in range(j, len(suf)):
                    c = suf[idx]
                    if c == "a":
                        da -= min_cnt
                    elif c == "b":
                        db -= min_cnt
                    else:
                        dc -= min_cnt

                # 更新掩码（a->1, b->2, c->4）
                if ch == "a":
                    mask |= 1
                elif ch == "b":
                    mask |= 2
                else:
                    mask |= 4

                key = (mask, da, db, dc)
                if key not in pos:
                    pos[key] = i - 1

            # ---- 更新当前字符的计数和前缀顺序 ----
            if v == "a":
                ca += 1
            elif v == "b":
                cb += 1
            else:
                cc += 1
            t = t.replace(v, "") + v

            # ---- 第二组状态：使用更新后的计数 ----
            suf = t
            mask = 0
            min_ch = "c"
            for j in range(len(suf) - 1, -1, -1):
                ch = suf[j]
                if ch < min_ch:
                    min_ch = ch

                if min_ch == "a":
                    min_cnt = ca
                elif min_ch == "b":
                    min_cnt = cb
                else:
                    min_cnt = cc

                da, db, dc = ca, cb, cc
                for idx in range(j, len(suf)):
                    c = suf[idx]
                    if c == "a":
                        da -= min_cnt
                    elif c == "b":
                        db -= min_cnt
                    else:
                        dc -= min_cnt

                if ch == "a":
                    mask |= 1
                elif ch == "b":
                    mask |= 2
                else:
                    mask |= 4

                key = (mask, da, db, dc)
                if key in pos:
                    ans = max(ans, i - pos[key])

        return ans

    execute = longestBalanced
