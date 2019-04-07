import pandas as pd
import numpy as np
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

    table = \
        [[(233, 221, 199), (196, 212, 170), (169, 204, 164),
          (169, 204, 164), (156, 187, 169), (156, 187, 169)],
         [(228, 232, 202), (196, 212, 170), (196, 212, 170),
          (180, 201, 169), (180, 201, 169), (164, 196, 168)],
         [(228, 232, 202), (228, 232, 202), (196, 204, 187),
          (196, 204, 187), (204, 212, 187), (204, 212, 187)],
         [(153, 153, 153), (187, 187, 187), (221, 221, 187),
          (255, 255, 255), (255, 255, 255), (255, 255, 255)]]
    water_color = (70, 130, 180)

    return np.array(table), np.array(water_color)


def LoadBiomeTable(biome_table_name=None):
    '''
    Read and return Biome table from .csv
    biomeTableName - name of .csv (example: ex.csv)
    Rows - height level
    Columns - humid level
    Second arg - water color
    '''

    if biome_table_name is None:
        return StdBiomeTable()

    biome_table = np.array(pd.read_csv(biome_table_name, header=None))
    return np.array([[[*map(int, j.split())] for j in i] for i in biome_table[:-1]]), \
        np.array([*map(int, biome_table[-1][0].split())])


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
    biome_table, water_color = LoadBiomeTable(biome_table_name)

    phys_map = HeightMap(map_power, seed)[:N, :M]
    humid_map = HeightMap(map_power, None if seed is None else seed+1)[:N, :M]

    phys_ind = ((phys_map-sea_level) / (1-sea_level) *
                biome_table.shape[0]).astype(int) - \
        (phys_map == 1.0)

    humid_ind = (humid_map * biome_table.shape[1]).astype(int) - \
        (humid_map == 1.0)

    RGB_map = biome_table[phys_ind, humid_ind]
    RGB_map[phys_map < sea_level] = water_color

    return RGB_map


def CreateWorld(N, M, seed=None, sea_level=0.45,
                biome_table_name=None, file_name=None):
    '''
    Create world with PIL.
    N - width.
    M - length.
    sea_level - level of sea.
    biome_table_name - name of .csv with colors
    '''

    pixels = CreateWorldRGB(N, M, seed, sea_level, biome_table_name)
    image = Image.fromarray(pixels.astype('uint8'), 'RGB')
    if file_name is None:
        image.show()
    else:
        image.save(file_name)
