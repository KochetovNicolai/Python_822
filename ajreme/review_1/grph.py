from PIL import Image
from mkwrld import MakeWorldRGB


def Show(image):
    N, M = len(image), len(image[0])
    img = Image.new('RGB', (N, M), 'black')
    pixels = img.load()

    for i in range(N):
        for j in range(M):
            pixels[i, j] = image[i][j]
    img.show()


Show(MakeWorldRGB(129, 129, seaLevel=0.45))
