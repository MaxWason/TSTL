def bsort(l):
    if len(l) < 10:
        return sorted(l)

    lc = list(l)

    for i in xrange(0,len(l)):
        for j in xrange(1,len(l)):
            if lc[i] > l[j]:
                t = lc[i]
                lc[i] = lc[j]
                lc[j] = lc[i]
    return lc
