
import time
import numpy as np
from PIL import Image
from numba import stencil, vectorize, cuda, guvectorize

@stencil()
def applyKernelOnPixel(a,color):
    clr1 = 1
    return (a[-1,-1,clr1]*-1 + a[-1, 0,clr1]*-1 + a[-1,1,clr1]*-1 +
            a[ 0,-1,clr1]*-1 + a[ 0, 0,clr1]* 8 + a[ 0,1,clr1]*-1 +
            a[ 1,-1,clr1]*-1 + a[ 1, 0,clr1]*-1 + a[ 1,1,clr1]*-1
            )

@vectorize(["float32(float32,float32)"],target="cpu")
def computePixel(a,b):
    return a * b

@vectorize(["float32(float32,float32)"],target="cpu")
def computeImage(a,kernel):
    arr0 = []
    arr1 = []
    arr2 = []
    for kerRow in range(len(kernel)):
        for kerCol in range(len(kernel[kerRow])):
            arr0.append(originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][0])
            arr1.append(originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][1])
            arr2.append(originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][2])
    arr0 = np.array(arr0, dtype = np.float32)
    arr1 = np.array(arr1, dtype = np.float32)
    arr2 = np.array(arr2, dtype = np.float32)
    #computePixel(arr0, kernelVec)
    #computePixel(arr1, kernelVec)
    #computePixel(arr2, kernelVec)


@guvectorize(["(int64[:], int64, int64[:])"], '(n),()->(n)')
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y


@cuda.jit("void(int8[:,:,:],float32[:,:],int8[:,:,:])", target="cpu")
def add_gpu_1d(imgVec, kernel, res):
    x,y,z = cuda.grid(3)
    if x <= imgVec.shape[0]:
        for j in range(len(kernel)//2, imgVec.shape[1] - len(kernel)//2):
            accumulatorR = 0
            accumulatorG = 0
            accumulatorB = 0
            for kerRow in range(len(kernel)):
                for kerCol in range(len(kernel[kerRow])):
                    accumulatorR += kernel[kerRow][kerCol] * imgVec[x+len(kernel)//2 - kerRow][j+len(kernel)//2 - kerCol][0]
                    accumulatorG += kernel[kerRow][kerCol] * imgVec[x+len(kernel)//2 - kerRow][j+len(kernel)//2 - kerCol][1]
                    accumulatorB += kernel[kerRow][kerCol] * imgVec[x+len(kernel)//2 - kerRow][j+len(kernel)//2 - kerCol][2]
            res[x][j][0] = np.int8(accumulatorG)
            res[x][j][1] = np.int8(accumulatorG)
            res[x][j][2] = np.int8(accumulatorG)

def main(imageName, kernel, showResult):
    
    print("CUDA Solution Output:\n")
    start = time.time()

    originalImg = Image.open(imageName)
    img = Image.open(imageName)
    originalPixels = originalImg.load()
    '''
    kernelVec = np.asarray(kernel, dtype=np.float32).reshape(-1)
    #reversing it
    kernelVec = kernelVec[::-1]
    kernelVecs = np.tile(kernelVec,(img.size[0]*img.size[1],1))
    
    result = np.array(img)
    #computeImage(result, kernelVecs)
    '''
    
    '''
    first = np.array([1,2,3,4])
    second = np.array([2,3,1,4])
    result = np.array([5,5,5,5])
    g(first,6,result)
    print(first,result)
    '''
    imgVec = np.array(img).astype(np.int8)
    kernelArray = np.array(kernel).astype(np.float32)
    result = np.array(img).astype(np.int8)
    threadsPerBlock = 256
    blocksPerGrid   = 1
    add_gpu_1d[blocksPerGrid, threadsPerBlock](imgVec,kernelArray,result)
    #print(result[50])
    result.tofile("cuda.txt")
    newimg = Image.fromarray(result, 'RGB')
    newimg.show()
    '''
    first = np.array([1,2,3,4]).astype(np.float32)
    second = np.array([2,3,1,4]).astype(np.float32)
    result = np.array([5,5,5,5]).astype(np.float32)
    #dfirst = cuda.to_device(first)
    #dsecond = cuda.to_device(second)
    #dresult = cuda.to_device(result)
    #dresult = cuda.to_device(result)
    data = first
    threadsperblock = 32
    #add_gpu_1d[32,(data.size + (threadsperblock - 1)) // threadsperblock](first,second,result)
    add_gpu_1d[4,1](first,second,result)
    #dresult.copy_to_host(result)
    print(first,result)
    '''

    '''
    for i in range(len(kernel)//2, img.size[0] - len(kernel)//2):
        for j in range(len(kernel)//2, img.size[1] - len(kernel)//2):
            arr0 = []
            arr1 = []
            arr2 = []
            for kerRow in range(len(kernel)):
                for kerCol in range(len(kernel[kerRow])):
                    arr0.append(originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][0])
                    arr1.append(originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][1])
                    arr2.append(originalPixels[i+len(kernel)//2 - kerRow,j+len(kernel)//2 - kerCol][2])
            arr0 = np.array(arr0, dtype = np.float32)
            arr1 = np.array(arr1, dtype = np.float32)
            arr2 = np.array(arr2, dtype = np.float32)
            computePixel(arr0, kernelVec)
            computePixel(arr1, kernelVec)
            computePixel(arr2, kernelVec)
    '''


    '''
    input_arr = np.array(img)
    for i in range(1):
        output_arr = applyKernelOnPixel(input_arr,0)
   
    output_arr = output_arr.astype(np.uint8)
    print(output_arr[3][:10])
    new_img = Image.fromarray(output_arr, mode=img.mode)
    new_img.format = img.format
    img = new_img
    '''
    

    
    width, height = img.size
    img = img.crop((len(kernel)//2, len(kernel)//2, width - len(kernel)//2, height - len(kernel)//2))

    end = time.time()
    print(end - start,"\n")
    
    if showResult:
        img.show()
