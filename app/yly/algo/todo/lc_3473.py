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
    我们需要找到最后一个待定a，将它改成b即可

    需要担心的是，改成b后会不会导致后面的


    """

    def get_cases(self):
        return dict(
            case0=dict(str1="TFTF", str2="ab", result="ababa"),
        )

    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        s = [""] * (n + m)
        t = ["a"] * (n + m)
        for i, v in enumerate(str1):
            if v == "T":
                for j in range(m):
                    if s[i + j] and s[i + j] != str2[j]:
                        return ""
                    t[i + j] = s[i + j] = str2[j]
            else:
                pass

    execute = generateString
