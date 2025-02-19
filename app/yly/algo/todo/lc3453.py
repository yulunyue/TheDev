from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/separate-squares-i/description/'
    def get_cases(self):
        return [
            dict(squares =[[0,0,1],[2,2,1]],result=1.00000),
            dict(squares=[[0,0,2],[1,1,1]],result=1.16667)
        ]
    def separateSquares(self, squares: List[List[int]]) -> float:
        tot = 0
        # 差分
        diff = defaultdict(int)
        for _, y, l in squares:
            tot += l*l
            diff[y] += l
            diff[y+l] -= l
        prey = 0  # 前一纵坐标
        width = 0  # 正方形宽度之和
        cur = 0  # 下方总面积
        for y in sorted(diff):
            # 尝试将这部分面积加入总面积
            tmp = cur + (y - prey) * width
            if tmp * 2 >= tot:
                return prey + (tot / 2 - cur) / width
            prey = y
            width += diff[y]
            cur = tmp
    def separateSquares(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self,squares):
        n=len(squares)
        sc=100000
        mx,mn=-inf,inf
        for i in range(n):
            squares[i][1]*=sc
            mx=max(squares[i][1]+squares[i][2]*sc,mx)
            mn=min(squares[i][1],mn)
        def check(h):
            up,low=0,0
            for _,y,c in squares:
                up+=min(max(y-h+sc*c,0),c*sc)*c
                low+=min(max(h-y,0),c*sc)*c
            # self.log(h,low,up)
            return low>=up-1
        return (bisect.bisect_left(range(mn,mx),True,key=check)+mn)/sc



if __name__=='__main__':
    Solution().run()