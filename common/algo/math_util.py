import math
import itertools
from functools import lru_cache
from collections import defaultdict, deque, Counter


def pi_float(v):
    if isinstance(v, int):
        return v/180*math.pi
    return v


def calc_angle(y, x, y1, x1):
    '''
    0->2*pi
    '''
    a = math.atan2(y1-y, x1-x)
    if a < 0:
        return 2*math.pi+a
    return a


def sin(v):
    return math.sin(pi_float(v))


def cos(v):
    return math.cos(pi_float(v))


def prime_gcds(max_value):
    ret = defaultdict(lambda: set())
    for i in range(2, max_value):
        if len(ret[i]):
            continue
        j = i
        while j < max_value:
            ret[j].add(i)
            j += i
        i += 1
    return ret


def decomposition_prime_factors(v):
    ret = dict()
    i = 2
    while i*i <= v:
        while v % i == 0:
            if i not in ret:
                ret[i] = 0
            ret[i] += 1
            v = v//i
        i += 1
    if v > 1:
        ret[v] = 1
    return ret


def prime_flags(max_v):
    ret = [None]*max_v
    for i in range(2, max_v):
        if ret[i] == False:
            continue
        ret[i] = True
        for j in range(i+i, max_v, i):
            ret[j] = False
    return ret


@lru_cache(None)
def factorial(n):
    if n <= 2:
        return n
    return n*factorial(n-1)


@lru_cache(None)
def com_c(a, b):
    if a == 0 or b == 0:
        return 1
    return factorial(a+b)//factorial(b)//factorial(a)
