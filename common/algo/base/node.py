from typing import List, Dict


def load_from_edges(cls: "Node", edges):

    nodes: Dict[str, Node] = dict()
    for f, t, *args in edges:
        if f not in nodes:
            nodes[f] = cls(f)
        if t not in nodes:
            nodes[t] = cls(t)
        if len(args) == 0:
            ft = tf = 1
        elif len(args) == 1:
            ft = tf = args[0]
        else:
            ft = tf = args
        if ft is not None:
            nodes[f].out_edges[t] = Edge(nodes[f], nodes[t]).load(ft)
        if tf is not None:
            nodes[t].out_edges[f] = Edge(nodes[t], nodes[f]).load(tf)
    return nodes


class Node:

    def __init__(self, key):
        self.key = key
        self.depth = 0
        self.in_edges: Dict[str, Edge] = {}
        self.out_edges: Dict[str, Edge] = {}

    def __repr__(self):
        return f"(key:{self.key})"


class Edge:
    def __init__(self, src, dst):
        self.src: Node = src
        self.dst: Node = dst

    def load(self, value):
        self.value = value
        return self


class TreeNode:
    r"""
               A                #
          /    |  \             #
       B       C     D          #
     / | \    / \   / \         #
    E  F  G  H   I  J  K        #
    """

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left: TreeNode = left
        self.right: TreeNode = right

    def dfs(self, call):
        def util(n: TreeNode, depth=0):
            if n is None:
                return
            util(n.left, depth + 1)
            call(n, depth)
            util(n.right, depth + 1)

        util(self)

    @staticmethod
    def make(array):
        ans = [None] + [TreeNode(v) if v is not None else v for v in array]
        for i in range(1, len(ans)):
            if ans[i] is None:
                continue
            if i * 2 < len(ans):
                ans[i].left = ans[i * 2]
            if i * 2 + 1 < len(ans):
                ans[i].right = ans[i * 2 + 1]
        return ans[1]

    def __repr__(self):
        ans = ["", "---TreeNode--begin--"]

        def util(n: TreeNode, depth):
            ans.append(f"{' '*depth*2}{n.val}: ")

        self.dfs(util)
        return "\n".join(ans + ["---TreeNode--end--", ""])
