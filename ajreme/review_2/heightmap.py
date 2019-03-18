import random
import numpy


def HeightMap(map_power, random_state=None):
    '''
    Generate and save world of size 2**map_power.
    Diamond square algorithm used.
    randomstate - seed. None means random seed.
    roughtness - shows the world UNflatness.
    Returns size, map - size of heightmap and
    heightmap.
    '''

    size = 2**map_power+1
    map_arr = numpy.array([numpy.array([None]*(size)) for i in range(size)])

    if random_state is not None:
        random.seed(random_state)

    map_arr[0][0] = random.uniform(-1.0, 1.0)
    map_arr[0][size-1] = random.uniform(-1.0, 1.0)
    map_arr[size-1][0] = random.uniform(-1.0, 1.0)
    map_arr[size-1][size-1] = random.uniform(-1.0, 1.0)

    def Get(edge_len, xList, yList):
        '''
        Private function.
        xList and yList has a size of 4.
        Returns average height + random noise,
        that depends in roughness and size of
        current subsquare edge len.
        '''

        total, count = 0, 0
        for i in range(4):
            if 0 <= xList[i] < size and \
               0 <= yList[i] < size:
                total, count = total+(map_arr[xList[i]][yList[i]]), count+1
        return total/count + random.uniform(-float(edge_len)/size,
                                            float(edge_len)/size)

    def Normilize():
        '''
        Private function.
        Normilize heightmap.
        '''

        minVal = min(map(min, map_arr))
        maxVal = max(map(max, map_arr))
        return numpy.vectorize(lambda x: (x-minVal) / (maxVal-minVal))(map_arr)

    for s_map_power in range(map_power, 0, -1):
        '''
        Generating map. For every depth:
        1) Diamond step
        2) Square step 1
        3) Square step 2
        '''

        edge_len, s_edge_len = 2**s_map_power, 2**(s_map_power-1)

        for i in range(2**(map_power-s_map_power)):
            for j in range(2**(map_power-s_map_power)):
                map_arr[i*edge_len+s_edge_len][j*edge_len+s_edge_len] = \
                    Get(edge_len,
                        (i*edge_len, i*edge_len,
                         i*edge_len+edge_len, i*edge_len+edge_len),
                        (j*edge_len, j*edge_len+edge_len,
                         j*edge_len+edge_len, j*edge_len))

        for i in range(2**(map_power-s_map_power)+1):
            for j in range(2**(map_power-s_map_power)):
                map_arr[i*edge_len][j*edge_len+s_edge_len] = \
                    Get(edge_len,
                        (i*edge_len, i*edge_len-s_edge_len,
                         i*edge_len, i*edge_len+s_edge_len),
                        (j*edge_len, j*edge_len+s_edge_len,
                         j*edge_len+edge_len, j*edge_len+s_edge_len))

        for i in range(2**(map_power-s_map_power)):
            for j in range(2**(map_power-s_map_power)+1):
                map_arr[i*edge_len+s_edge_len][j*edge_len] = \
                    Get(edge_len,
                        (i*edge_len+s_edge_len, i*edge_len,
                         i*edge_len+s_edge_len, i*edge_len+edge_len),
                        (j*edge_len-s_edge_len, j*edge_len,
                         j*edge_len+s_edge_len, j*edge_len))

    return Normilize()
