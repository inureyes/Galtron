def getInvertedRGB(rgb):
    invertedR = (127 - (rgb[0] - 128)) % 256
    invertedG = (127 - (rgb[1] - 128)) % 256
    invertedB = (127 - (rgb[2] - 128)) % 256

    return (invertedR, invertedG, invertedB)