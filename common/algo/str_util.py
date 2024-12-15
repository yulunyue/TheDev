                   
def kmp_next(l, s, pi, v):
    while l and s[l] != v:
        l = pi[l-1]
    if s[l] == v:
        l += 1
    return l


def kmp_array(s):
    '''
    ret[i]=max(j)
    s[:j+1]==s[i-j:i+1]))
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
    match_idx = []
    m = len(target)
    c = 0
    for i, v in enumerate(src):
        c = kmp_next(c, target, pi, v)
        if c == len(target):
            match_idx.append(i-m+1)
            c = pi[c-1]
    return match_idx


def z_kmp(s):
    '''
    z[i]=max(j) 
    s[:j+1]==s[i:i+j+1]))
    z(aaabaab) = [0, 2, 1, 0, 2, 1, 0]
        aaabaab 
      1 aabaab 2
      2 abaab 1
    z(abacaba) = [0, 0, 1, 0, 3, 0, 1]
        abacaba
      2 acaba 1
      4 aba 
    '''
    n = len(s)
    z = [0]*n
    l = r = 0
    for i in range(1, n):
        if i<r:
            z[i] = min(z[i-l], r-i)
        while i+z[i] < n and s[z[i]] == s[z[i]+i]:
            z[i] += 1
        if i+z[i]>r:
            l, r = i, i+z[i]
    return z


def manacher_get_odd_p(s):
    '''
    ret[i]=max(k) 
    all(s[i-k]==s[i+k])
    '''
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
