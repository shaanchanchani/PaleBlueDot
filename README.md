1. Project Overview

XOR Cipher:
An XOR Cipher is an example of a symmetric-key cryptosystem or a “secret key” system. This system sends an encrypted message along with an encrypted key to open the message. In this system the same key is used both for encryption and decryption of the image or message. The process in which this operates is an image is taken and encrypted using a key generator, that image is then transmitted to the receiver who uses the same key generator to decrypt the image. The issue with this method is that it requires both parties have the same key generator, and neither can send the key generator to the other because it could be intercepted and therefore useless. This means this system is great as long as it was set up before messages were being intercepted, or face to face.

Noise Reduction:
This is a crucial step to complete before developing a gradient map. Edge detection involves viewing pixel derivatives to identify the location of discontinuities. These discontinuities are where the edges are located. Smoothing an image prior to edge detection is vital because it ensures that only actual edges are detected. An image with a large amount of noise will likely identify many false edges.

Gradient Map:
In this project we were able to develop a gradient map by implementing the sobel algorithm. In the simplest of terms, the sobel algorithm operates by running a small matrix window over each value in a grayscale image matrix. For every value in the matrix, the algorithm measures the gradient change in the window. The greater the gradient change, the more intense the edge is.

2. Discussion of Algorithmn Design

`importImage()`
Using matplotlib to import a PNG file results in a data type of float32. The range of this data type is [0.0,1.0]. Importing both a JPG image and a TIFF image results in a data type of uint8. The range of this data type is [0,255]. Since we want values in a range of [0,255] the image will need to be uint8. Conversion from float32 to uint8 can be done by multiplying the data by 255 and then casting it as uint8. The following code demonstrates this:
image = (image*255).astype(np.uint8) 
The code for this function is optimal for use by any future image processing operations
using matplotlib.

`toDecimal() & toBinary`
These are two very simple user-defined functions. The XORcipher() function requires seamless conversions of values from binary to decimal and vice-versa. The easiest way to accomplish this was to create user-defined functions that can operate within XORcipher(). These functions are also optimal for use in any program that requires binary/decimal conversions. The only limitation is that toBinary() outputs in a datatype of string rather than a bin. However, this can be easily mitigated by casting.

`XORcipher()`
The XOR cipher was designed using a series of nested for loops, user defined functions, Python’s built in functions, and functions from the numpy library. The first step was to initialize a decrypted image matrix to be the same size as the encrypted image matrix. The shape() and zeros() functions from the numpy library make this simple.
```
 nR, nC,nCh = encryptedIm.shape
 decryptedIm = np.zeros([nR,nC,nCh])
 ```
Next, we can iterate through and convert each element of the key matrix and encrypted image matrix to binary. This was done with the following code:
```
 for row in range(len(encryptedIm)):
         for column in range(len(encryptedIm[row])):
             K = toBinary(keyMat[row][column])
             for color in range(len(encryptedIm[row][column])):
                 A = toBinary(encryptedIm[row][column][color])
```
Each iteration of this structure allows us to simultaneously access a key matrix value in binary and its corresponding 3 RGB values in binary. The next step is to take each key value and perform a bitwise XOR with each of its RGB values. This was done inside the loop structure with the following code:
```
                 newBin = ""
                 for valA,valK in zip(A,K):
                     newBin = newBin + str(ord(valA)^ord(valK))
```
The user-defined function returns a string so the newBin string was created to hold the binary value generated from the bitwise XOR. Python’s built-in zip() function allows us to iterate through two strings simultaneously. For each iteration, ord() allows us to cast each character as an int so that we can use the XOR operator. The result is then cast as string and added to the newBin string. The final step is to convert the new binary number generated (newBin) back to a decimal value and store it in the decrypted image matrix. Then convert the entire decrypted image matrix to uint8 before passing it to other functions. The following code demonstrates this last step:
```
                 decryptedIm[row][column][color] = toDecimal(newBin)
   decryptedIm = decryptedIm.astype(np.uint8)
return decryptedIm
```
This function can be used by any future related projects. All that is necessary for it to
run is an encrypted image and its corresponding key matrix.

`toGreyscale()`
The toGreyscale() function converts a color image into a black and white image. This was done by pulling the RGB values at each pixel and converting them into one value that represents brightness. Each color channel contributes towards a pixel’s brightness in a different way. This is why each channel value is multiplied by a different constant. The constants used were taken from ITU-R Recommendation BT.709, also known as Rec. 709. Rec. 709 is the standard for high-definition television image encoding. Given that it only needs a color image input, this function can be used for any future grayscale conversions.

`smoothFilter()`
This function requires a grayscale image to be inputted for it to correctly reduce noise. The purpose of this function is to prepare an image for an edge detection process. The first step is to manually input the gaussian kernel and initialize an empty matrix of the same size as the input image. The empty matrix is created to hold the data of the blurred image. This step is demonstrated by the following lines of code.
```
 gKernel=np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,
 16,4],[1,4,6,4,1]])/256
 smoothIm = np.zeros([greyIm.shape[0],greyIm.shape[1]])
 ```
Next we can iterate through each row and column of the grayscale image to access the values. This iteration must be done with the consideration of the kernel size. This is because in order to evaluate the blurry values we have to multiply the gaussian kernel by an equally sized window centered around each value. The gaussian kernel is 5 pixels by 5 pixels. This means that if we’re basing our 5x5 windows on a center value, the center value must have 2 pixels surrounding it on all edges. Python will return an error message if you try to create a 5x5 window surrounding a center value without 2 pixels on each edge. The iteration was accomplished with the following code.
```
 for row in range(2, greyIm.shape[0]-2):
         for column in range(2, greyIm.shape[1]-2):
             window = greyIm[row-2:row+3,column-2:column+3]
             blurryPixel = abs(np.sum(window*gKernel))
             smoothIm[row][column] = blurryPixel
```
The for loops range only on the rows and columns in which the center pixel of the window will have sufficient points around it. The sum of the window multiplied by the gaussian kernel is set equal to the variable blurryPixel. The value of smoothIm at the current iteration’s row and column index is set equal to the value held by blurryPixel. The final step of this function is to simply return the smoothIm matrix.
`return smoothIm`
Despite the function only being able to work with grayscale images, it is still optimal for future edge detection programs. Grayscale images are best suited for edge detection due to efficiency and simplicity. Edge detection on color images requires much more complex algorithms. This is because you would have to operate on all 3 color channels.

`edgeDetection()`
This function inputs a grayscale image and outputs a gradient map, a location tuple of where Earth is located in the image, and a cropped image zoomed in on earth. Before we’re able to find the location of earth in the image we have to develop a gradient map of the image. This process is initiated by manually creating matrices for each directional kernel and each directional gradient map.
```
 xDirKernel = np.array([[-1,0,1,],[-2,0,2],[-1,0,1]])
 yDirKernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
 newImX = np.zeros([smoothIm.shape[0]-2,smoothIm.shape[1]-2])
 newImY = np.zeros([smoothIm.shape[0]-2,smoothIm.shape[1]-2])
```
Next, we can iterate over the array and apply the kernels in the same way the gaussian kernel was applied.
```
 for row in range(2, smoothIm.shape[0]-2):
         for column in range(2,smoothIm.shape[1]-2):
            window = smoothIm[row-1:row+2,column-1:column+2]
            xPix = np.sum(xDirKernel*window)
            yPix = np.sum(yDirKernel*window)
            newImX[row][column] = xPix
            newImY[row][column] = yPix
```
The code above gives us gradient matrices for the x and y directions. We can plug the matrices into the sobel operator and then rescale the data to create a single gradient map of the image.
 ```
 gradientMag = np.sqrt(np.square(newImX) + np.square(newImY))
 gradientMag *= 255.0 / gradientMag.max()
```
Now that we have a gradient map the image is ready for edge detection. The pixels in the gradient map are arranged in brightness on a scale of 0 to 255. By the viewing gradient map (a.figure 4), it’s clear that the pixel values, excluding those of earth, are generally homogeneous. This means that we can simply iterate through the map until we find a pixel of sufficient magnitude. Once that pixel is found, we can set the variables rowLocation and columnLocation to the corresponding pixel indices.
```
for row in range(2, smoothIm.shape[0]-2):
        for column in range(2, smoothIm.shape[0]-2):
            if gradientMag[row][column] > 120:
                rowLocation = row
                columnLocation = column
                break
return gradientMag, croppedIm
```
This function would be difficult to implement in future image projects, as it is catered specifically for the pale blue dot image. However, the gradient map portion can easily be pulled out and placed in its own function for future use.

`plotColorDistribution()`
When using the initial key of 4 the encryption is much better. This can be displayed by comparing the peaks of the histograms (a.figure6 and a.figure8). A larger peak means a greater information entropy, effectively making the image more difficult to decipher.

3. References 
Good links for further research
https://jivp-eurasipjournals.springeropen.com/articles/10.1186/s13640-018-0386-3 
https://ui.adsabs.harvard.edu/abs/2018JPhCS1004a2023T/abstract 
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7998182/

4. Appendices: