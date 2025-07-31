class Solution:
    def get_cases(self):
        return [
            dict(n=10101, result="一万零一百零一"),
            dict(n=22001121, result="二千二百万零一千一百二十一"),
            dict(n=2200121, result="二百二十万零一百二十一"),
        ]

    def execute(self, n):
        danwei = "万十百千万"
        wei = "零一二三四五六七八九"
        cc = ["", "万"]
        result = []
        jw = 0
        last_a = None
        while n:
            a = n % 10
            if a == last_a == 0:
                jw += 1
                n = n // 10
                continue
            if a and 1 <= jw:
                if cc[jw // len(danwei)]:
                    result.insert(0, cc[jw // len(danwei)])
                    cc[jw // len(danwei)] = ""
                result.insert(0, danwei[(jw % (len(danwei) - 1))])
            result.insert(0, wei[a])
            jw += 1
            n = n // 10
            last_a = a
        return "".join(result)
