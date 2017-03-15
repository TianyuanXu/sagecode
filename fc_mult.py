import itertools
from collections import defaultdict

""" Tuple Operations """

def convert_to_word(l):
    return int(''.join(map(str,l)))

def remove_first(t,y):
    """ Remove the first occurrence of t from a tuple y.
    
    EXAMPLE:
        sage: remove_first(3,(1,2,3,4,3,2)) 
        sage: (1,2,4,3,2)
    """

    a = y.index(t)
    return y[:a]+y[a+1:]

def neighbors_before(s,y):
    """ Find the indices neighbors of s before its first appearance in y. Stop
    if two neighbors are found.

    Note: If the resulting list is empty, sy < y. If two neighbors are found,
    sy is still fully-commutative. 
 
    EXAMPLE:
        sage: neighbors_before(3,(2,1,4,2,3))
        sage: [0,2] 
    """

    i = 0
    l = []
    while len(l)<2 and i<y.index(s):
            if y[i] == s+1 or y[i] == s-1:
                l = l+[i]
            else:
                l = l
            i = i+1
    return l

def first_12(y):
    """ Find the index of the first occurence of 1 or 2 in y. Return -1 if
    there's no 1 or 2 in y.
    
    EXAMPLE:
        sage: first_12((1,3,4,2))
        sage: 0

        sage: first_12((3,2,4,1))
        sage: 1

        sage: first_12((3,4))
        sage: -1 
    """
    i = 0
    index = -1
    while i < len(y):
        if y[i] > 2:
            i = i + 1
        else: 
            index = i
            break
    return index

def first_neighbor(s,y):
    """ Find the index of the leftmost neighbor of s in y. 

    Note: We will only call this function when we know there is such a
    neighbor.

    EXAMPLE:
        sage: first_neighbor(2,(5,3,1,4))
        sage: 1

        sage: first_neighbor(2,(5,4,1,2))
        sage: 2
    """
    i = 0
    while i < len(y):
        if y[i] == s-1 or y[i] == s+1:
            return i
        else: 
            i = i+1

def before_12(y):
    """
    Return the part of y before the first appearance of 1 or 2.

    EXAMPLE: 
        sage: before_12((3,4,5))
        sage: (3,4,5)

        sage: before_12((3,4,1,2,5))
        sage: (3,4)

        sage: before_12((3,4,2,5))
        sage: (3,4)
    """

    if first_12(y) == -1:
        return y
    else:
        return y[:first_12(y)]

def after_12(y):
    """
    Return the part of y starting from the first 1 or 2. 

    EXAMPLE: 
        sage: after_12((3,4,5))
        sage: ()

        sage: after_12((3,4,1,2,5))
        sage: (1,2,5)

        sage: after_12((3,4,2,5))
        sage: (2,5)
    """
    if first_12(y) == -1:
        return tuple()
    else: 
        return y[first_12(y):]

def my_index(s,y):
    """ 
    Return the index of s in y if s is in y; otherwise return -1. 
    
    EXAMPLE:
        sage: my_index(1,(2,1,3))
        sage: 1

        sage: my_index(1,(2,3,4))
        sage: -1
    """
    try: 
        return y.index(s)
    except ValueError:
        return -1

def onetwo_on_left(y):
    """ 
    Return the coset decomposition y_1 * y_2 of y, where y_1 is in the
    parabolic subgroup generated by 1 and 2 and neither 1 or 2 reduces y_2.  
    
    EXAMPLE:
        sage: onetwo_on_left((1,2,3)) 
        sage: ((1,2), (3,))
        
        sage: onetwo_on_left((1,2,3,1))
        sage: ((1,2,1,),(3,))

        sage: onetwo_on_left((1,2,3,2,1))
        sage: ((1,2,1),(3,1))
    """

    parabolic = tuple()
    minimal = y

    if first_12(y) > -1:
        s = y[first_12(y)]
        i = 1
        while i < 5 and my_index(s,minimal) > -1 and neighbors_before(s, minimal) == []:
            s = minimal[first_12(minimal)]
            parabolic = parabolic + (s,)
            minimal = remove_first(s,minimal)    
            i = i + 1
            s = 3 - s
    return parabolic, minimal 

def my_append(l,x):
    """
    Append x to l if x is not the empty tuple; return l as is otherwise.

    EXAMPLE:
        sage: my_append(((1,2)),(3,))
        sage: ((1,2),(3,))

        sage: my_append((1,2),())
        sage: ((1,2))
    """
    if x == tuple():
        return l
    else: 
        return l + [x]

def left_justify(y):
    """ 
    Return the segments of the left justified word of y.

    EXAMPLE:
        sage: left_justify((1,2,3,1,4,2,1,5))
        sage: [(1,2,1),(3,4),(2,1),(5,)]

        sage: left_justify((3,2,1,3,2,5,1))
        sage: [(3),(2,1),(3,),(2,1),(5,)]
    """


    l = []
    remain = y
    while remain != tuple():
        x = onetwo_on_left(remain)[0]
        y = onetwo_on_left(remain)[1]
        ll = my_append(l,x)
        l = my_append(ll,before_12(y))
        remain = after_12(y) 
    return l

def right_justify(y):
    """ 
    Return the segments of the right justified word of y.
    
    EXAMPLE:
        sage: right_justify((1,2,3,1,4,2,1,5))
        sage: [(1,2),(3,4,5),(1,2,1)]
    
    """
    z = y[::-1]
    l = left_justify(z)
    ll = [i[::-1] for i in l]
    return ll[::-1]

# variables for the six types of 12-chuncks in a right justified word. They
# represent, in order: c1c2-1, c1c2c1-c1, c2c1c2-c2, c1c2c1c2-2c1c2,
# c2c1c2-2c2, c2c1c2c1-2c2c1
var('A')
var('B')
var('C')
var('D')
var('E')
var('F')


def canonical_factors(y):
    """
    Return the factors of Green's f-basis vector for y.
    
    EXAMPLE:
        sage: canonical_factors((1,2,3,1,4,2,1,5))
        sage: [A,3,4,5,B]

        sage: canonical_factors((3,1,2,3,1,4,5,2))
        sage: [3,A,3,4,5,1,2]

    """
    l = right_justify(y)
    factors = []
    for i in range(len(l)):
        seg = l[i]
        if seg[0] == 1 or seg[0] == 2:
            if seg == (1,) or seg == (2,) or seg == (2,1):
                factors = factors + [i for i in seg]
            elif seg == (1,2):
                if i < len(l) - 2 and l[i+2][0] == 1:
                    factors = factors + [A]
                else:
                    factors = factors + [1,2]
            elif seg == (1,2,1):
                factors = factors + [B]
            elif seg == (2,1,2):
                if i < len(l) - 3 and l[i+2][0] == 1:
                    factors = factors + [E]
                else:
                    factors = factors + [C]
            elif seg == (1,2,1,2):
                factors = factors + [D]
            elif seg == (2,1,2,1):
                factors = factors + [F]
        else:
            factors = factors + [j for j in seg]
    return factors


var('v')

def s_once(s,y):
    """ 
    Return the result of the first step in computing c_s * c_w.

    INPUTS:
    -- 's': any factor in Green's f-basis, so s\in S or s = A, B, C, D, E, F.
    -- 'w': the reduced word of an f.c. element

    OUTPUT:
    -- a pair (left, d), where left is a list of things to be multiplied on the
    left to the linear combination in d.

    EXAMPLES:
        sage: factor_times_w(1,(2,3))
        sage: ([], {(1,2,3):1})

        sage: factor_times_w(1,(5,4,1,2))
        sage: ([], {(5,4,1,2): v+1/v}

        sage: factor_times_w(3,(5,2,4,1,3,2))
        sage: ([], {(3,5,2,4,1,3,2): 1})

        sage: factor_times_w(6,(4,1,2,1,7,3,6))
        sage: ([4,A], {(3,6,1): 1})
    """
    d = defaultdict(int)
    left = tuple()
    if my_index(s,y) == -1:             # if s does not appear in y
        d[(s,)+y] += 1 
    elif neighbors_before(s,y) == []:   # this is equivalent to sy<y 
        d[y] += (v + v**(-1))     
    elif len(neighbors_before(s,y)) == 2: # so sy is f.c.
        d[(s,)+y] += 1
    elif s > 3 or (s == 3 and y[first_neighbor(3,y)] == 4):
        factors = canonical_factors(y)
        neighbor = first_neighbor(s,factors)
        left = tuple(factors[:neighbor])
        d[factor_to_tuple(factors[neighbor+1:])] += 1 
    else:           # s appears in y, has only 1 neighbor before it, and sy>y
        if s == 1: 
            first2 = y.index(2)      # locate the first 2 in y
            left = y[:first2]
            z = y[first2:]
            parabolic = onetwo_on_left(z)[0] # the 12-star move
            if parabolic == (2,):
                d[(1,)+z] += 1 
            elif parabolic == (2,1,2,1):
                d[z[1:]] += 1 
            else:
                d[(1,)+z] += 1 
                d[z[1:]] += 1 
        elif s == 2 and y[first_neighbor(2,y)] == 1:
            first1 = y.index(1) 
            left = y[:first1]
            z = y[first1:]
            parabolic = onetwo_on_left(z)[0] # the 21-star move
            if parabolic == (1,):
                d[(2,)+z] += 1 
            elif parabolic == (1,2,1,2):
                d[z[1:]] += 1 
            else:
                d[(2,)+z] += 1 
                d[z[1:]] += 1 
        elif s == 2 and y[first_neighbor(2,y)] == 3: # the 23-star move
            first3 = y.index(3) 
            left = y[:first3]
            d[y[first3+1:]] += 1
        elif s == 3 and y[first_neighbor(3,y)] == 2:
            parabolic = onetwo_on_left(y)[0] 
            if parabolic == (1,2,1):   # the most subtle case
                pass             # since c_s * c_y = 0
            else:
                first2 = y.index(2)
                left = y[:first2]
                d[y[first2+1:]] += 1 
    dd = factor_to_poly(left)
    e = defaultdict(int)
    for k in dd:
        for j in d:
            e[(k,j)] += dd[k] * d[j] 
    return e

def s_times_w(s,w):
    todo = defaultdict(int)
    todo[((s,),w)] = 1
    done = defaultdict(int)
    while todo != {}:
        for pair in list(todo):
            if pair[0] == tuple():
                done[pair[1]] += todo[pair]
                del todo[pair]
            else:
                monomial = pair[0]
                w = pair[1]
                c = todo[pair]
                del todo[pair]
                s = monomial[-1]
                d = s_once(s,w)
                for k in d:
                    todo[(monomial[:-1]+k[0],k[1])] += d[k] * c
    return clean_up(done)

def clean_up(d):
    dd = defaultdict(int)
    for k in d:
        if d[k] != 0:
            dd[tuple(flatten(left_justify(k)))] += d[k]
    return dd


def factor_to_tuple(l):
    t = tuple()
    for x in l:
        if x == A:
            t = t + (1,2)
        elif x == B:
            t = t + (1,2,1)
        elif x == C:
            t = t + (2,1,2)
        elif x == D:
            t = t + (1,2,1,2)
        elif x == E:
            t = t + (2,1,2)
        elif x == F:
            t = t + (2,1,2,1)
        else: 
            t = t + (x,)
    return t

def factor_to_poly(l):
    d = defaultdict(int)
    d[tuple()] = 1
    for i in l:
        if i == A:
            for w in list(d):
                d[w+(1,2)] += d[w]
                d[w] = -d[w]
        elif i == B:
            for w in list(d):
                d[w+(1,2,1)] += d[w]
                d[w+(1,)] += -d[w]
                del d[w]
        elif i == C:
            for w in list(d):
                d[w+(2,1,2)] += d[w]
                d[w+(2,)] += -d[w]
                del d[w]
        elif i == D:
            for w in list(d):
                d[w+(1,2,1,2)] += d[w]
                d[w+(1,2)] += -2*d[w]
                del d[w]
        elif i == E:
            for w in list(d):
                d[w+(2,1,2)] += d[w]
                d[w+(2,)] += -2*d[w]
                del d[w]
        elif i == F:
            for w in list(d):
                d[w+(2,1,2,1)] += d[w]
                d[w+(2,1)] += -2*d[w]
                del d[w]
        else:
            for w in list(d):
                d[w+(i,)] += d[w]
                del d[w]
    return d

def descendents_of(w,n):
    new_vertices = [w]
    current_vertices = [w]
    edges = defaultdict(list)
    while new_vertices != []:
        for w in new_vertices:
            for s in range(1,n+1):
                d = s_times_w(s,w)
                for y in d:
                    y_word = convert_to_word(y)
                    if y != w and (y_word not in edges[convert_to_word(w)]):
                        edges[convert_to_word(w)] += [convert_to_word(y)]
                        if y not in current_vertices:
                            new_vertices = new_vertices + [y]
                            current_vertices = current_vertices + [y]
            new_vertices.remove(w)  
    return edges

def descendent_graph(w,n):
    return DiGraph(descendents_of(w,n))
