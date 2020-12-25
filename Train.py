import math
from PIL import Image
import pickle
import random
import Test as test


def countPixels(height, width, pixel_values, pixel_values2, skin2, nonSkin2):
    for count in range(height * width - 1):
        a = pixel_values[count][0]
        b = pixel_values[count][1]
        c = pixel_values[count][2]

        if pixel_values2[count][0] > 241 and pixel_values2[count][1] > 241 and pixel_values2[count][2] > 241:
            nonSkin2[a][b][c] += 1
        else:
            skin2[a][b][c] += 1


def readImage(skin2, nonSkin2, skipIndex):
    for i in range(555):
        if i in skipIndex:
            continue
        print('PROCESSING: ', i)
        if i < 10:
            img = "ibtd/000" + str(i) + ".jpg"
        elif i < 100:
            img = "ibtd/00" + str(i) + ".jpg"
        else:
            img = "ibtd/0" + str(i) + ".jpg"

        im = Image.open(img, 'r')
        width, height = im.size
        pixel_values = list(im.getdata())

        if (i < 10):
            img2 = "ibtd/Mask/000" + str(i) + ".bmp"
        elif i < 100:
            img2 = "ibtd/Mask/00" + str(i) + ".bmp"
        else:
            img2 = "ibtd/Mask/0" + str(i) + ".bmp"

        im2 = Image.open(img2, 'r')
        width2, height2 = im2.size
        pixel_values2 = list(im2.getdata())

        countPixels(height, width, pixel_values, pixel_values2, skin2, nonSkin2)


def calcSumAndProbability(arr):
    sum = 0
    for p in range(256):
        for q in range(256):
            for r in range(256):
                sum = sum + arr[p][q][r]

    for p in range(256):
        for q in range(256):
            for r in range(256):
                if (arr[p][q][r] != 0):
                    arr[p][q][r] = arr[p][q][r] / sum


def calcTrainedData(skin2, nonSkin2, trained2):
    for p in range(256):
        for q in range(256):
            for r in range(256):
                if nonSkin2[p][q][r] == 0 and skin2[p][q][r] != 0:
                    trained2[p][q][r] = 10
                elif skin2[p][q][r] == 0 and nonSkin2[p][q][r] != 0:
                    trained2[p][q][r] = 0.000001
                elif skin2[p][q][r] == 0 and nonSkin2[p][q][r] == 0:
                    trained2[p][q][r] = 0.00001
                else:
                    trained2[p][q][r] = skin2[p][q][r] / nonSkin2[p][q][r]


skin = [[[0 for col in range(256)] for row in range(256)] for x in range(256)]
nonSkin = [[[0 for col2 in range(256)] for row2 in range(256)] for x2 in range(256)]
trained = [[[0 for col3 in range(256)] for row3 in range(256)] for x3 in range(256)]
tempRandomIndex = random.sample(range(0, 555), 555)

indexCounter = 0
randomIndex = []
for i in range(10):
    randomIndex.append([])
counter = 0
for i in range(10):
    for j in range(math.ceil(555 / 10)):
        randomIndex[i].append(tempRandomIndex[counter])
        counter += 1
        if counter == 555:
            break

avg = 0
for i in range(10):
    readImage(skin, nonSkin, randomIndex[i])
    calcSumAndProbability(skin)
    calcSumAndProbability(nonSkin)
    calcTrainedData(skin, nonSkin, trained)
    
    avg += test.main(trained, randomIndex[i])

    skin = [[[0 for col in range(256)] for row in range(256)] for x in range(256)]
    nonSkin = [[[0 for col2 in range(256)] for row2 in range(256)] for x2 in range(256)]
    trained = [[[0 for col3 in range(256)] for row3 in range(256)] for x3 in range(256)]
    

print('\n\nFinal::: ', avg/10,'%')