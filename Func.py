import copy
from random import choices
import numpy as np
import cv2 as cv

tolerance = 2


class pokemon:
    id = 0
    gender = -1  # -1:no gender; 0: male; 1:female
    statSet = [0, 0, 0, 0, 0, 0]

    def __init__(self, id, gender, statSet):
        self.statSet = statSet
        self.gender = gender
        self.id = id


class bredTreeElement:
    bredTreeId = 0
    statSet = [0, 0, 0, 0, 0, 0]
    son = None
    parent = None

    def __init__(self, bredTreeId, statSet, son, parent):
        self.bredTreeId = bredTreeId
        self.statSet = statSet
        self.son = son
        self.parent = parent


def getSon(m, n):  # m:1维
    t1 = copy.deepcopy(m)
    t2 = copy.deepcopy(m)
    c = []
    for i in range(0, len(m)):
        if m[i] == 1:
            c = c + [i]
    for i in range(0, len(c)):
        t1[c[i]] = n[0][i]
        t2[c[i]] = n[1][i]

    return [t1, t2]


def delZero(l):
    p = []
    for i in range(0, len(l)):
        if not l[i] == 0:
            p = p + [l[i]]
    p.sort()
    return p


def isEqual(a, b):
    k = 0
    for i in range(0, len(a)):
        if not a[i] == b[i]:
            k = k + 1
    if not k == 0:
        return False
    if k == 0:
        return True


def selectPoke(A, B):
    p = [0, 0, 0, 0, 0]
    a = 0
    b = 0
    loop = 0
    while True:
        if loop > tolerance:
            print("can not find combine!")
            break
        haveReturnA = False
        haveReturnB = False
        while not haveReturnA:
            m = choices([0, 1, 2, 3, 4], [0.2, 0.2, 0.2, 0.2, 0.2])[0]
            if A[m] > 0:
                haveReturnA = True
                a = m
        while not haveReturnB:
            n = choices([0, 1, 2, 3, 4], [0.2, 0.2, 0.2, 0.2, 0.2])[0]
            if B[n] > 0:
                haveReturnB = True
                b = n
        if not a == b:
            A[a] = A[a] - 1
            B[b] = B[b] - 1
            # print("Male:", a)
            # print("Female:", b)
            break
        loop=loop+1
    p[a] = 1
    p[b] = 1
    return p, [a, b]


def findRoute(sdic, ldic, tree, maleSet, femaleSet):
    loop = 0
    while True:
        if loop > tolerance:
            print("can not find route!")
            break
        mset = copy.deepcopy(maleSet)
        fset = copy.deepcopy(femaleSet)
        p2Set = []
        sxSet = []

        for i in range(0, 8):
            sP = selectPoke(mset, fset)
            p2Set = p2Set + [sP[0]]
            sxSet = sxSet + [sP[1]]
        # print(p2Set)
        # print(sxSet)

        pp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, len(p2Set)):
            for key in sdic:
                if isEqual(p2Set[i], sdic[key]):
                    pp[key] = pp[key] + 1
        # print(pp)

        for key in ldic:
            if isEqual(ldic[key], pp):
                # print(key, ":", ldic[key])
                # print(key, ":", tree[key])
                return p2Set, sxSet, tree[key]
        loop = loop + 1



def genTree(sdic, ldic, tree):
    a1 = [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 1, 0]], [[1, 0, 1], [1, 1, 0]]]  # 3
    a2 = [[[0, 1, 1, 1], [1, 0, 1, 1]], [[0, 1, 1, 1], [1, 1, 0, 1]], [[0, 1, 1, 1], [1, 1, 1, 0]],
          [[1, 0, 1, 1], [1, 1, 0, 1]], [[1, 0, 1, 1], [1, 1, 1, 0]], [[1, 1, 0, 1], [1, 1, 1, 0]]]  # 6
    a3 = [[[0, 1, 1, 1, 1], [1, 0, 1, 1, 1]], [[0, 1, 1, 1, 1], [1, 1, 0, 1, 1]], [[0, 1, 1, 1, 1], [1, 1, 1, 0, 1]],
          [[0, 1, 1, 1, 1], [1, 1, 1, 1, 0]], [[1, 0, 1, 1, 1], [1, 1, 0, 1, 1]], [[1, 0, 1, 1, 1], [1, 1, 1, 0, 1]],
          [[1, 0, 1, 1, 1], [1, 1, 1, 1, 0]], [[1, 1, 0, 1, 1], [1, 1, 1, 0, 1]], [[1, 1, 0, 1, 1], [1, 1, 1, 1, 0]],
          [[1, 1, 1, 0, 1], [1, 1, 1, 1, 0]]]  # 10
    id = 1
    rawTree = {}
    a4 = [0, [1, 2], [1, 2, 3, 4]]
    for i0 in range(0, 10):
        for i1 in range(0, 6):
            for i2 in range(0, 6):
                for i3 in range(0, 3):
                    for i4 in range(0, 3):
                        for i5 in range(0, 3):
                            for i6 in range(0, 3):
                                rawTree[id] = [i0, [i1, i2], [i3, i4, i5, i6]]
                                id = id + 1
    # print(rawTree)
    # tree = {}
    ti = 1
    for key in rawTree:
        b0 = a3[rawTree[key][0]][0]
        p0 = getSon(b0, a2[rawTree[key][1][0]])
        b1 = a3[rawTree[key][0]][1]
        p1 = getSon(b1, a2[rawTree[key][1][1]])
        p2 = p0 + p1
        pa = []
        for i in range(0, 4):
            pa = pa + getSon(p2[i], a1[rawTree[key][2][i]])
        tree[ti] = pa
        ti = ti + 1
    # print(tree)

    blk = [0, 0, 0, 0, 0]
    # sdic = {}
    p = 0
    for i in range(0, 5):
        for j in range(i + 1, 5):
            c = copy.deepcopy(blk)
            c[i] = 1
            c[j] = 1
            sdic[p] = c
            p = p + 1
    # print(sdic)

    # ldic = {}
    l = 1
    for key in tree:
        m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, len(tree[key])):
            for j in range(0, 10):
                if tree[key][i] == sdic[j]:
                    m[j] = m[j] + 1
        ldic[l] = m
        l = l + 1
    # print(ldic)

    rlist = []
    for key in ldic:
        isRepeat = False
        c = delZero(ldic[key])
        for i in range(0, len(rlist)):
            if c == rlist[i]:
                isRepeat = True
        if not isRepeat:
            rlist = rlist + [c]
    # print(rlist)


def swapList(l: list, a, b):
    temp = l[a]
    l[a] = l[b]
    l[b] = temp


def sum(l):
    p = 0
    for i in range(0, len(l)):
        p = p + l[i]
    return p


def swapPoke(poke, pokeSex, aimRoute):
    el = [0, 0, 0, 0, 0, 0, 0, 0]
    sList = []
    while sum(el) < 8:
        for i in range(0, 8):
            if poke[i] == aimRoute[i]:
                el[i] = 1
        # print(el)

        for i in range(0, 8):
            if el[i] == 0:
                for j in range(0, 8):
                    if poke[i] == aimRoute[j] and not el[j] == 1:
                        # print("swap")
                        swapList(poke, i, j)
                        sList = sList + [[i, j]]
    # print(poke)

    for i in range(0, len(sList)):
        swapList(pokeSex, sList[i][0], sList[i][1])


def combinePoke(l1, l2):
    l = l1
    for i in range(0, len(l2)):
        if not hasElement(l2[i], l):
            l = l + [l2[i]]
    l.sort()
    return l


def hasElement(a, B):
    for i in range(0, len(B)):
        if B[i] == a:
            return True
    return False


def iseven(num):
    if (num % 2) == 0:
        return True
    else:
        return False


def genImg(pokeSexAll, pokeSex0, pokeSex1, pokeSex2, pokeSex3):
    dx = 100
    dy = 100
    h = 7 * dy
    w = 18 * dx

    img = np.zeros((h, w), dtype=np.uint8)
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    img[:, :, 0] = 255
    img[:, :, 1] = 255
    img[:, :, 2] = 255

    xpos = dx
    for i in range(0, 16):
        cv.putText(img, str(pokeSexAll[i]), (xpos, 6 * dy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        xpos = xpos + dx

    xpos = round(1.35 * dx)
    for i in range(0, 8):
        cv.putText(img, str(pokeSex0[i]), (xpos, 5 * dy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        xpos = xpos + 2 * dx

    xpos = round(2.05 * dx)
    for i in range(0, 4):
        cv.putText(img, str(pokeSex1[i]), (xpos, 4 * dy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        xpos = xpos + 4 * dx

    xpos = round(3.75 * dx)
    for i in range(0, 2):
        cv.putText(img, str(pokeSex2[i]), (xpos, 3 * dy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        xpos = xpos + 8 * dx

    xpos = round(7.4 * dx)
    cv.putText(img, str(pokeSex3), (xpos, 2 * dy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    xpos1 = round(1.45 * dx)
    xpos2 = round(1.85 * dx)
    ypos1 = round(5.8 * dy)
    ypos2 = round(5.1 * dy)
    for i in range(0, 8):
        cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)
        xpos1 = xpos1 + 2 * dx
        xpos2 = xpos2 + 2 * dx

    xpos1 = round(2.3 * dx)
    xpos2 = round(1.9 * dx)
    ypos1 = round(5.8 * dy)
    ypos2 = round(5.1 * dy)
    for i in range(0, 8):
        cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)
        xpos1 = xpos1 + 2 * dx
        xpos2 = xpos2 + 2 * dx

    xpos1 = round(1.95 * dx)
    xpos2 = round(2.9 * dx)
    ypos1 = round(4.8 * dy)
    ypos2 = round(4.1 * dy)
    for i in range(0, 4):
        cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)
        xpos1 = xpos1 + 4 * dx
        xpos2 = xpos2 + 4 * dx

    xpos1 = round(3.9 * dx)
    xpos2 = round(2.95 * dx)
    ypos1 = round(4.8 * dy)
    ypos2 = round(4.1 * dy)
    for i in range(0, 4):
        cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)
        xpos1 = xpos1 + 4 * dx
        xpos2 = xpos2 + 4 * dx

    xpos1 = round(2.9 * dx)
    xpos2 = round(4.85 * dx)
    ypos1 = round(3.8 * dy)
    ypos2 = round(3.1 * dy)
    for i in range(0, 2):
        cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)
        xpos1 = xpos1 + 8 * dx
        xpos2 = xpos2 + 8 * dx

    xpos1 = round(6.85 * dx)
    xpos2 = round(4.9 * dx)
    ypos1 = round(3.8 * dy)
    ypos2 = round(3.1 * dy)
    for i in range(0, 2):
        cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)
        xpos1 = xpos1 + 8 * dx
        xpos2 = xpos2 + 8 * dx

    xpos1 = round(4.9 * dx)
    xpos2 = round(8.85 * dx)
    ypos1 = round(2.8 * dy)
    ypos2 = round(2.1 * dy)
    cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)

    xpos1 = round(12.85 * dx)
    xpos2 = round(8.9 * dx)
    ypos1 = round(2.8 * dy)
    ypos2 = round(2.1 * dy)
    cv.line(img, (xpos1, ypos1), (xpos2, ypos2), (0, 0, 0), 1, 4)
    cv.imwrite("img.png", img)


def processPoke(transDict, pokeSexAll, pokeSex0, pokeSex1, pokeSex2, pokeSex3):
    for i in range(0, 16):
        if iseven(i):
            pokeSexAll[i] = [transDict[pokeSexAll[i]], "M"]
        else:
            pokeSexAll[i] = [transDict[pokeSexAll[i]], "F"]
    print(pokeSexAll)
    for i in range(0, 8):
        pokeSex0[i][0] = transDict[pokeSex0[i][0]]
        pokeSex0[i][1] = transDict[pokeSex0[i][1]]
    print(pokeSex0)
    for i in range(0, 4):
        pokeSex1[i][0] = transDict[pokeSex1[i][0]]
        pokeSex1[i][1] = transDict[pokeSex1[i][1]]
        pokeSex1[i][2] = transDict[pokeSex1[i][2]]
    print(pokeSex1)
    for i in range(0, 2):
        pokeSex2[i][0] = transDict[pokeSex2[i][0]]
        pokeSex2[i][1] = transDict[pokeSex2[i][1]]
        pokeSex2[i][2] = transDict[pokeSex2[i][2]]
        pokeSex2[i][3] = transDict[pokeSex2[i][3]]
    print(pokeSex2)
    pokeSex3[0] = transDict[pokeSex3[0]]
    pokeSex3[1] = transDict[pokeSex3[1]]
    pokeSex3[2] = transDict[pokeSex3[2]]
    pokeSex3[3] = transDict[pokeSex3[3]]
    pokeSex3[4] = transDict[pokeSex3[4]]
    print(pokeSex3)
