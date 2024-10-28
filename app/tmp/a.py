import time
a=time.time()
c=[0]*5
d=0
for i in range(10**8):
    # c.append(0)
    # # d+=1
    # c.pop()
    d+=1
    d-=1
print(time.time()-a)