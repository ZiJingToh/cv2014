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
4.0.0     15/11/2014   Toh ZiJing   Added image display mode toggle.
4.1.0     15/11/2014   Dave Tan     Added new Method plotCFCamPosAndOrient.
                                    Invoked plotCFCamPosAndOrient Method to plot
                                    both Camera Location and Camera Orientation
                                    when the ENTER Key, i.e Chr(13) is pressed.
"""

#===============
#Initialisation.
#===============
from inputmodehandler import InputModeHandler
import numpy as np
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

        # keyboard event callback of the form
        # { keychar:callback(key) }
        self._keyboardEvents = {"a":self.UIEnterCameraMovement,     	#left
                                "d":self.UIEnterCameraMovement,     	#right
                                "w":self.UIEnterCameraMovement,     	#forward
                                "s":self.UIEnterCameraMovement,     	#backward
                                "r":self.UIEnterCameraMovement,     	#up
                                "f":self.UIEnterCameraMovement,     	#down
                                "q":self.UIEnterCameraMovement,       	#rotate left
                                "e":self.UIEnterCameraMovement,        	#roate right
                                chr(127):self.UIDeleteLastData,        	#delete key
                                chr(13):self.UIEnterCameraMovement,    	#enter key
                                "c":self.ClearSetPoints,               	#clear all camera position
                                "l":self.UILoadCameraData,             	#load predefined camera positions
                                "o":self.Render,			#render
                                "p":self.toggleImageMode}


        #global constant
        #define image resolution
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
        
        #define maximum frame allowed and focal length
        self.MAX_FRAME = 30
        self.FOCAL = 700

        #initialize global variables
        self.INITIALCAMERADATA = [self.IMAGE_WIDTH/2, self.IMAGE_HEIGHT/2, 300, 0, np.identity(3)]  #x,y,z,rotdegree,rotmat
        
        self.cameraDataSet = []                             #vector of vector (x,y,z,r,(3x3))
        self.cameraData = self.INITIALCAMERADATA[:]          #vector (x,y,z,r,(3x3))
        self.cameraDataSet.append(self.INITIALCAMERADATA[:])
        
        self.frames = []
        self.frameCount = 0
        self.interpFrameCount = 0
        
        tempCamPos = self.cameraData[0:3]
        tempCamRotMat = self.cameraData[4]
        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
        self._window.display(self._imageObj.getResizedImage(newImage))
        
        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])

    def toggleImageMode(self, key):
        self._imageObj.toggleImageMode()
        newImage = self._imageObj.getImageFromCam(self.cameraData[0:3],
                                                  self.cameraData[4],
                                                  self.FOCAL)
        self._window.display(self._imageObj.getResizedImage(newImage))   

    def ClearSetPoints(self, key=None):
        print "In ClearSetPoints"

        self.cameraData = self.INITIALCAMERADATA[:]
        self.cameraDataSet = []
        self.cameraDataSet.append(self.cameraData[:])
        self.frameCount = 0
        self.interpFrameCount = 0   
        
        tempCamPos = self.cameraData[0:3]
        tempCamRotMat = self.cameraData[4]
            
        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
        self._window.display(self._imageObj.getResizedImage(newImage))   
            
        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
        
    #revert to last saved point, cannot revert to last unsaved point
    def UIDeleteLastData(self, key):
        print "In UIDeleteLastData"
        
        if(self.cameraData[0] == self.INITIALCAMERADATA[0]) and (self.cameraData[1] == self.INITIALCAMERADATA[1]) and (self.cameraData[2] == self.INITIALCAMERADATA[2]) and (self.cameraData[3] == self.INITIALCAMERADATA[3]):
            print "No frame to delete"
            
        else:
			#revert to last saved point
            print "Delete point"
            if(self.cameraData == self.cameraDataSet[-1]):
                self.cameraDataSet.pop()
                self.frameCount -= 1
				
            self.cameraData = (self.cameraDataSet[-1])[:]
			
            tempCamPos = self.cameraData[0:3]
            tempCamRotMat = self.cameraData[4]

            newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
            self._window.display(self._imageObj.getResizedImage(newImage))	
            
            self.interpFrameCount = 0
            
            print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
            print "frameCount : ", self.frameCount


    def UIEnterCameraMovement(self, key): 
        print "In EnterCameraMovement"
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
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[0] = tempX
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                    
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
					   
                    else:
                        #update current camera position x
                        self.cameraData[0] = tempX
					
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))	
                        print "Update camera data x: {}".format(self.TRANSLATION_X_INTERVAL*-1)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
                        	        
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
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[0] = tempX
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                    print "Interpolated frame count: self.interpFrameCount"
                        
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
                        
                    else:
					    #update current camera position x
                        self.cameraData[0] = tempX
                        
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))	  
                        print "Update camera data x: {}".format(self.TRANSLATION_X_INTERVAL)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
                        
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
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[2] = tempZ
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                        
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
                        
                    else:
					    #update current camera position z
                        self.cameraData[2] = tempZ
					
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))	
                        print "Update camera data z: {}".format(self.TRANSLATION_Z_INTERVAL)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
           
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
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[2] = tempZ
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                        
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
                        
                    else:
					    #update current camera position z
                        self.cameraData[2] = tempZ
					
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))	
                        
                        print "Update camera data z: {}".format(self.TRANSLATION_Z_INTERVAL*-1)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
        
        #move up
        elif key == "f":      
            if(self.frameCount >= 30):
                print "error"
				#print error, exceed maximum camera point
					
            else:
                tempY = self.cameraData[1] + self.TRANSLATION_Y_INTERVAL

                if(tempY >= self.MAX_TRANSLATION_Y):
					print "error"
					#print error, outside image upper boundary
					
                else:
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[1] = tempY
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                        
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
                        
                    else:
					    #update current camera position y
                        self.cameraData[1] = tempY
					
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))	
                        
                        print "Update camera data y: {}".format(self.TRANSLATION_Y_INTERVAL)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
            
        #move down
        elif key == "r":   
            if(self.frameCount >= 30):
                print "error"
				#print error, exceed maximum camera point
					
            else:
                tempY = self.cameraData[1] - self.TRANSLATION_Y_INTERVAL

                if(tempY <= self.MIN_TRANSLATION_Y):
					print "error"
					#print error, outside image lower boundary
					
                else:
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[1] = tempY
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                        
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
                        
                    else:
					    #update current camera position y
                        self.cameraData[1] = tempY
					
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))	
                        
                        print "Update camera data y: {}".format(self.TRANSLATION_Y_INTERVAL*-1)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
        
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
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[3] = tempR
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                        
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
                        
                    else:
                        print "Update camera data r"
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get rotation matrix
                        tempCamRotMat = self._imageObj._rotByRotMat(tempCamRotMat, (self.ROTATION_INTERVAL * -1), 0, 1, 0, 1)
					
					    #update current camera rotation degree and matrix
                        self.cameraData[3] = tempR
                        self.cameraData[4] = tempCamRotMat
					
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))
                        
                        print "Update camera data r: {}".format(self.ROTATION_INTERVAL*-1)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
            
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
                    #get interpolated framecount between current point and last saved point
                    tempCamData = self.cameraData
                    tempCamData[3] = tempR
                    fc = self.GetInterpolatedFrameCount(tempCamData, self.cameraDataSet[-1])
                    self.interpFrameCount = fc[0]
                        
                    if(self.interpFrameCount + self.frameCount > 30):
            			print "error"
            		    #print error, exceed maximum camera point
                        
                    else:
                        print "Update camera data r"
                        tempCamPos = self.cameraData[0:3]
                        tempCamRotMat = self.cameraData[4]
					
					    #get rotation matrix
                        tempCamRotMat = self._imageObj._rotByRotMat(tempCamRotMat, self.ROTATION_INTERVAL, 0, 1, 0, 1)
					
					    #update current camera rotation degree and matrix
                        self.cameraData[3] = tempR
                        self.cameraData[4] = tempCamRotMat
					    
					    #get image and display
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, self.FOCAL)
                        self._window.display(self._imageObj.getResizedImage(newImage))	
                        
                        print "Update camera data r: {}".format(self.ROTATION_INTERVAL)
                        print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
		
        elif key == chr(13):    
            print ""
            print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])
            print "Last saved point: ({} {} {} {})".format((self.cameraDataSet[-1])[0],
                                                            (self.cameraDataSet[-1])[1],
                                                            (self.cameraDataSet[-1])[2],
                                                            (self.cameraDataSet[-1])[3])
            lastSavedPoint = self.cameraDataSet[-1]                                            
            if (self.cameraData[0] != lastSavedPoint[0]) or (self.cameraData[1] != lastSavedPoint[1]) or (self.cameraData[2] != lastSavedPoint[2]) or (self.cameraData[3] != lastSavedPoint[3]): 

                tempCamData = self.cameraData[:]
                self.cameraDataSet.append(tempCamData)
            
                self.frameCount += self.interpFrameCount
                self.interpFrameCount = 0
            
                print "Camera data saved"
                print "Current point: ({} {} {} {})".format(self.cameraData[0],self.cameraData[1],self.cameraData[2],self.cameraData[3])

            #Plot the Current Frame's Camera Location and Orientation.
            self.plotCFCamPosAndOrient(self.cameraData[0:3], self.cameraData[4])
                  
    def UILoadCameraData(self, key=None):
        print "In UILoadCameraData"  
     
    def Render(self, key=None):
        print "In Render"
        if(self.frameCount > 0):
            print "Rendering..."
        
            count = 0
        
            for currPoint in self.cameraDataSet:
                if(count != 0):
                    prevPoint = self.cameraDataSet[count-1]
                
                    print "currpoint: ",currPoint
                    print "prevpoint:",prevPoint
                
                    fc = self.GetInterpolatedFrameCount(currPoint, prevPoint)
                    interpFrameCount = fc[0]
                    
                    print "interpFrameCount: ",interpFrameCount
                    
                    interval = 0
                
                    if(fc[1] == True):
                        interval = self.TRANSLATION_X_INTERPOLATION
                    else:
                        interval = self.ROTATION_INTERPOLATION
                    
                    print "interval: ",interval
                    
                    totalFrame = interpFrameCount * interval + 1
                    
                    for i in range(totalFrame):
                        print"count :", i
                        deltaX = float(currPoint[0]) - float(prevPoint[0])
                        deltaY = float(currPoint[1]) - float(prevPoint[1])
                        deltaZ = float(currPoint[2]) - float(prevPoint[2])
                        detaR = float(currPoint[3]) - float(prevPoint[3])
                        
                        tempX =  float(prevPoint[0]) + (deltaX / (totalFrame - 1)) * i
                        tempY =  float(prevPoint[1]) + (deltaY / (totalFrame - 1)) * i
                        tempZ =  float(prevPoint[2]) + (deltaZ / (totalFrame - 1)) * i
                        rotDegree = (detaR / (totalFrame - 1)) * i
                        
                        tempCamPos = [tempX,tempY,tempZ]
                        tempCamRotMat = self._imageObj._rotByRotMat(prevPoint[4], rotDegree, 0, 1, 0, 1)
                    
                        print "tempCamPos: ",tempCamPos
                        print "rotDegree:",rotDegree
                        print "tempCamRotMat:",tempCamRotMat
                        
                        newImage = self._imageObj.getImageFromCam(tempCamPos, tempCamRotMat, 500)
                        newImage = cv2.resize(newImage,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
                        self.frames.append(newImage)
                        
                count += 1
            
            #write output
            self.WriteMovie()
         
    def WriteMovie(self):
        print "Writing Movie..."   
        
        #mp4 video encoding in avi container, 25fps, resolution = imagewidth x imageheight
        fourcc = cv2.cv.CV_FOURCC('m','p','4','v')
        video = cv2.VideoWriter('output.avi', fourcc, 25, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))

        for frame in self.frames:
            video.write(frame)
                   
        video.release()
        print "Done"  
        
    def GetInterpolatedFrameCount(self, currentPoint, prevPoint):
        deltaX = abs(currentPoint[0] - prevPoint[0])
        deltaY = abs(currentPoint[1] - prevPoint[1])
        deltaZ = abs(currentPoint[2] - prevPoint[2])
        deltaR = abs(currentPoint[3] - prevPoint[3])
        
        frameCountX = deltaX/self.TRANSLATION_X_INTERVAL
        frameCountY = deltaY/self.TRANSLATION_Y_INTERVAL
        frameCountZ = deltaZ/self.TRANSLATION_Z_INTERVAL
        frameCountR = deltaR/self.ROTATION_INTERVAL
        
        maxFrameCountXYZ = max(frameCountX, frameCountY, frameCountZ)
        
        if(maxFrameCountXYZ > frameCountR):
            return [maxFrameCountXYZ,True]
        
        else:
            return [frameCountR,False]

    def plotCFCamPosAndOrient(self, arrayCFCamTrans, arrayCFCamOrient):
        #Initialisation.
        intxMin = -2000
        intxMax = 2000
        intyMin = -2000
        intyMax = 2000
        intzMin = -1000
        intzMax = 1000
        strCamTransFigTitle = "Current Captured Frame's\n" + "Camera Location" \
                              + " at Point: (" + str(arrayCFCamTrans[0]) \
                              + ", " + str(arrayCFCamTrans[1]) + ", " \
                              + str(arrayCFCamTrans[2]) + ")"
        strCamOrientFigTitle = "Current Captured Frame's Camera Orientation"

        #Plot the Current Frame's Camera Position and Orientation.
        self._imageObj.plotCamTransAndOrient(arrayCFCamTrans,
                                             strCamTransFigTitle,
                                             arrayCFCamOrient,
                                             strCamOrientFigTitle, intxMin,
                                             intxMax, intyMin, intyMax, intzMin,
                                             intzMax)

    def cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Movie..."               
                
                
                
                
                
                
            
