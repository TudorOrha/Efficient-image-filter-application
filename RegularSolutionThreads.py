import time
import _thread
from PIL import Image

nrOfThreads = 4

def applyFilterOnPart(img, pixels, originalPixels, kernel, threadNr):
    fromI = int(round(threadNr*(img.size[0]-1)/nrOfThreads))
    if fromI == 0:
        fromI = 1
    toI = int(round((1+threadNr)*(img.size[0]-1)/nrOfThreads))
    for i in range(fromI, toI):
        for j in range(1,img.size[1]-1):
            accumulatorR = 0
            accumulatorG = 0
            accumulatorB = 0
            
            for kerRow in range(len(kernel)):
                for kerCol in range(len(kernel[kerRow])):
                    accumulatorR += kernel[kerRow][kerCol] * originalPixels[i+1-kerRow,j+1-kerCol][0]  
                    accumulatorG += kernel[kerRow][kerCol] * originalPixels[i+1-kerRow,j+1-kerCol][1]
                    accumulatorB += kernel[kerRow][kerCol] * originalPixels[i+1-kerRow,j+1-kerCol][2]

            pixels[i,j] = (int(round(accumulatorR)), int(round(accumulatorG)), int(round(accumulatorB)))
            

def main():
    print("Regular Solution With Threads Output:")
    start = time.time()

    #kernel = [[0,0,0],[0,1,0],[0,0,0]]
    kernel = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
    #kernel = [[0,-1,0],[-1,5,-1],[0,-1,0]]
    #kernel = [[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]]

    
    
    originalImg = Image.open("OriginalPic.png")
    originalPixels = originalImg.load()
    img = Image.open("OriginalPic.png")
    pixels = img.load()

    try:
        for i in range(0,nrOfThreads):
            _thread.start_new_thread(
                applyFilterOnPart, (img, pixels, originalPixels, kernel, i))
    except:
        print ("Error: unable to start threads")


    time.sleep(0.06)

    width, height = img.size
    img = img.crop((1, 1, width-1, height-1))

    end = time.time()
    print(end - start,"\n")
    #img.show()
    
