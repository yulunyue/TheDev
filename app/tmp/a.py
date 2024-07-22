from util.fun import sub


class Route:
    def add(self, a, b):
        return dict(c=a+b)

    def sub(self, a, b):
        return dict(c=a-b)


def task(c=1):
    return c+2
