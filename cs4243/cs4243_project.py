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
1.0.0     26/10/2014   Dave Tan     Initial Version to test Polygon and Image
                                    Classes.
1.1.0     02/11/2014   Dave Tan     Updated Method Names due to changes in
                                    Polygon Class. Include Method Invocation by
                                    using Polygon._rotByImage. Converted Screen
                                    Prints to Verbose Outputs.
1.2.0     04/11/2014   Dave Tan     Introduced Options for displaying of Camera
                                    Translations and Rotations.
          05/11/2014   Dave Tan     Introduced codes to test Vectorised
                                    Rotation.
"""

def ptsTestSet1():
    """
    =====================
    Function ptsTestSet1.
    =====================
    =========
    Sypnosis.
    =========
    This Function returns the original 11 x 3 Set of Points.
    """

    #===============
    #Initialisation.
    #===============
    pts = np.zeros([11, 3])

    #=======================
    #Populate the 3D Points.
    #=======================
    pts[0, :] = [-1, -1, -1]
    pts[1, :] = [1, -1, -1]
    pts[2, :] = [1, 1, -1]
    pts[3, :] = [-1, 1, -1]
    pts[4, :] = [-1, -1, 1]
    pts[5, :] = [1, -1, 1]
    pts[6, :] = [1, 1, 1]
    pts[7, :] = [-1, 1, 1]
    pts[8, :] = [-0.5, -0.5, -1]
    pts[9, :] = [0.5, -0.5, -1]
    pts[10, :] = [0, 0.5, -1]

    #===================
    #return the Results.
    #===================
    return pts

def ptsTestSet2():
    """
    =====================
    Function ptsTestSet2.
    =====================
    =========
    Sypnosis.
    =========
    This Function returns introduces Cube and Triangle Wireframes to the
    Original Points referenced from Assignment 3.
    """

    def c8intpts(pt1, pt2, granularity):
        #===============
        #Initialisation.
        #===============
        new_pts = []

        #===============
        #Compute Vector.
        #===============
        vector = np.array([(x[0] - x[1]) for x in zip(pt1, pt2)])

        #==============================
        #Return the Granularised Array.
        #==============================
        return[(np.array(pt2) + (vector * (float(i) / granularity))) \
               for i in range(1, granularity)]

    #===============
    #Initialisation.
    #===============
    pts = []
    granularity = 20

    #======================
    #Create Cube Wireframe.
    #======================
    pts.extend([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], \
              [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]])

    pts.extend(c8intpts([-1, -1, 1], [1, -1, 1], granularity))
    pts.extend(c8intpts([1, -1, 1], [1, 1, 1], granularity))
    pts.extend(c8intpts([1, 1, 1], [-1, 1, 1], granularity))
    pts.extend(c8intpts([-1, 1, 1], [-1, -1, 1], granularity))
    
    pts.extend(c8intpts([-1, -1, -1], [1, -1, -1], granularity))
    pts.extend(c8intpts([1, -1, -1], [1, 1, -1], granularity))
    pts.extend(c8intpts([1, 1, -1], [-1, 1, -1], granularity))
    pts.extend(c8intpts([-1, 1, -1], [-1, -1, -1], granularity))

    pts.extend(c8intpts([1, 1, 1], [1, 1, -1], granularity))
    pts.extend(c8intpts([1, -1, 1], [1, -1, -1], granularity))
    pts.extend(c8intpts([-1, -1, 1], [-1, -1, -1], granularity))
    pts.extend(c8intpts([-1, 1, 1], [-1, 1, -1], granularity))

    #==========================
    #Create Triangle Wireframe.
    #==========================
    pts.extend([[-0.5, -0.5, -1], [0.5, -0.5, -1], [0, 0.5, -1]])
    pts.extend(c8intpts([-0.5, -0.5, -1], [0.5, -0.5, -1], granularity))
    pts.extend(c8intpts([0.5, -0.5, -1], [0, 0.5, -1], granularity))
    pts.extend(c8intpts([0, 0.5, -1], [-0.5, -0.5, -1], granularity))

    #==============================
    #Return the Granularised Array.
    #==============================
    return np.array(pts)

#===============================
#1. Set the Working Directories.
#===============================
print("===============================")
print("1. Set the Working Directories.")
print("===============================")

#==================
#a. Initialisation.
#==================
print("==================")
print("a. Initialisation.")
print("==================")

strWorkingDirectory = "F:\Python\CS4243\Project\CS4243_v2.0.1_Dave"
import os
from polygon import Polygon
os.system('cls')
os.chdir(strWorkingDirectory)
strRegisteredWorkingDirectory = os.getcwd()
import numpy as np
import cv2
booVerbose = False
booTestMode = True
booDisplayCamTrans = False
booDisplayCamOrient = False
booPlotPersProj = False
print("The current Working Directory is \"" + strRegisteredWorkingDirectory +
      "\".\n")
strImageFileName = "project.jpeg"
print("\n")
print("\n")

if __name__== "__main__":
    import image, projectwindow
    window = projectwindow.ProjectWindow()
    img = image.Image(window, strImageFileName)
    poly = Polygon(window, img)
    #window.display()
    cv2.waitKey(0)

#=========
#2. Tests.
#=========
print("=========")
print("2. Tests.")
print("=========")

#==================
#a. Initialisation.
#==================
print("==================")
print("a. Initialisation.")
print("==================")

#Class Polygon Documentation.
#print poly.__doc__

#Class Image Documentation.
#print img.__doc__

pts = ptsTestSet2()
mat3DScene = pts
ptsRows = pts.shape[0]
ptsColumns = pts.shape[1]

#Test 8 x 3 Matrix as List of 3D Scene Points.
mat3DScenePoints = np.matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
matOnes = np.matrix(np.ones([3, 3]))
matRotatedPoints = mat3DScenePoints * matOnes

#Test Flat 3D Scene Points List.
fltTheta = -30
wx = 0
wy = 1
wz = 0
#img.getFlat3DPoints()

#Calculate Time Elapsed.
import time
intStart = time.time()

print "Original 3D Scene Points:\n"
print img._flat_3dpoints
print "\n"
img._flat_3dpoints_new = poly._rotByImage(img, fltTheta, wx, wy, wz)
intEnd = time.time()
print "Rotated 3D Scene Points:\n"
print img._flat_3dpoints_new
print "\n"
print "Dimensions of the Array of Rotated Points is:\n"
print img._flat_3dpoints_new.shape
print "\n"
print "Original 3D Scene Points Height (Rows) is: "
print img.getHeight()
print "\n"
print "Original 3D Scene Points Width (Columns) is: "
print img.getWidth()
print "\n"
print "The Product of Height and Width = # Pixels is:"
print img.getHeight() * img.getWidth()
print "\n"
print "The Time Elapsed to perform the Rotation of " \
      + str(img.getHeight() * img.getWidth()) + " Pixels is: " \
      + str(intEnd - intStart) + " Seconds.\n"

strFigureTitle = "Camera Translation"

#Test 3D Scene Flat Structure.
test = np.zeros((2, 2, 3))
test[0, 0] = [1, 1, 1]
test[0, 1] = [2, 2, 2]
test[1, 0] = [3, 3, 3]
test[1, 1] = [4, 4, 4]
test2 = test.ravel()

if(booTestMode):
    #==========
    #Test Mode.
    #==========
    print "mat3DScenePoints is:\n"
    print mat3DScenePoints
    print "\n"
    print "matOnes is:\n"
    print matOnes
    print "\n"
    print "matRotatedPoints is:\n"
    print matRotatedPoints
    print "\n"

if(booVerbose):
    #=============
    #Verbose Mode.
    #=============
    print("pts is:\n")
    print(pts)
    print("\n")
    print("The Number of Rows and Columns of the \"" + "pts" + "\" Array are:\n")
    print(str(ptsRows) + " Rows, " + str(ptsColumns) + " Columns.\n")
    print("\n")

#====================
#b. Camera Locations.
#====================
print("====================")
print("b. Camera Locations.")
print("====================")

#Camera Locations.
arrayInitialPoint = [0, 0, -5]
fltTheta = -30
wx = 0
wy = 1
wz = 0
intIterations = 3

#Compute Camera Locations.
matRotatedPoints = poly._rotByQuatMult(arrayInitialPoint, fltTheta, wx, wy, wz,
                                      intIterations)
arrayCamPos1 = arrayInitialPoint
arrayCamPos2 = np.array(matRotatedPoints[0, :])[0].tolist()
arrayCamPos3 = np.array(matRotatedPoints[1, :])[0].tolist()
arrayCamPos4 = np.array(matRotatedPoints[2, :])[0].tolist()
matRotatedPoints = np.append(arrayInitialPoint, matRotatedPoints)

if(booVerbose):
    #=============
    #Verbose Mode.
    #=============
    print("The Camera Position at Frame 1 is:\n")
    print arrayCamPos1
    print("\n")
    print("The Camera Position at Frame 2 is:\n")
    print(arrayCamPos2)
    print("\n")
    print("The Camera Position at Frame 3 is:\n")
    print(arrayCamPos3)
    print("\n")
    print("The Camera Position at Frame 4 is:\n")
    print(arrayCamPos4)
    print("\n")

#Display Camera Translations.
if(booDisplayCamTrans):
    #============================
    #Display Camera Translations.
    #============================
    img.dispCamTrans(matRotatedPoints, strFigureTitle)

print("\n")

#=======================
#c. Camera Orientations.
#=======================
print("=======================")
print("c. Camera Orientations.")
print("=======================")

from numpy.linalg import inv
fltTheta = -30
wx = 0
wy = 1
wz = 0

#Compute Camera Orientations.
CamOrient1 = np.array(np.eye(3))
CamOrient2 = poly._rotByRotMat(CamOrient1, fltTheta, wx, wy, wz, 1)
CamOrient3 = poly._rotByRotMat(CamOrient2, fltTheta, wx, wy, wz, 1)
CamOrient4 = poly._rotByRotMat(CamOrient3, fltTheta, wx, wy, wz, 1)

#Display Camera Orientations.
if(booDisplayCamOrient):
    #============================
    #Display Camera Orientations.
    #============================
    strFigureTitle1 = "Camera Orientation 1"
    img.dispCamOrient(CamOrient1, strFigureTitle1)
    strFigureTitle2 = "Camera Orientation 2"
    img.dispCamOrient(CamOrient2, strFigureTitle2)
    strFigureTitle3 = "Camera Orientation 3"
    img.dispCamOrient(CamOrient3, strFigureTitle3)
    strFigureTitle4 = "Camera Orientation 4"
    img.dispCamOrient(CamOrient4, strFigureTitle4)

if(booVerbose):
    #=============
    #Verbose Mode.
    #=============
    print("The Camera Orientation at Frame 1 (quatmat_1) is:\n")
    print CamOrient1
    print("\n")
    print("The Camera Orientation at Frame 2 (quatmat_2) is:\n")
    print(CamOrient2)
    print("\n")
    print("The Camera Orientation at Frame 3 (quatmat_3) is:\n")
    print(CamOrient3)
    print("\n")
    print("The Camera Orientation at Frame 4 (quatmat_4) is:\n")
    print(CamOrient4)
    print("\n")
    print("Each Row of the above Matrices represent the X-Axis, Y-Axis and Z-Axis ")
    print("Directions respectively.\n")

print("\n")

#===================================================================
#d. Plot the Images for the Perspective Projection for the 4 Frames.
#===================================================================
print("===================================================================")
print("d. Plot the Images for the Perspective Projection for the 4 Frames.")
print("===================================================================")

arrayFr1PersProj = img.persProj(mat3DScene, arrayCamPos1, CamOrient1)
arrayFr2PersProj = img.persProj(mat3DScene, arrayCamPos2, CamOrient2)
arrayFr3PersProj = img.persProj(mat3DScene, arrayCamPos3, CamOrient3)
arrayFr4PersProj = img.persProj(mat3DScene, arrayCamPos4, CamOrient4)
strPlotTitle = "Perspective Projection"

if(booPlotPersProj):
    #=============================
    #Plot Perspective Projections.
    #=============================
    img.plotProj(strPlotTitle, arrayFr1PersProj, arrayFr2PersProj,
                 arrayFr3PersProj, arrayFr4PersProj)
    print("\n")

