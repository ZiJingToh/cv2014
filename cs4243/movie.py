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
        self.focal = 700

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
                                "k":self._UIRender}

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
        self._orient = np.eye(3)
        #x,y,z,rotdegree,rotmat
        self.INITIALCAMERADATA = [self.IMAGE_WIDTH/2, self.IMAGE_HEIGHT/2, 0, 0, np.identity(3)]
        
        #DIVX video encoding in avi container, 25fps, resolution = imagewidth x imageheight
        fourcc = cv2.cv.CV_FOURCC('D','I','V','X')
        self._video  = cv2.VideoWriter('output.avi', fourcc, 25, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT));
        
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

            newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
            self._window.display(self._imageObj.getResizedImage(newImage))
        else:
             print "No frame to delete"

    def UIEnterCameraTranslation(self, key): 
        #move left 
        if key == "a":
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
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))
        #move right     
        elif key == "d":                
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
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))
        #move forward 
        elif key == "w":
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
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))

        #move backward 
        elif key == "s":
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
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))
        #move up
        elif key == "r":      
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
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))  
        #move down
        elif key == "f":   
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
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))  

        #rotate left
        elif key == "q":    
            tempR = self.cameraData[3] - self.ROTATION_INTERVAL

            if(abs(tempR) > self.MAX_ROTATION):
                print "print something"
                #print error, rotation exceed MAX_ROTATION 
                                    
            else:
                tempCamPos = self.cameraData[0:3]
                tempCamRotMat = self.cameraData[4]
                                    
                #get rotation matrix
                tempCamRotMat = self._imageObj._rotByRotMat(tempCamRotMat, -self.ROTATION_INTERVAL, 0, 1, 0, 1)
                                    
                #update current camera rotation degree and matrix
                self.cameraData[3] = tempR
                self.cameraData[4] = tempCamRotMat
                                    
                #get image and display
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))
            
        #rotate right
        elif key == "e":
            tempR = self.cameraData[3] + self.ROTATION_INTERVAL
            if(tempR > self.MAX_ROTATION):
                print "error"
                #print error, rotation exceed MAX_ROTATION 
            else:
                tempCamPos = self.cameraData[0:3]
                tempCamRotMat = self.cameraData[4]
                
                #get rotation matrix
                tempCamRotMat = self._imageObj._rotByRotMat(tempCamRotMat, self.ROTATION_INTERVAL, 0, 1, 0, 1)
                
                #update current camera rotation degree and matrix
                self.cameraData[3] = tempR
                self.cameraData[4] = tempCamRotMat
                                    
                #get image and display
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                self._window.display(self._imageObj.getResizedImage(newImage))                                         
        elif key == chr(13):
            if(self.frameCount >= 30):
                print "error exceeding frame 30"
                #print error, exceed maximum camera point
                    
            else:        
                self.cameraDataSet.append(self.cameraData)
                self.frameCount += 1                  
            
    def UILoadCameraData(self, key):
        print "Loading camera data..."  
                
    def _UIkeyframe(self,key):
        self.WriteMovie()
     
    def _UIRender(self, key):
        if(self.frameCount > 0):
            print "Rendering..."
            xframe = 0
            while xframe != self.frameCount:
                camdata = self.cameraDataSet[xframe]
                tempCamPos = camdata[0:3]
                tempCamRotMat = camdata[4]
                
                #get rotation matrix
                tempCamRotMat = self._imageObj._rotByRotMat(tempCamRotMat, self.ROTATION_INTERVAL, 0, 1, 0, 1)
                
                #update current camera rotation degree and matrix
                self.cameraData[3] = camdata[3]
                self.cameraData[4] = tempCamRotMat
                                    
                #get image and display
                newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.focal)
                newImage = cv2.resize(newImage,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
                self._video.write(newImage)
        #interpolate all images in frames[]    
        #call WriteMovie to output avi
        #possible show the video output
        #clean up
        else:
            print "No frame to render"
         
    def WriteMovie(self,):
        print "Writing Movie..."   
        
        '''Testing frames'''
        imageDir = os.path.join(".", "video")
        images = list()
        
        #get frames
        for jpgfiles in os.listdir(imageDir):
        
            if '.jpg' in jpgfiles:
                frame = cv2.imread(os.path.join(imageDir, jpgfiles)) 
                frame = cv2.resize(frame,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
                self._video.write(frame)
                
    def cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Movie..."               
                
                
                
                
                
                
            
