import random


class HeightMap(object):

    _K, _N, _map = None, None, None
    _roughness = None

    def __init__(self, K):
        self._K, self._N = K, 2**K
        self._map = [[None]*(2**K+1) for i in range(2**K+1)]

    def Map(self):
        return self._map.copy()

    def Size(self):
        return self._N+1

    def _Get(self, N, xList, yList):
        total, count = 0, 0
        for i in range(4):
            if 0 <= xList[i] <= self._N and 0 <= yList[i] <= self._N:
                total, count = total+(self._map[xList[i]][yList[i]]), count+1
        return total/count + random.uniform(-N*self._roughness/self._N, \
                                             N*self._roughness/self._N)

    def _Normilize(self):
        N, minVal, maxVal = 2**self._K+1, None, None
        for i in range(N):
            for j in range(N):
                minVal = self._map[i][j] if minVal is None \
                    or self._map[i][j] < minVal else minVal
                maxVal = self._map[i][j] if maxVal is None \
                    or self._map[i][j] > maxVal else maxVal
        for i in range(N):
            for j in range(N):
                self._map[i][j] = (self._map[i][j]-minVal) / (maxVal-minVal)

    def Generate(self, randomstate=None, roughness=4.0):
        if randomstate is not None:
            random.seed(randomstate)
        self._roughness = roughness

        self._map[0][0] = random.uniform(-1.0, 1.0)
        self._map[0][2**self._K] = random.uniform(-1.0, 1.0)
        self._map[2**self._K][0] = random.uniform(-1.0, 1.0)
        self._map[2**self._K][2**self._K] = random.uniform(-1.0, 1.0)

        for K in range(self._K, 0, -1):
            N, sN = 2**K, 2**(K-1)

            for i in range(2**(self._K-K)):
                for j in range(2**(self._K-K)):
                    self._map[i*N+sN][j*N+sN] = \
                        self._Get(N, \
                        (i*N, i*N, i*N+N, i*N+N), \
                        (j*N, j*N+N, j*N+N, j*N))

            for i in range(2**(self._K-K)+1):
                for j in range(2**(self._K-K)):
                    self._map[i*N][j*N+sN] = \
                        self._Get(N, \
                        (i*N, i*N-sN, i*N, i*N+sN), \
                        (j*N, j*N+sN, j*N+N, j*N+sN))

            for i in range(2**(self._K-K)):
                for j in range(2**(self._K-K)+1):
                    self._map[i*N+sN][j*N] = \
                        self._Get(N, \
                        (i*N+sN, i*N, i*N+sN, i*N+N), \
                        (j*N-sN, j*N, j*N+sN, j*N))

        self._Normilize()
