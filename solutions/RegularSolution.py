import time
from PIL import Image

def main(imageName, kernel, showResult):
    print("Regular Solution Output:")
    start = time.time()
     
    originalImg = Image.open(imageName)
    img = Image.open(imageName)

    originalPixels = originalImg.load()
    pixels = img.load()
    
    for i in range(len(kernel)//2, img.size[0] - len(kernel)//2):
        for j in range(len(kernel)//2, img.size[1] - len(kernel)//2):
            accumulatorR = 0
            accumulatorG = 0
            accumulatorB = 0
            
            for kerRow in range(len(kernel)):
                for kerCol in range(len(kernel[kerRow])):
                    accumulatorR += kernel[kerRow][kerCol] * originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][0]  
                    accumulatorG += kernel[kerRow][kerCol] * originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][1]
                    accumulatorB += kernel[kerRow][kerCol] * originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][2]

            pixels[i,j] = (int(round(accumulatorR)), int(round(accumulatorG)), int(round(accumulatorB)))
            
    width, height = img.size
    img = img.crop((len(kernel)//2, len(kernel)//2, width - len(kernel)//2, height - len(kernel)//2))

    end = time.time()
    print(end - start,"\n")
    if showResult:
        img.show()
