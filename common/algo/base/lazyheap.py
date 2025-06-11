import heapq
from collections import defaultdict


class LazyMinHeap:
    def __init__(self):
        self.size = 0
        self.h = []
        self.sum = 0
        self.remove_ct = defaultdict(int)

    def get_value(self, v):
        return v

    def push(self, v):
        value = self.get_value(v)
        if self.remove_ct[value] > 0:
            self.remove_ct[value] -= 1
        else:
            heapq.heappush(self.h, value)
        self.sum += value
        self.size += 1

    def pushpop(self, v):
        value = self.get_value(v)
        self.apply_remove()
        if not self.h or value <= self.h[0]:
            return v
        ret = heapq.heappushpop(self.h, value)
        self.sum += value - ret
        return self.get_value(ret)

    def apply_remove(self):
        while self.h and self.remove_ct[self.h[0]]:
            self.remove_ct[self.h[0]] -= 1
            heapq.heappop(self.h)

    def get_sum(self):
        return self.get_value(self.sum)

    def top(self):
        self.apply_remove()
        return self.get_value(self.h[0])

    def remove(self, v):
        value = self.get_value(v)
        self.remove_ct[value] += 1
        self.size -= 1
        self.sum -= value

    def __str__(self):
        return f"h:{[self.get_value(v) for v in self.h]}, sum:{self.get_value(self.sum)}, size:{self.size}"


class LazyMaxHeap(LazyMinHeap):
    def get_value(self, v):
        return -v


class LazyHeapMinMax:
    def __init__(self):
        self.right_min_heap = LazyMinHeap()
        self.left_max_heap = LazyMaxHeap()

    def pushpop(self, v):
        if self.right_min_heap.size == self.left_max_heap.size:
            self.left_max_heap.push(self.right_min_heap.pushpop(v))
        else:
            self.right_min_heap.push(self.left_max_heap.pushpop(v))

    def remove(self, v):
        if v <= self.left_max_heap.top():
            self.left_max_heap.remove(v)
        else:
            self.right_min_heap.remove(v)

    def apply_remove(self):
        self.left_max_heap.apply_remove()
        self.right_min_heap.apply_remove()

    def __str__(self):
        return f"min => {self.left_max_heap}  max => {self.right_min_heap}"
