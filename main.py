from Func import genTree, findRoute, swapPoke, combinePoke, processPoke, genImg


def main():
    transDict = {0: "HP  ", 1: "DEF ", 2: "SATK", 3: "SDEF", 4: "SPD "}
    maleSet = [0, 3, 1, 4, 0]
    femaleSet = [2, 1, 1, 2, 2]

    sdic = {}
    ldic = {}
    tree = {}
    genTree(sdic, ldic, tree)
    rt = findRoute(sdic, ldic, tree, maleSet, femaleSet)
    # print("out")
    poke = rt[0]
    pokeSex = rt[1]
    aimRoute = rt[2]
    swapPoke(poke, pokeSex, aimRoute)

    pokeSexAll = []
    for i in range(0, 8):
        pokeSexAll = pokeSexAll + [pokeSex[i][0]]
        pokeSexAll = pokeSexAll + [pokeSex[i][1]]
    # print(pokeSexAll)
    pokeSex0 = pokeSex
    # print(pokeSex0)
    pokeSex1 = [combinePoke(pokeSex0[0], pokeSex0[1]), combinePoke(pokeSex0[2], pokeSex0[3]),
                combinePoke(pokeSex0[4], pokeSex0[5]), combinePoke(pokeSex0[6], pokeSex0[7])]
    # print(pokeSex1)
    pokeSex2 = [combinePoke(pokeSex1[0], pokeSex1[1]), combinePoke(pokeSex1[2], pokeSex1[3])]
    # print(pokeSex2)
    pokeSex3 = combinePoke(pokeSex2[0], pokeSex2[1])
    # print(pokeSex3)

    processPoke(transDict, pokeSexAll, pokeSex0, pokeSex1, pokeSex2, pokeSex3)
    genImg(pokeSexAll, pokeSex0, pokeSex1, pokeSex2, pokeSex3)


if __name__ == '__main__':
    main()
    print("---End Program---")
