from common.util.export import List, Dict, MockCf, CT, functools


class Solution(MockCf):
    uri = "https://www.luogu.com.cn/problem/P2123"
    """  A,B 为正整数
    MA[i] = SUM(A[:i+1])
    C[i] = A[i] + B[i] i==1
         = max(C[i-1], MA[i]) + B[i] i>=2
    求C[n]的最小值
    考虑 位置 i, i+1,i-1，如果交换能使C[i+1]变小
    不交换
        C[i+1] = max(
            C[i-1] + B[i] + B[i+1], 
            MA[i-1] + A[i] + B[i] + B[i+1],
            MA[i-1]+ A[i]+ A[i+1]+ B[i+1]
        )
    交换 i,i+1
        C[i+1] = max(
            C[i-1]+B[i+1]+B[i],
            MA[i-1]+A[i+1]+B[i+1]+B[i],
            MA[i-1]+A[i]+A[i+1]+B[i],
        )
    如果交换能使C[i+1]变小，则交换
        1. 
        
        max(
            C[i-1]+B[i+1]+B[i],
            MA[i-1]+A[i+1]+B[i+1]+B[i],
            MA[i-1]+A[i]+A[i+1]+B[i],
        ) <
        max(
            C[i-1] + B[i] + B[i+1], 
            MA[i-1] + A[i] + B[i] + B[i+1],
            MA[i-1]+ A[i]+ A[i+1]+ B[i+1]
        )
        2. 由于max(a,b) < max(a,c) 的充分条件是 b<c
        3. 所以化简可得 
        
        max(
            MA[i-1]+A[i+1]+B[i+1]+B[i],
            MA[i-1]+A[i]+A[i+1]+B[i],
        ) < 
        max(
            MA[i-1] + A[i] + B[i] + B[i+1],
            MA[i-1]+ A[i]+ A[i+1]+ B[i+1]
        )

        4.继续化简 

        A[i+1]+B[i]+max(B[i+1],A[i]) 
        <
        A[i]+B[i+1]+max(A[i+1],B[i])

        5.继续化简 
        
        A[i+1]+B[i]-max(A[i+1],B[i]) == min(A[i+1],B[i])
        < 
        A[i]+B[i+1]-max(A[i],B[i+1]) == min(A[i],B[i+1])
    
        
        min(A[i+1],B[i]) <  min(A[i],B[i+1]) 则交换


    """

    def calc(self, nums: list):
        s = 0
        n = len(nums)
        c = [0] * (n + 1)

        def compare(task1, task2):
            x1, y1 = task1
            x2, y2 = task2
            # 比较 min(x1, y2) 和 min(y1, x2)
            val1 = CT.min(x1, y2)
            val2 = CT.min(y1, x2)
            if val1 < val2:
                return -1
            elif val1 > val2:
                return 1
            else:
                return 0

        nums.sort(key=functools.cmp_to_key(compare))
        for i in range(1, n + 1):
            x, y = nums[i - 1]
            s += x
            c[i] = CT.max(c[i - 1], s) + y

        return c[n]

    def execute(self):
        ans = []
        for _ in range(int(self.input())):
            nums = []
            for _ in range(int(self.input())):
                nums.append(self.ii())
            ans.append(self.calc(nums))
        return "\n".join([str(v) for v in ans])


if __name__ == "__main__":
    print(Solution().execute())
