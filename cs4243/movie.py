"""
=======================================================
Course: CS4243.
Course Title: Computer Vision & Pattern Recognition.
Project: CS4243 Project on 3D Walk-through of 2D Image.
Group Members: Dave Tan Woo Hong (A0106505R)
               Desmond Lim Hock Yeam (A0106477B)
               Toh Zijing (A0123506R)
               Darren Boo Kuok Liang (A0087547N)
=======================================================
=======   ==========   ===========  ============================================
Version      Date      Modified By                    Details
=======   ==========   ===========  ============================================
1.0.0     01/11/2014   ???          Added new Class Movie.
"""

#===============
#Initialisation.
#===============
from inputmodehandler import InputModeHandler
import numpy as np
import os
import cv2

class Movie(InputModeHandler):
    #========
    #Methods.
    #========
    def __init__(self, window, imageObj):
        #===================
        #Constructor Method.
        #===================
        super(Movie, self).__init__()
        self._window = window
        self._imageObj = imageObj

        self._modeName = "Movie"

        self.cameraDataSet = []             #vector of vector (x,y,z,(3x3))
        self.cameraData =[]                 #vector (x,y,z,(3x3))

        self.frames = []
        self.frameCount = 0

        # keyboard event callback of the form
        # { keychar:callback(key) }
        self._keyboardEvents = {"a":self.UIEnterCameraTranslation,        #left
                                "d":self.UIEnterCameraTranslation,        #right
                                "w":self.UIEnterCameraTranslation,        #forward
                                "s":self.UIEnterCameraTranslation,        #backward
                                "r":self.UIEnterCameraTranslation,        #up
                                "f":self.UIEnterCameraTranslation,        #down
                                "q":self.UIEnterCameraTranslation,        #rotate left
                                "e":self.UIEnterCameraTranslation,        #roate right
                                chr(127):self.UIDeleteLastData,           #delete key
                                chr(13):self.UIEnterCameraTranslation,    #enter key
                                "c":self.ClearSetPoints,                  #clear all camera position
                                "l":self.UILoadCameraData,                #load predefined camera positions
                                                                "k":self._UIkeyframe}

        self.IMAGE_WIDTH = self._imageObj.getWidth()
        self.IMAGE_HEIGHT = self._imageObj.getHeight()
          
        #define camera movement interval
        self.TRANSLATION_X_INTERVAL = 50  
        self.TRANSLATION_Y_INTERVAL = 50
        self.TRANSLATION_Z_INTERVAL = 50
        self.ROTATION_INTERVAL = 20     #degree
        
        #define interpolation interval between each camera position                       
        self.TRANSLATION_Z_INTERPOLATION = 10   #10 frames intepolated between z
        self.TRANSLATION_X_INTERPOLATION = 10   #10 frames intepolated between x
        self.TRANSLATION_Y_INTERPOLATION = 10   #10 frames intepolated between y
        self.ROTATION_INTERPOLATION = 10        #10 frames intepolated between rotation

        #define camera boundary
        self.MIN_TRANSLATION_X = 0 
        self.MAX_TRANSLATION_X = self.IMAGE_WIDTH
        self.MIN_TRANSLATION_Y = 0   
        self.MAX_TRANSLATION_Y = self.IMAGE_HEIGHT
        self.MIN_TRANSLATION_Z = 0
        self.MAX_TRANSLATION_Z = 1000    
        self.MAX_ROTATION = 60          #degree
        
        self.MAX_FRAME = 30

                #x,y,z,rotdegree,rotmat
        self.INITIALCAMERADATA = [self.IMAGE_WIDTH/2, self.IMAGE_HEIGHT/2, 300, 0, np.identity(3)]

        """
        img = self._imageObj._image.copy()
        for e in self._imageObj._tri.edges:
            cv2.line(img,
                     tuple(self._imageObj._selected2DPoints[e[0]][:2]),
                     tuple(self._imageObj._selected2DPoints[e[1]][:2]), (0,255,0))
        img = self._imageObj.getResizedImage(img)
        self._window.display(img)
        """
        self.ClearSetPoints()


    def ClearSetPoints(self, key=None):
        self.cameraData = self.INITIALCAMERADATA
        self.cameraDataSet = []
        self.cameraDataSet.append(self.cameraData)
        self.frameCount = 0
        
    #revert to last saved point, cannot revert to last unsaved point
    def UIDeleteLastData(self, key):
                if (self.frameCount > 0):
                        #revert to last saved point
                        if(self.cameraData == self.cameraDataSet[-1]):
                                self.cameraDataSet.pop()
                                
                        self.cameraData = self.cameraDataSet[-1]
                        
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]

                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                        self._window.display(self._imageObj.getResizedImage(newImage))  

    def UIEnterCameraTranslation(self, key):
        #move left 
        if key == "a":            
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point

            else:
                tempX = self.cameraData[0] - self.TRANSLATION_X_INTERVAL

                if(tempX <= self.MIN_TRANSLATION_X): 
                    print "error"
                    #print error, outside image left boundary

                else:
                    #update current camera position x
                    self.cameraData[0] = tempX

                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]

                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))  

                    self.frameCount += 1            
        #move right     
        elif key == "d":                
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point

            else:
                tempX = self.cameraData[0] + self.TRANSLATION_X_INTERVAL

                if(tempX >= self.MAX_TRANSLATION_X): 
                    print "error"
                    #print error, outside image right boundary

                else:
                    #update current camera position x
                    self.cameraData[0] = tempX

                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]

                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))  

                    self.frameCount += 1      
        #move forward 
        elif key == "w":
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point

            else:
                tempZ = self.cameraData[2] + self.TRANSLATION_Z_INTERVAL

                if(tempZ >= self.MAX_TRANSLATION_Z): 
                    print "error"
                    #print error, outside image z boundary

                else:
                    #update current camera position z
                    self.cameraData[2] = tempZ

                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]

                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))  

                    self.frameCount += 1    
           
        #move backward 
        elif key == "s":
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point

            else:
                tempZ = self.cameraData[2] - self.TRANSLATION_Z_INTERVAL

                if(tempZ <= self.MIN_TRANSLATION_Z): 
                    print "error"
                    #print error, outside image z boundary

                else:
                    #update current camera position z
                    self.cameraData[2] = tempZ

                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]

                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))  

                    self.frameCount += 1    
        
        #move up
        elif key == "r":      
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point

            else:
                tempY = self.cameraData[1] + self.TRANSLATION_Y_INTERVAL

                if(tempY >= self.MAX_TRANSLATION_Y):
                    print "error"
                    #print error, outside image upper boundary

                else:
                    #update current camera position y
                    self.cameraData[1] = tempY

                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]

                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))  

                    self.frameCount += 1
            
        #move down
        elif key == "f":   
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point
                                        
            else:
                tempY = self.cameraData[1] - self.TRANSLATION_Y_INTERVAL

                if(tempY <= self.MIN_TRANSLATION_Y):
                    print "error"
                    #print error, outside image lower boundary
                                        
                else:
                    #update current camera position y
                    self.cameraData[1] = tempY

                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]

                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))  

                    self.frameCount += 1
        
        #rotate left
        elif key == "q":    
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point
                                
            else:
                tempR = self.cameraData[3] - self.ROTATION_INTERVAL

                if(abs(tempR) > self.MAX_ROTATION):
                    print "print something"
                    #print error, rotation exceed MAX_ROTATION 
                                        
                else:
                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]
                                        
                    #get rotation matrix
                    tempCamRotMat = rotByRotMat(tempCamRotMat, self.ROTATION_INTERVAL, 0, 1, 0, 1)
                                        
                    #update current camera rotation degree and matrix
                    self.cameraData[3] = tempR
                    self.cameraData[4] = tempCamRotMat
                                        
                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))
                                        
                    self.frameCount += 1
            
        #rotate right
        elif key == "e":
            if(self.frameCount >= 30):
                print "error"
                #print error, exceed maximum camera point
                
            else:
                tempR = self.cameraData[3] + self.ROTATION_INTERVAL
                if(tempR > self.MAX_ROTATION):
                    print "error"
                    #print error, rotation exceed MAX_ROTATION 
                                        
                else:
                    tempCamPos = self.cameraData[0:3]
                    tempCamRotMat = self.cameraData[4]
                    
                    #get rotation matrix
                    tempCamRotMat = rotByRotMat(tempCamRotMat, self.ROTATION_INTERVAL, 0, 1, 0, 1)
                    
                    #update current camera rotation degree and matrix
                    self.cameraData[3] = tempR
                    self.cameraData[4] = tempCamRotMat
                                        
                    #get image and display
                    newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                    self._window.display(self._imageObj.getResizedImage(newImage))  
                                        
                    self.frameCount += 1    
                                        
        elif key == chr(13):    
            cameraDataSet.append(cameraData)
                  
            
    def UILoadCameraData(self, key):
        print "Loading camera data..."  
                
    def _UIkeyframe(self,key):
        self.WriteMovie()
     
    def Render(self):
                if(self.frameCount > 0):
                        print "Rendering..."
        #interpolate all images in frames[]    
        #call WriteMovie to output avi
        #possible show the video output
        #clean up    
         
    def WriteMovie(self):
        print "Writing Movie..."   
        
        '''Testing frames'''
        imageDir = os.path.join(".", "video")
        images = list()
        
        #H.264 video encoding in avi container, 25fps, resolution = imagewidth x imageheight
        fourcc = cv2.cv.CV_FOURCC('D','I','V','X')
        video  = cv2.VideoWriter('output.avi', fourcc, 25, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT));
        
        #get frames
        for jpgfiles in os.listdir(imageDir):
            if '.jpg' in jpgfiles:
                frame = cv2.imread(os.path.join(imageDir, jpgfiles)) 
                frame = cv2.resize(frame,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
                video.write(frame)
                
    def cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Movie..."               
                
                
                
                
                
                
            
