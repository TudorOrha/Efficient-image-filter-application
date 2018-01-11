from solutions import RegularSolution 
from solutions import RegularSolutionThreads
from solutions import DistributedSolution
from solutions import CUDASolution

#https://en.wikipedia.org/wiki/Kernel_(image_processing)
if __name__ == '__main__':
    imageName = "pictures/"
    imageName += "200.jpg"
    showResults = 0
    
    #identity
    kernel = [[0,0,0],[0,1,0],[0,0,0]]
    
    #edge detection
    #kernel = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
    #kernel = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,24,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    #kernel = [[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,48,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]]

    #sharpen
    kernel = [[0,-1,0],[-1,5,-1],[0,-1,0]]

    #box blur
    #kernel = [[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]]

    for i in range(1, 2):
        RegularSolution.main(imageName, kernel, showResults)
        #RegularSolutionThreads.main(imageName, kernel, showResults)
        #DistributedSolution.main()
        CUDASolution.main(imageName, kernel, showResults)
    
