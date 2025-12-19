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

    def calc(self, tasks: list):
        c = s = 0
        n = len(tasks)
        nums = []
        for x, y in tasks:
            if x > y:
                d = 1
            elif x < y:
                d = -1
            else:
                d = 0
            nums.append((x, y, d))
        nums.sort(
            key=lambda task: (
                task[2],  # 先按d排序
                task[0] if task[2] <= 0 else -task[1],  # d<=0按x升序，d>0按y降序
            )
        )
        for x, y, _ in nums:
            s += x
            c = CT.max(c, s) + y

        return c

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
