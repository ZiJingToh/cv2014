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
1.0.0     01/11/2014   Toh Zijing   Added new Class InputModeHandler.
"""

#===============
#Initialisation.
#===============
from inputmodehandler import InputModeHandler
import numpy as np


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
        self.rotationMat = np.identity(3)   #3x3 
        
        # mouse event callback of the form
        # { (EVENT, FLAGS):callback(x, y) }
        self._mouseEvents = {}

        # keyboard event callback of the form
        # { keychar:callback(key) }
        self._keyboardEvents = {"a":self.UIEnterCameraMovement,      #left
                                "d":self.UIEnterCameraMovement,     #right
                                "w":self.UIEnterCameraMovement,     #forward
                                "s":self.UIEnterCameraMovement,     #backward
                                "r":self.UIEnterCameraMovement,     #up
                                "f":self.UIEnterCameraMovement,     #down
                                "q":self.UIEnterCameraMovement,        #rotate left
                                "e":self.UIEnterCameraMovement,        #roate right
                                chr(127):self.UIDeleteLastData,        #delete key
                                chr(13):self.UIEnterCameraMovement,        #enter key
                                "c":self.ClearSetPoints,               #clear all camera position
                                "l":self.UILoadCameraData,             #load predefined camera positions
                                "k":self._UIkeyframe}

        self.IMAGE_WIDTH = self._imageObj.getWidth()
        self.IMAGE_HEIGHT = self._imageObj.getHeight()
          
        #define camera movement interval
        self.TRANSLATION_X_INTERVAL = self.IMAGE_WIDTH/10     
        self.TRANSLATION_Y_INTERVAL = self.IMAGE_HEIGHT/10
        self.TRANSLATION_Z_INTERVAL = 1
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
        self.MAX_TRANSLATION_Z = -1
        self.MAX_TRANSLATION_Z = 9    
        self.MAX_ROTATION = 60          #degree

        self.INITIALCAMERADATA = [self.IMAGE_WIDTH/2, self.IMAGE_HEIGHT/2, 0, np.identity(3)]
        self.ClearSetPoints()

    def _UIkeyframe(self, key):
        print "_UIkeyframe"

    def ClearSetPoints(self, key=None):
        """
        Clears camera position and orientation set, initialize camera pos to (w/2,h/2,0) and camera orientation to identity matrix
        """
        self.cameraData = self.INITIALCAMERADATA
        self.cameraDataSet = []
        self.cameraDataSet.append(self.cameraData)
        
    def UIDeleteLastData(self, key):
        if len(self.cameraDataSet) > 0:
            self.cameraDataSet.pop()
            if len(self.cameraDataSet) > 0:
                self.cameraData = self.cameraDataSet[-1]
            else:
                self.cameraData = self.INITIALCAMERADATA

    def UIEnterCameraMovement(self, key):
        if key == "a":
            tempX = self.cameraData[0] - self.TRANSLATION_X_INTERVAL
            if(tempX) <= self.MIN_TRANSLATION_X: #outside image left boundary
                print "print something"
            else:
                self.cameraData[0] = tempX
                #print info
            
        elif key == "d":
            tempX = self.cameraData[0] + self.TRANSLATION_X_INTERVAL
            if(tempX) >= self.MAX_TRANSLATION_X: #outside image right boundary
                print "print something"
            else:
                self.cameraData[0] = tempX
                #print info
        
        elif key == "w":
            tempZ = self.cameraData[2] + self.TRANSLATION_Z_INTERVAL
            if(tempZ) >= self.MAX_TRANSLATION_Z: #outside image z boundary
                print "print something"
            else:
                self.cameraData[2] = tempZ
                #print info
            
        elif key == "s":
            tempZ = self.cameraData[2] - self.TRANSLATION_Z_INTERVAL
            if(tempZ) <= self.MAX_TRANSLATION_Z: #outside image z boundary
                print "print something"
            else:
                self.cameraData[2] = tempZ
                #print info
        
        elif key == "r":    
            tempY = self.cameraData[1] + self.TRANSLATION_Y_INTERVAL
            if(tempY) >= self.MAX_TRANSLATION_Y: #outside image upper boundary
                print "print something"
            else:
                self.cameraData[1] = tempY
                #print info
            
        elif key == "f":
            tempY = self.cameraData[1] - self.TRANSLATION_Y_INTERVAL
            if(tempY) <= self.MIN_TRANSLATION_Y: #outside image lower boundary
                print "print something"
            else:
                self.cameraData[1] = tempY
                #print info
        
        elif key == "q":    
            print "print something"
            #convert cameraData[2] to degree, how?
            #add self.ROTATION_INTERVAL to it, then compare to maxrotation
            #if smaller, convert it back to rotmat, and replace cameraData[2]
            
        elif key == "e":
            print "print something"
            
        elif key == chr(13):    
            if len(cameraDataSet) < 30:
                cameraDataSet.append(cameraData)
        
                
    def UILoadCameraData(self, key):
        print "Loading camera data..."  
                
    def WriteMovie(self):
        print "Writing Movie..."   
        
        #H.264 video encoding in avi container, 25fps, resolution = imagewidth x imageheight
        fourcc = cv.CV_FOURCC('H','2','6','4')
        video  = cv2.VideoWriter('output.avi', fourcc, 25, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT));
        
        #get frames
        
        #while still has frame
        #   video.write(frane)
                
    def Cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Movie..."               
                
                
                
                
                
                
            
