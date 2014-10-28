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

strWorkingDirectory = "F:\Python\CS4243\Project"
import os
from Polygon import Polygon
from Image import Image
os.system('cls')
os.chdir(strWorkingDirectory)
strRegisteredWorkingDirectory = os.getcwd()
import numpy as np
print("The current Working Directory is \"" + strRegisteredWorkingDirectory +
      "\".\n")
poly = Polygon()
print("\n")
img = Image()
print("\n")

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
print poly.__doc__

#Class Image Documentation.
print img.__doc__

pts = ptsTestSet2()
mat3DScene = pts
ptsRows = pts.shape[0]
ptsColumns = pts.shape[1]
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
matRotatedPoints = poly.rotbyquatmult(arrayInitialPoint, fltTheta, wx, wy, wz,
                                      intIterations)
arrayCamPos1 = arrayInitialPoint
arrayCamPos2 = np.array(matRotatedPoints[0, :])[0].tolist()
arrayCamPos3 = np.array(matRotatedPoints[1, :])[0].tolist()
arrayCamPos4 = np.array(matRotatedPoints[2, :])[0].tolist()

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
quatmat_1 = np.array(np.eye(3))
quatmat_2 = poly.rotbyrotmat(quatmat_1, fltTheta, wx, wy, wz, 1)
quatmat_3 = poly.rotbyrotmat(quatmat_2, fltTheta, wx, wy, wz, 1)
quatmat_4 = poly.rotbyrotmat(quatmat_3, fltTheta, wx, wy, wz, 1)

print("The Camera Orientation at Frame 1 (quatmat_1) is:\n")
print quatmat_1
print("\n")
print("The Camera Orientation at Frame 2 (quatmat_2) is:\n")
print(quatmat_2)
print("\n")
print("The Camera Orientation at Frame 3 (quatmat_3) is:\n")
print(quatmat_3)
print("\n")
print("The Camera Orientation at Frame 4 (quatmat_4) is:\n")
print(quatmat_4)
print("\n")
print("Each Row of the above Matrices represent the X-Axis, Y-Axis and Z-Axis ")
print("Directions respectively.\n")

#===================================================================
#d. Plot the Images for the Perspective Projection for the 4 Frames.
#===================================================================
print("===================================================================")
print("d. Plot the Images for the Perspective Projection for the 4 Frames.")
print("===================================================================")

arrayFr1PersProj = img.persproj(mat3DScene, arrayCamPos1, quatmat_1)
arrayFr2PersProj = img.persproj(mat3DScene, arrayCamPos2, quatmat_2)
arrayFr3PersProj = img.persproj(mat3DScene, arrayCamPos3, quatmat_3)
arrayFr4PersProj = img.persproj(mat3DScene, arrayCamPos4, quatmat_4)
strPlotTitle = "Perspective Projection"
img.plotproj(strPlotTitle, arrayFr1PersProj, arrayFr2PersProj, arrayFr3PersProj,
             arrayFr4PersProj)
print("\n")

