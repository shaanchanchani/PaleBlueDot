import numpy as np
import matplotlib.pyplot as plt
import os

def importImage():
     #Prompt user to enter filename
     fileName = input("Enter the name of your color image file: ")
     #Error handling
     if (fileName[-1:-3] != "iff" and fileName[-1:-3] != "png" and fileName[-1:-3] != "jpg" ):
         print("ERROR: Bad file input, try again! ")
         print(" ")
         print("Exiting program...")
         raise SystemExit()
     #Read image data
     image = plt.imread(fileName)[:,:,:3]
     #Converts to uint8 if necessary and passes image data
     if(image.dtype != "uint8"):
         image = (image*255).astype(np.uint8)
         return image
     else:
        return image

#converts binary to decimal
#inputs string, outputs int
def toDecimal(numBinary):
     numBinary = numBinary[::-1]
     num = 0
     numBinary = list(numBinary)
     numBinary = [int(i) for i in numBinary]
     for i in range(8):
         num = num + numBinary[i]*2**i
     return num

#converts decimal to binary
#inputs int, outputs string
def toBinary(num):
    numBinary = ""
    for i in range(8):
        r = num % 2
        num = num //2
        numBinary = numBinary + str(r)
    return numBinary[::-1]

#generates key matrix
def keyGenerator(rows,columns,initialKey):
     letterCount = len(initialKey) - initialKey.count(" ")
     keyMat = np.zeros([rows,columns])
     for i in range(len(keyMat)):
         for j in range(len(keyMat[i])):
             A = i * j % letterCount
             keyMat[i][j] = A*((2**8)//(letterCount))
     keyMat = keyMat.astype(np.uint8)
     return keyMat

#performs XORcipher
def XORcipher(encryptedIm, keyMat):
     nR, nC,nCh = encryptedIm.shape
     decryptedIm = np.zeros([nR,nC,nCh])
     for row in range(len(encryptedIm)):
         for column in range(len(encryptedIm[row])):
             K = toBinary(keyMat[row][column])
             for color in range(len(encryptedIm[row][column])):
                 A = toBinary(encryptedIm[row][column][color])
                 newBin = ""
                 for valA,valK in zip(A,K):
                     newBin = newBin + str(ord(valA) ^ ord(valK))
                 decryptedIm[row][column][color] = toDecimal(newBin)
     decryptedIm = decryptedIm.astype(np.uint8)
     return decryptedIm

#converts color image to grayscale
def toGreyscale(image):
    greyIm = np.zeros([image.shape[0],image.shape[1]])
    if(image.dtype != "float64"):
        image = image.astype(np.float64)
    for row in range(len(image)):
        for column in range(len(image[row])):
            redPixel = image[row][column][0]
            greenPixel = image[row][column][1]
            bluePixel = image[row][column][2]
            greyPixel = (redPixel*.2126) + (greenPixel*.7152) + (bluePixel*.0722)
            greyIm[row][column] = greyPixel
    return greyIm

#blurs grayscale image
def smoothFilter(greyIm):
    gKernel =np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]])/256
    smoothIm = np.zeros([greyIm.shape[0],greyIm.shape[1]])
    for row in range(2, greyIm.shape[0]-2):
        for column in range(2, greyIm.shape[1]-2):
            window = greyIm[row-2:row+3,column-2:column+3]
            blurryPixel = abs(np.sum(window*gKernel))
            smoothIm[row][column] = blurryPixel
    return smoothIm

#converts grayscale image to a gradient map
def edgeDetection(smoothIm):
    xDirKernel = np.array([[-1,0,1,],[-2,0,2],[-1,0,1]])
    yDirKernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    newImX = np.zeros([smoothIm.shape[0]-2,smoothIm.shape[1]-2])
    newImY = np.zeros([smoothIm.shape[0]-2,smoothIm.shape[1]-2])
    for row in range(2, smoothIm.shape[0]-2):
        for column in range(2,smoothIm.shape[1]-2):
            window = smoothIm[row-1:row+2,column-1:column+2]
            xPix = np.sum(xDirKernel*window)
            yPix = np.sum(yDirKernel*window)
            newImX[row][column] = xPix
            newImY[row][column] = yPix
    gradientMag = np.sqrt(np.square(newImX) + np.square(newImY))
    gradientMag *= 255.0 / gradientMag.max()
    for row in range(2, smoothIm.shape[0]-2):
        for column in range(2, smoothIm.shape[0]-2):
            if gradientMag[row][column] > 120:
                 rowLocation = row
                 columnLocation = column
                 break
    return gradientMag, rowLocation, columnLocation

#creates histogram of color distribution
def plotColorDistribution(image):
    image = (image*255).astype(np.uint8)
    plt.hist(image[:,:,0].reshape(image.shape[0]*image.shape[1]),bins=np.arange(2**8+1), color = "red", alpha=0.5)
    plt.hist(image[:,:,1].reshape(image.shape[0]*image.shape[1]),bins=np.arange(2**8+1), color = "green", alpha=0.5)
    plt.hist(image[:,:,2].reshape(image.shape[0]*image.shape[1]),bins=np.arange(2**8+1), color = "blue", alpha=0.5)

#generates a new key array
def newKeyGenerator(rows,columns,initialKey):
    key = int(initialKey)
    #if the user doesn't enter 4, print error message
    if key != 12:
        print("ERROR: Wrong key, try again! ")
        print(" ")
        print("Exiting program...")
        raise SystemExit()
    keyMat = np.zeros([rows,columns])
    for i in range(len(keyMat)):
        for j in range(len(keyMat[i])):
            A = i * j % key
            keyMat[i][j] = A*((2**8)//(key))
    keyMat = keyMat.astype(np.uint8)
    return keyMat