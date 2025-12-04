from common.util.export import List


class Node:
    def __init__(self, cnt, left=None, right=None):
        self.left: Node = left
        self.right: Node = right
        self.cnt = cnt


class PersistentSegmentTree:
    def __init__(self, arr):
        self.sorted_values = sorted(set(arr))
        self.value_to_idx = {v: i for i, v in enumerate(self.sorted_values)}
        self.n = len(self.sorted_values)
        self.roots: List[Node] = [None] * (len(arr) + 1)
        self.roots[0] = self.build(0, self.n - 1)
        for i, val in enumerate(arr, 1):
            idx = self.value_to_idx[val]
            self.roots[i] = self.insert(self.roots[i - 1], 0, self.n - 1, idx)

    def build(self, l, r):
        if l == r:
            return Node(0)
        mid = (l + r) // 2
        left = self.build(l, mid)
        right = self.build(mid + 1, r)
        return Node(left.cnt + right.cnt, left=left, right=right)

    def insert(self, prev_node: Node, l, r, idx):
        if l == r:
            return Node(prev_node.cnt + 1)
        mid = (l + r) // 2
        if idx <= mid:
            new_left = self.insert(prev_node.left, l, mid, idx)
            return Node(prev_node.cnt + 1, new_left, prev_node.right)
        new_right = self.insert(prev_node.right, mid + 1, r, idx)
        return Node(prev_node.cnt + 1, prev_node.left, new_right)

    def quert_cnt(self, l: int, r: int):
        return self.roots[r].cnt - self.roots[l - 1].cnt

    def query(self, l, r, k):
        return self.query_kth(self.roots[l - 1], self.roots[r], 0, self.n - 1, k)

    def query_kth(self, node_l: Node, node_r: Node, l, r, k):
        if l == r:
            return self.sorted_values[l]
        mid = (l + r) // 2
        left_cnt = node_r.left.cnt - node_l.left.cnt
        if k <= left_cnt:
            return self.query_kth(node_l.left, node_r.left, l, mid, k)
        return self.query_kth(node_l.right, node_r.right, mid + 1, r, k - left_cnt)
