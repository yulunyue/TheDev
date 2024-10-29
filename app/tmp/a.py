import time
a = time.time()
c = [0]*5
d = 0


class A:
    def __init__(self, a) -> None:
        self.a = a


def e(*args):
    pass


c = [(i, 0) for i in range(10**7)]
for f in c:
    # if d == 0:
    #     b = 0
    # elif d == 1:
    #     b = 1
    # elif d == 2:
    #     b = 2
    # elif d == 3:
    #     b = 3
    # else:
    #     b = 4
    b = [1, 0, 2, 3, 5][d]

    # d += 1
    # d -= 1

print(time.time()-a)
