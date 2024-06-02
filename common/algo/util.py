import math
import itertools

def combinations(array,n):
    return itertools.combinations(array,n)

def permutations(array,n):
    return itertools.permutations(array,n)

def pi_float(v):
    if isinstance(v,int):
        return v/180*math.pi
    return v


def calc_angle(y,x,y1,x1):
    '''
    0->2*pi
    '''
    a = math.atan2(y1-y,x1-x)
    if a<0:
        return 2*math.pi+a
    return a

def sin(v):
    return math.sin(pi_float(v))

def cos(v):
    return math.cos(pi_float(v))