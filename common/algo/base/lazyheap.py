import heapq


class LazyMinHeap:
    def __init__(self, size):
        self.size = size
        self.h = []
        self.sum = 0

    def add(self, v):
        heapq.heappush(self.h, v)
        self.sum += v
        if len(self.h) > self.size:
            return self.pop()

    def pop(self):
        return heapq.heappop(self.h)

    def top(self):
        return self.h[0]


class LazyMaxHeap(LazyMinHeap):
    def add(self, v):
        return super().add(-v)

    def top(self):
        return -super().top()

    def pop(self):
        return -super().pop()


class LazyHeapMinMax:
    def __init__(self, min_size, max_size):
        self.min_heap = LazyMinHeap(min_size)
        self.max_heap = LazyMaxHeap(max_size)

    def add(self, v):
        u = self.min_heap.add(v)
        if u is not None:
            self.max_heap.add(u)

    def adds(self, array):
        for a in array:
            self.add(a)

    def __str__(self):
        return f"min:{self.min_heap.h},max:{self.max_heap.h}"
