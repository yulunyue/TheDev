
def kmp_next(l, s, pi, v):
    while l and s[l] != v:
        l = pi[l-1]
    if s[l] == v:
        l += 1
    return l


def kmp_array(s):
    '''
    ret[i]= max(j->[1,n] => s[:j]==s[-j:]))
    '''
    n = len(s)
    pi = [0]*n
    l = 0
    for r in range(1, n):
        l = kmp_next(l, s, pi, s[r])
        pi[r] = l
    return pi


def kmp_search(src, target):
    pi = kmp_array(target)
    m = len(target)
    mathch_idx = []
    c = 0
    for i, v in enumerate(src):
        c = kmp_next(c, target, pi, v)
        if c == len(target):
            mathch_idx.append(i-m+1)
            c = pi[c-1]
    return mathch_idx


def z_kmp(s):
    '''
    max(i,s[i:i+z[i]]==s[:z[i]])
    '''
    n = len(s)
    z = [0]*n
    l = r = 0
    for i in range(1, n):
        z[i] = max(min(z[i-l], r-i+1), 0)
        while i+z[i] < n and s[z[i]] == s[z[i]+i]:
            l, r = i, i+z[i]
            z[i] += 1
    return z


def manacher_get_odd_p(s):
    n = len(s)
    ret = [0]*n
    l, r = 0, -1
    for i in range(n):
        if i > r:
            k = 1
        else:
            k = min(ret[l+r-i], r-i+1)
        while k <= i and i+k < n and s[i-k] == s[i+k]:
            k += 1
        ret[i] = k
        k -= 1
        if i+k > r:
            l = i-k
            r = i+k
    return ret
