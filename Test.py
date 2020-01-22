from PIL import Image
import pickle, pprint

pkl_file = open("trained.pkl", 'rb')

trained = pickle.load(pkl_file)

pkl_file.close()


testImg = Image.open("zuck.jpg")
pix = testImg.load()
testWidth, testHeight = testImg.size
#print("test width: ", testWidth, " testhei: ", testHeight)

for p in range(testWidth-1):
    for q in range(testHeight-1):
        r = pix[p,q][0]
        g = pix[p,q][1]
        b = pix[p,q][2]

        if trained[r][g][b]<0.4999 :
            pix[p,q]=(255,255,255)
            #pix[p,q][1]=255
            #pix[p,q][2]=255

testImg.save("zuck.png")
print("image saved")


