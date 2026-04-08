from typing import List
from common.util.export import logger


def kmp_next(l, s, pi, v):
    while l and s[l] != v:
        l = pi[l - 1]
    if s[l] == v:
        l += 1
    return l


def kmp_array(s):
    """
    ret[i]=max(j)
    s[:j+1]==s[i-j:i+1]))

    a,b,a,b,c,a,b,a
    0,0,1,2,0,1,2,3
    """
    n = len(s)
    pi = [0] * n
    l = 0
    for r in range(1, n):
        l = kmp_next(l, s, pi, s[r])
        pi[r] = l
    return pi


def kmp_search(src, target):
    if not target:
        return range(0, len(src))
    pi = kmp_array(target)
    match_idx = []
    m = len(target)
    c = 0
    for i, v in enumerate(src):
        c = kmp_next(c, target, pi, v)
        if c == len(target):
            match_idx.append(i - m + 1)
            c = pi[c - 1]
    return match_idx


def z_kmp(s):
    """
    z[i]=max(j)
    s[:j+1]==s[i:i+j+1]))
    """
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(z[i - l], r - i)
        while i + z[i] < n and s[z[i]] == s[z[i] + i]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def manacher_get_odd_p(s):
    """
    ret[i]=max(k)
    all(s[i-k]==s[i+k])
    u = 'aabcbc'
    s = '#a#a#b#c#b#c#'
    ret= 0121010303010
    """

    n = len(s)
    result = [0] * (n * 2 + 1)
    max_l, max_r = 0, -1
    for i in range(n * 2 + 1):
        r = (i - 1) // 2
        l = i - 1 - r
        if r < max_r:
            L = min(r + 1 - l + (max_r - r) * 2, result[(max_l + max_r + 1) * 2 - i])
            r = (i + L - 2) // 2
            l = i - 1 - r
        while l - 1 >= 0 and r + 1 < n and s[l - 1] == s[r + 1]:
            l -= 1
            r += 1
        result[i] = r + 1 - l
        if r > max_r:
            max_l = l
            max_r = r
    return result


def sa_pre1(s):
    n = len(s)

    t = [False] * n
    for i in range(len(s) - 2, -1, -1):
        if s[i] < s[i + 1]:
            t[i] = True
        elif s[i] > s[i + 1]:
            t[i] = False
        else:
            t[i] = t[i + 1]


def get_sa_prefix_doubling(s: List[int]):
    """
    s = aabcbc#
    id   s   rk0 sa1 rk1 sa2 rk2 sa4 rk4
    0 aabcbc  0   0   0       0   0   0
    1 abcbc   0   1   1       1   1   1
    2 bcbc    1   2   2       3   4   3
    3 cbc     2   4   4       5   2   5
    4 bc      1   5   2       2   5   2
    5 c       2   3   3       4   3   4
    sa[rk[i]]=rk[sa[i]]=i
    """
    if isinstance(s[0], str):
        s = [ord(v) for v in s]
    n = len(s)
    sa = list(range(n))
    rank = s
    k = 1
    while k < n:
        sa = sorted(sa, key=lambda i: [rank[i], rank[i + k] if i + k < n else -1])
        new_rank = [0] * n
        for i in range(1, n):
            pre_rank, cur_rank = [rank[sa[i - 1]]], [rank[sa[i]]]
            if sa[i - 1] + k < n:
                pre_rank.append(rank[sa[i - 1] + k])
            else:
                pre_rank.append(-1)
            if sa[i] + k < n:
                cur_rank.append(rank[sa[i] + k])
            else:
                cur_rank.append(-1)
            new_rank[sa[i]] = new_rank[sa[i - 1]]
            if pre_rank < cur_rank:
                new_rank[sa[i]] += 1
        rank = new_rank
        # logger.info(f"{k},sa:{sa},rk:{rank}")
        k *= 2
    return sa, rank


def get_height_form_sa(s, sa: List[int] = None, rank=None):
    n = len(s)
    if sa is None:
        sa, rank = get_sa_prefix_doubling(s)
    if rank is None:
        rank = [0] * n
        for i in range(n):
            rank[sa[i]] = i  # 构建rank数组
    lcp = [0] * n
    k = 0  # 当前匹配长度
    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue

        j = sa[rank[i] - 1]  # SA中前一个后缀的起始位置
        # 利用性质：H[i] ≥ H[i-1]-1
        if k > 0:
            k -= 1

        # 扩展匹配长度
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1

        lcp[rank[i]] = k

    return lcp, sa, rank
