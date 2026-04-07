from common.util.export import MockCf


class Solution(MockCf):
    """
    给定两个长度分别为n,m的strn,strm
    其中strn由TF两个字符构成,strm由小写字母构成
    我们需要构造一个长度为n+m的目标字符t,使得t的字典序最小
    使得t的n个长度为m的子串subt[i]
    如果strn[i]==T,那么subt[i]==strm
    如果strn[i]==F,那么subt[i]!=strm
    通过strn的T我们可以确定字符t的部分位置
    剩下的位置我们可以都先填入'a',这样能使得t的字典序最小
    包含待定a的字串不等于strm
    不包含待定a的字串等于strm
    采用贪心的策略
    对于strn的每个不满足的F，从左到右
    我们找到最后一个待定a，将它改成b
    需要担心的是，改成b后会不会导致后面的f不成立
    假设
    strm AbBaC
    AbB?C
      A?BaC
    BaC 为 AbBaC 的前缀
    A 为 AbBaC 的后缀

    如果|B|==|A|
    则 BaC不可能为AbB前缀

    如果|B|<|A|
    A = BD
    BaC 为 BDbBaC 的前缀
    aC 为 DbBaC 的前缀
    |C|=|D|
    C=Eb D=aE
    BD 为 BDbBaC 的后缀
    BaE 为 BDbBaEb
    Eb长为|aE|的后缀 不可能为aE

    如果|B|>|A|
    B=DA
    DAaC 为 AbDAaC 的前缀
    DAa 的长为|DAc|的前缀不可能为 AbD
    """

    def get_cases(self):
        return dict(
            case0=dict(str1="TFTF", str2="ab", result="ababa"),
            case1=dict(str1="F", str2="da", result="aa"),
        )

    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        s = [""] * (n + m - 1)
        t = ["a"] * (n + m - 1)
        for i, v in enumerate(str1):
            if v == "T":
                for j in range(m):
                    if s[i + j] and s[i + j] != str2[j]:
                        return ""
                    t[i + j] = s[i + j] = str2[j]
        for i, v in enumerate(str1):
            if v == "F":
                k = None
                for j in range(m - 1, -1, -1):
                    if s[i + j] == str2[j]:
                        return ""
                    if t[i + j] == str2[j]:
                        if s[i + j] == "" and k is None:
                            k = i + j
                    else:
                        k = None
                        break
                if k is not None:
                    t[k] = "b"
        return "".join(t)

    execute = generateString
