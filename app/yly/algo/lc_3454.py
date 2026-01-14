class Solution:
    def get_cases(self):
        return dict(case0=squares = [[0,0,1],[2,2,1]]

输出： 1.00000=)
    def separateSquares(self, squares: List[List[int]]) -> float:
        c=defaultdict(list)
        mx=0
        for x,y,l in squares:
            c[y].append([x,x+l,1])
            c[y+l].append([x,x+l,-1])
            mx=max(mx,x+l)
        t=T().set_range(0,mx)
        sa=[]
        ly=None
        for y in sorted(c.keys()):
            t.update(*c[y])
            if ly is not None:
                sa.append([sa[-1][0]+lx*(y-ly),y,lx])
            else:
                sa.append([0,y])
            lx,ly=t.query(0,mx),y
        mid=sa[-1][0]//2
        idx=bisect.bisect_left(sa,[mid])
        return sa[idx][1]+(mid-sa[idx][0])//sa[idx+1][2]
        
