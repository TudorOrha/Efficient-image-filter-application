import time
import threading
import multiprocessing
from multiprocessing import Pool
from PIL import Image

nrOfThreads = multiprocessing.cpu_count()

class myThread (threading.Thread):
    def __init__(self, threadID, kernel, img, originalImg):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.kernel = kernel
        self.img = img
        self.originalImg = originalImg
        self.pixels = img.load()
        self.originalPixels = originalImg.load()
        
    def run(self):
        applyFilterOnPart(self.threadID, self.kernel, self.img, self.originalImg)


def applyFilterOnPart(threadNr, kernel, img, originalImg):
    pixels = img.load()
    originalPixels = originalImg.load()
    fromI = int(round(threadNr*(img.size[0]-2*(len(kernel)//2))/nrOfThreads)) + len(kernel)//2
    toI = int(round((1+threadNr)*(img.size[0]-2*(len(kernel)//2))/nrOfThreads)) + len(kernel)//2
    for i in range(fromI, toI):
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
    return img


def generateParameters(kernel, img, originalImg):
    params = []
    for k in range(nrOfThreads):
        params.append((k, kernel, img, originalImg))
    return params
        
            
def main(imageName, kernel, showResult):
    print("Regular Solution With Threads Output:")
    start = time.time()
    originalImg = Image.open(imageName)
    img = Image.open(imageName)

    pixels = img.load()

    with Pool(processes=nrOfThreads) as pool:
        results = pool.starmap(applyFilterOnPart, generateParameters(kernel,img,originalImg))
    
    for k in range(nrOfThreads):
        fromI = int(round(k*(img.size[0]-2*(len(kernel)//2))/nrOfThreads)) + len(kernel)//2
        toI = int(round((1+k)*(img.size[0]-2*(len(kernel)//2))/nrOfThreads)) + len(kernel)//2
        for i in range(fromI, toI):
            for j in range(len(kernel)//2, img.size[1] - len(kernel)//2):
                pixels[i,j] = results[k].load()[i,j]        
  
    '''
    threads = []
    for i in range (nrOfThreads):
        thread = myThread(i, kernel, img, originalImg)
        threads.append(thread)
        thread.start()
        
    for i in range (nrOfThreads):
        threads[i].join()
    '''
    width, height = img.size
    img = img.crop((len(kernel)//2, len(kernel)//2, width - len(kernel)//2, height - len(kernel)//2))

    end = time.time()
    print(end - start,"\n")
    if showResult:
        img.show()
