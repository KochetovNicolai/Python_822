import pandas
import numpy
from PIL import Image
from heightmap import HeightMap


def StdBiomeTable():
    '''
    Returns build-in Biome Table
    https://hsto.org/storage/694bf417/2bd7e8fe/47ea1f86/057bf768.png
    Rows - height level
    Columns - humid level
    Second arg - water color
    '''

    return [[(233, 221, 199), (196, 212, 170), (169, 204, 164),
             (169, 204, 164), (156, 187, 169), (156, 187, 169)],
            [(228, 232, 202), (196, 212, 170), (196, 212, 170),
             (180, 201, 169), (180, 201, 169), (164, 196, 168)],
            [(228, 232, 202), (228, 232, 202), (196, 204, 187),
             (196, 204, 187), (204, 212, 187), (204, 212, 187)],
            [(153, 153, 153), (187, 187, 187), (221, 221, 187),
             (255, 255, 255), (255, 255, 255), (255, 255, 255)]], \
        (70, 130, 180)


def LoadBiomeTable(biome_table_name=None):
    '''
    Read and return Biome table from .csv
    biomeTableName - name of .csv (example: ex.csv)
    Rows - height level
    Columns - humid level
    Second arg - water colors
    '''

    if biome_table_name is None:
        return StdBiomeTable()

    biome_table = numpy.array(pandas.read_csv(biome_table_name))
    return numpy.vectorize(lambda x: tuple(map(int, x.split())))(biome_table)


def TwoPower(N):
    K = 0
    while 2**K+1 < N:
        K += 1
    return K


def CreateWorldRGB(N, M, seed=None, sea_level=0.45, biome_table_name=None):
    '''
    Create two heightmaps and return RGB 2D-matrix.
    seed - world seed. None if random.
    sea_level - limit of water.
    biome_table_name - name of .csv file with colors
    '''

    map_power = max(TwoPower(N), TwoPower(M))

    phys_map = HeightMap(map_power, seed)
    humid_map = HeightMap(map_power, None if seed is None else seed+1)
    biome_table, water_color = LoadBiomeTable(biome_table_name)

    RGB_map = [[None]*M for i in range(N)]
    for i in range(N):
        for j in range(M):
            if phys_map[i][j] < sea_level or sea_level == 1.0:
                RGB_map[i][j] = water_color
            else:
                phys_level = int((phys_map[i][j]-sea_level) / (1-sea_level) *
                                 (len(biome_table)-1))
                humid_level = int(humid_map[i][j]*len(biome_table[0]))
                humid_level -= humid_level == len(biome_table[0])
                RGB_map[i][j] = biome_table[phys_level][humid_level]

    return RGB_map


def CreateWorld(N, M, seed=None, sea_level=0.45, biome_table_name=None):
    '''
    Create world with PIL.
    N - width.
    M - length.
    sea_level - level of sea.
    biome_table_name - name of .csv with colors
    '''

    image = CreateWorldRGB(N, M, seed, sea_level, biome_table_name)

    N, M = len(image), len(image[0])
    img = Image.new('RGB', (N, M))
    pixels = img.load()

    for i in range(N):
        for j in range(M):
            pixels[i, j] = image[i][j]

    img.show()
