def getReversedRGB(rgb):
    reversedR = (127 - (rgb[0] - 128)) % 256
    reversedG = (127 - (rgb[1] - 128)) % 256
    reversedB = (127 - (rgb[2] - 128)) % 256

    return (reversedR, reversedG, reversedB)