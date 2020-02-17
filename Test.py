from PIL import Image
import pickle, pprint


def calculateAccuracy(index):
    right = 0
    wrong = 0
    avg = 0
    for i in range(len(index)):
        if index[i] < 10:
            img = "newMask/000" + str(index[i]) + ".png"
        elif index[i] < 100:
            img = "newMask/00" + str(index[i]) + ".png"
        else:
            img = "newMask/0" + str(index[i]) + ".png"

        if index[i] < 10:
            img2 = "ibtd/Mask/000" + str(index[i]) + ".bmp"
        elif index[i] < 100:
            img2 = "ibtd/Mask/00" + str(index[i]) + ".bmp"
        else:
            img2 = "ibtd/Mask/0" + str(index[i]) + ".bmp"

        im = Image.open(img, 'r')
        width, height = im.size
        pixel_values = list(im.getdata())
        totalSize = len(pixel_values)

        im2 = Image.open(img2, 'r')
        width2, height2 = im2.size
        pixel_values2 = list(im2.getdata())

        for x in range(totalSize):
            if pixel_values[x] != pixel_values2[x]:
                wrong += 1
            else:
                right += 1

    avg = (right / (right + wrong)) * 100
    print('Acuracy : ', avg, '%')
    return avg


def main(trained, index):
    for i in range(len(index)):
        if index[i] < 10:
            img = "ibtd/000" + str(index[i]) + ".jpg"
        elif index[i] < 100:
            img = "ibtd/00" + str(index[i]) + ".jpg"
        else:
            img = "ibtd/0" + str(index[i]) + ".jpg"

        testImg = Image.open(img)
        pix = testImg.load()
        testWidth, testHeight = testImg.size
        # print("test width: ", testWidth, " testhei: ", testHeight)

        for p in range(testWidth - 1):
            for q in range(testHeight - 1):
                r = pix[p, q][0]
                g = pix[p, q][1]
                b = pix[p, q][2]

                if trained[r][g][b] < 0.5555:
                    pix[p, q] = (255, 255, 255)
                    # pix[p,q][1]=255
                    # pix[p,q][2]=255

        if index[i] < 10:
            img2 = "newMask/000" + str(index[i]) + ".png"
        elif index[i] < 100:
            img2 = "newMask/00" + str(index[i]) + ".png"
        else:
            img2 = "newMask/0" + str(index[i]) + ".png"
        testImg.save(img2)
    avrg  = calculateAccuracy(index)
    return avrg
