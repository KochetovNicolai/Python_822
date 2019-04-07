import random
import numpy


def HeightMap(map_power, random_state=None):
    '''
    Generate and save world of size 2**map_power.
    Diamond square algorithm used.
    randomstate - seed. None means random seed.
    '''

    size = 2**map_power+1
    map_arr = numpy.empty([size, size])

    if random_state is not None:
        random.seed(random_state)

    map_arr[0][0] = random.uniform(-1.0, 1.0)
    map_arr[0][size-1] = random.uniform(-1.0, 1.0)
    map_arr[size-1][0] = random.uniform(-1.0, 1.0)
    map_arr[size-1][size-1] = random.uniform(-1.0, 1.0)

    def Get(edge_len, xList, yList):
        # Returns average height + random noise,
        # that depends in roughness and size of
        # current subsquare edge length.

        total, count = 0, 0
        for i in range(4):
            if 0 <= xList[i] < size and \
               0 <= yList[i] < size:
                total, count = total+(map_arr[xList[i]][yList[i]]), count+1
        return total/count + random.uniform(-float(edge_len)/size,
                                            float(edge_len)/size)

    def Normilize():
        # Normilize heightmap.

        minVal = numpy.amin(map_arr)
        maxVal = numpy.amax(map_arr)
        return (map_arr-minVal) / (maxVal-minVal)

    for s_map_power in range(map_power, 0, -1):
        '''
        Generating map. s_map_power - len of smaller current square.
        X - ready values
        1 - current step values
        0 - not considered values
        Example of second step:
        1)  Diamond step
            X 0 X 0 X
            0 1 0 1 0
            X 0 X 0 X
            0 1 0 1 0
            X 0 X 0 X
        2)  Square step 1
            X 0 X 0 X
            1 X 1 X 1
            X 0 X 0 X
            1 X 1 X 1
            X 0 X 0 X
        3)  Square step 2
            X 1 X 1 X
            X X X X X
            X 1 X 1 X
            X X X X X
            X 1 X 1 X
        4)  Finally
            X X X X X
            X X X X X
            X X X X X
            X X X X X
            X X X X X
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
