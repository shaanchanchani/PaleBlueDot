import numpy as np
import matplotlib.pyplot as plt
import time
import random
from Funcs import importImage, keyGenerator, XORcipher, newKeyGenerator, plotColorDistribution, toGreyscale, smoothFilter, edgeDetection 
plotColorDistribution, newKeyGenerator

def main():
    #get start time
    startTime = time.time()
    #import image
    encryptIm = importImage()
    #ask user for initial key and generate key matrix with it
    initialKey = input("Enter initial key: ")
    keyMat = keyGenerator(encryptIm.shape[0],encryptIm.shape[1],initialKey)
    #encrypted image
    plt.figure(0)
    plt.imshow(encryptIm)
    #decrypts encrypted image
    plt.figure(1)
    decryptIm = XORcipher(encryptIm,keyMat)
    plt.imshow(decryptIm)
    plt.savefig("Pale_Blue_Dot_Decrypted.tiff")
    #converts decrypted image to grayscale
    plt.figure(2)
    greyIm = toGreyscale(decryptIm)
    plt.imshow(greyIm,cmap='gray')
    plt.savefig("Pale_Blue_Dot_Grayscale.tiff")
    #blurs grayscale image
    plt.figure(3)
    smoothIm = smoothFilter(greyIm)
    plt.imshow(smoothIm,cmap='gray')
    plt.savefig("Pale_Blue_Dot_GrayscaleBlur.tiff")
    #converts grayscale to gradient map
    plt.figure(4)
    part3output = edgeDetection(smoothIm)
    plt.imshow(part3output[0],cmap='gray')
    plt.savefig("Pale_Blue_Dot_GradientMap.tiff")
    #cropped window around earth
    plt.figure(5)
    row = part3output[1]
    col = part3output[2]
    print(f'Earth Located at: ({row},{col})')
    croppedIm = decryptIm[row-50:row+50,col-50:col+50]
    plt.imshow(croppedIm)
    plt.savefig("Pale_Blue_Dot_Cropped.tiff")
    #color distribution of encrypted image
    plt.figure(6)
    plotColorDistribution(encryptIm)
    plt.savefig("Pale_Blue_Dot_Encrypted_Histogram.tiff")
    #re-encrypts decrypted image
    plt.figure(7)
    random.seed(int(input("Enter new initial key: ")))
    newInitialKey = round(random.uniform(0,50),0)
    newKeyMat = newKeyGenerator(decryptIm.shape[0],decryptIm.shape[1], newInitialKey)
    reencryptIm = XORcipher(decryptIm,newKeyMat)
    plt.imshow(reencryptIm)
    plt.savefig("Pale_Blue_Dot_Reencrypted.tiff")
    #color distribution of re-encrypted image
    plt.figure(8)
    plotColorDistribution(reencryptIm)
    plt.savefig("Pale_Blue_Dot_Reencrypted_Histogram.tiff")
    #runtime is the difference between start time and end time
    print(f"Runtime: {time.time() - startTime}")

if __name__ == '__main__':
    main()