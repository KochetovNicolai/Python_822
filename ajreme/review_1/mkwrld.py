import pandas
import numpy
from heightmap import HeightMap


def StdBiomeTable():
    return [[(233, 221, 199), (196, 212, 170), (169, 204, 164), \
             (169, 204, 164), (156, 187, 169), (156, 187, 169)], \
            [(228, 232, 202), (196, 212, 170), (196, 212, 170), \
             (180, 201, 169), (180, 201, 169), (164, 196, 168)], \
            [(228, 232, 202), (228, 232, 202), (196, 204, 187), \
             (196, 204, 187), (204, 212, 187), (204, 212, 187)], \
            [(153, 153, 153), (187, 187, 187), (221, 221, 187), \
             (255, 255, 255), (255, 255, 255), (255, 255, 255)]]


def LoadBiomeTable(biomeTableName=None):
    if biomeTableName is None:
        return StdBiomeTable()
    else:
        biomeTable = numpy.array(pandas.read_csv('biome-table.csv'))
        for i in range(biomeTable.shape[0]):
            for j in range(biomeTable.shape[1]):
                biomeTable[i][j] = tuple(map(int, biomeTable[i][j].split()))
        return biomeTable


def MakeWorldRGB(N, M, seed=None, physRoughtness=4.0, humidRoughtness=4.0, \
                 seaLevel=0.45, biomeTableName=None):
    K = 0
    while 2**K+1 < N or 2**K+1 < M:
        K += 1

    physMap = HeightMap(K)
    physMap.Generate(seed, physRoughtness)
    physMap = physMap.Map()

    humidMap = HeightMap(K)
    humidMap.Generate(None if seed is None else seed+1, humidRoughtness)
    humidMap = humidMap.Map()

    biomeTable = LoadBiomeTable(biomeTableName)

    RGBMap = [[None]*(2**K+1) for i in range(2**K+1)]
    for i in range(N):
        for j in range(M):
            if physMap[i][j] < seaLevel:
                RGBMap[i][j] = (70, 130, 180)
            else:
                physLevel = int((physMap[i][j]-seaLevel) / (1-seaLevel) * \
                                (len(biomeTable)-1))
                humidLevel = int(humidMap[i][j]*(len(biomeTable[0])-1))
                RGBMap[i][j] = biomeTable[physLevel][humidLevel]

    for i in range(len(RGBMap)):
        RGBMap[i] = RGBMap[i][:M]

    return RGBMap[:N]
