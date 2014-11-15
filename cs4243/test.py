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
1.0.0     07/11/2014   Dave Tan     Added new Class Test. Moved the following
                                    Test Functions in "cs4243_project.py" and
                                    implemented as new Methods in Class Test:
                                    ptsTestSet1 -> getTestSet1; ptsTestSet2 ->
                                    getTestSet2. Moved 8 x 3 Array to a new
                                    getTestSet3 Method. Moved all Testing Codes
                                    for testing Cube and Triangle Wireframe into
                                    new Method performTestScenario1. Moved small
                                    Test Set mirroring Image Class
                                    Image._image_points Data Structure to a new
                                    Instance Attribute self._matSmallTestSet.
                                    Moved all other Testing Codes for testing
                                    Vectorisation and Optimisation into new
                                    Method performTestScenario2.
                                    Added new Methods: getWorkingDirectory,
                                    get3DSceneHeight, get3DSceneWidth,
                                    getSmallTestSetHeight, getSmallTestSetWidth,
                                    showPolygonClassSypnosis,
                                    showImageClassSypnosis,
                                    turnOnAllDisplayOptions,
                                    turnOffAllDisplayOptions, disp3DScenePoints,
                                    dispSmallTestSetPoints, performSelectedTest,
                                    cleanup.
1.1.0     09/11/2014   Dave Tan     Updated Test Class Sypnosis.
4.1.0     15/11/2014   Dave Tan     Changed Method Invocation for the following
                                    Methods due to their move to Image Class:
                                    _rotByQuatMult, _rotByRotMat in
                                    performTestScenario1 Method; _rotByImage,
                                    _rotByQuatMult and _rotByRotMat in
                                    performTestScenario2 Method. Changed Method
                                    Invocation from persProj2 to persProj due to
                                    rename of persProj2 back to persProj in
                                    Image Class in both performTestScenario1 and
                                    performTestScenario2 Methods. Added Boolean
                                    Argument in dispCamTrans Invocation in
                                    performTestScenario1 Method to annotate on
                                    each Frame Basis.
"""

#===============
#Initialisation.
#===============
import os
from polygon import Polygon
import numpy as np
import cv2
#from numpy.linalg import inv

class Test():
    """
    ***********
    Class Test.
    ***********
    =========
    Sypnosis.
    =========
    This is a Class representing the Test Object to be used for any kind of
    tests to build the Methods of the various Classes. This Class is not part of
    the Production Code used in the actual routines but rather a separate set
    used for testing and validation.

    ========
    Methods.
    ========
    __init__: This is the Constructor Method for Class Image.

    getWorkingDirectory: This Method sets and prints the Current Working
    Directory.
    
    getTestSet1: This Method sets the 3D Scene Points with an arbitrary 11 x 3
    Set of Points.

    getTestSet2: This Method sets the 3D Scene Points with a Cube Wireframe with
    a Triangle Wireframe inside of it as another n x 3 Set of Points.

    getTestSet3: This Method sets the 3D Scene Points with an arbitrary 8 x 3
    Set of Points for performing quick tests.

    getSmallTestSet: This Method sets the 3D Scene Points with an even smaller
    arbitrary 4 x 3 Set of Points for performing quick tests.

    get3DSceneHeight: This Method computes and stores the 3D Scene Points Array
    Height or the Number of Rows.

    get3DSceneWidth: This Method computes and stores the 3D Scene Points Array
    Height or the Number of Rows.

    getSmallTestSetHeight: This Method computes and stores the 3D Scene Points
    Array (based on small Test Set) Height or the Number of Rows.

    getSmallTestSetWidth: This Method computes and stores the 3D Scene Points
    Array (based on small Test Set) Width or the Number of Columns.

    showPolygonClassSypnosis: This Method invokes and displays the Polygon Class
    Sypnosis.

    showImageClassSypnosis: This Method invokes and displays the Image Class
    Sypnosis.

    turnOnAllDisplayOptions: This Method turns on all Boolean Options for
    Verbose, Display and Test.

    turnOffAllDisplayOptions: This Method turns off all Boolean Options for
    Verbose, Display and Test.

    disp3DScenePoints: This Method prints the 3D Scene Points and the
    corresponding Height and Width.

    dispSmallTestSetPoints: This Method prints the 3D Scene Points based on the
    small Test Set and the corresponding Height and Width.

    performSelectedTest: This Method performs the selected Test by specifying
    which Test Scenario to run.

    performTestScenario1: This Method performs the Test based on the Cube and
    the Triangle Wireframes so as to calibrate and verify that Vectorisation and
    Optimisation of Codes will not affect Rotation and Perspective Projection
    Methods.

    performTestScenario2: This Method performs the Test involving 3D Scene
    Points, small Test Set, new algorithms etc.

    cleanup: Method to execute all tasks that need to be done at the end.
    """
    
    #============================
    #Class Properties/Attributes.
    #============================
    #Reserved for Global Class Attributes, if any. Instance Attributes are
    #initialised in __init__ Constructor Method.
    
    #========
    #Methods.
    #========
    def __init__(self, strWorkingDirectory, strImageFileName):
        #===================
        #Constructor Method.
        #===================
        #General.
        import image, projectwindow
        self.window = projectwindow.ProjectWindow()
        self.img = image.Image(self.window, strImageFileName)
        self.poly = Polygon(self.window, self.img)
        #window.display()
        cv2.waitKey(0)
        
        #Working Directory.
        self._strWorkingDirectory = None

        #Test Set.
        self._mat3DScene = None
        self._mat3DSceneHeight = None
        self._mat3DSceneWidth = None
        self._matSmallTestSet = None
        self._matSmallTestSetHeight = None
        self._matSmallTestSetWidth = None

        #Flattened Small Test Set.
        self._matSmallTestSetFlattened = None

        #Rotation Angle and Rotation Axis (in Unit Vector Format).
        self._fltTheta = -30
        self._wx = 0
        self._wy = 1
        self._wz = 0

        #Verbose and Display Options.
        self._booVerbose = False
        self._booDisplayCamTrans = False
        self._booDisplayCamOrient = False
        self._booPlotPersProj = False

        #Camera Locations.
        self._arrayCamPos1 = [0, 0, -5]
        self._arrayCamPos2 = None
        self._arrayCamPos3 = None
        self._arrayCamPos4 = None
        _matRotatedPoints = None
        self._intIterations = 3
        self._strFigureTitle = "Camera Translations"

        #Camera Orientations.
        self._matCamOrient1 = np.array(np.eye(3))
        self._matCamOrient2 = None
        self._matCamOrient3 = None
        self._matCamOrient4 = None
        self._strFigureTitle1 = "Camera Orientation 1"
        self._strFigureTitle2 = "Camera Orientation 2"
        self._strFigureTitle3 = "Camera Orientation 3"
        self._strFigureTitle4 = "Camera Orientation 4"

        #Perspective Projections.
        self._arrayFr1PersProj = None
        self._arrayFr2PersProj = None
        self._arrayFr3PersProj = None
        self._arrayFr4PersProj = None
        self._strPlotTitle = "Perspective Projection"

        #================
        #Test Scenario 2.
        #================
        #Test Sets.
        #Test 8 x 3 Matrix as List of 3D Scene Points.
        self._matOnes = np.matrix(np.ones([3, 3]))

        #Test Mode.
        self._booTestMode = False

    def getWorkingDirectory(strWorkingDirectory):
        os.system('cls')
        os.chdir(strWorkingDirectory)
        self._strWorkingDirectory = os.getcwd()
        print("The current Working Directory is \"" \
              + self._strWorkingDirectory + "\".\n")
                
    def getTestSet1(self):
        #===============
        #Initialisation.
        #===============
        self._mat3DScene = np.zeros([11, 3])

        #=======================
        #Populate the 3D Points.
        #=======================
        self._mat3DScene[0, :] = [-1, -1, -1]
        self._mat3DScene[1, :] = [1, -1, -1]
        self._mat3DScene[2, :] = [1, 1, -1]
        self._mat3DScene[3, :] = [-1, 1, -1]
        self._mat3DScene[4, :] = [-1, -1, 1]
        self._mat3DScene[5, :] = [1, -1, 1]
        self._mat3DScene[6, :] = [1, 1, 1]
        self._mat3DScene[7, :] = [-1, 1, 1]
        self._mat3DScene[8, :] = [-0.5, -0.5, -1]
        self._mat3DScene[9, :] = [0.5, -0.5, -1]
        self._mat3DScene[10, :] = [0, 0.5, -1]

    def getTestSet2(self):
        def createIntermediatePoints(pt1, pt2, intGranularity):
            #===============
            #Initialisation.
            #===============
            _mat3DScene = []

            #===============
            #Compute Vector.
            #===============
            vector = np.array([(x[0] - x[1]) for x in zip(pt1, pt2)])

            #==============================
            #Return the Granularised Array.
            #==============================
            return[(np.array(pt2) + (vector * (float(i) / intGranularity))) \
                   for i in range(1, intGranularity)]

        #===============
        #Initialisation.
        #===============
        self._mat3DScene = []
        intGranularity = 20

        #======================
        #Create Cube Wireframe.
        #======================
        self._mat3DScene.extend([[-1, -1, -1], [1, -1, -1], [1, 1, -1],
                                 [-1, 1, -1], [-1, -1, 1], [1, -1, 1],
                                 [1, 1, 1], [-1, 1, 1]])

        self._mat3DScene.extend(createIntermediatePoints([-1, -1, 1],
                                                         [1, -1, 1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([1, -1, 1], [1, 1, 1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([1, 1, 1], [-1, 1, 1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([-1, 1, 1], [-1, -1, 1],
                                                         intGranularity))

        self._mat3DScene.extend(createIntermediatePoints([-1, -1, -1],
                                                         [1, -1, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([1, -1, -1],
                                                         [1, 1, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([1, 1, -1],
                                                         [-1, 1, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([-1, 1, -1],
                                                         [-1, -1, -1],
                                                         intGranularity))

        self._mat3DScene.extend(createIntermediatePoints([1, 1, 1], [1, 1, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([1, -1, 1],
                                                         [1, -1, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([-1, -1, 1],
                                                         [-1, -1, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([-1, 1, 1],
                                                         [-1, 1, -1],
                                                         intGranularity))

        #==========================
        #Create Triangle Wireframe.
        #==========================
        self._mat3DScene.extend([[-0.5, -0.5, -1], [0.5, -0.5, -1],
                                 [0, 0.5, -1]])
        self._mat3DScene.extend(createIntermediatePoints([-0.5, -0.5, -1],
                                                         [0.5, -0.5, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([0.5, -0.5, -1],
                                                         [0, 0.5, -1],
                                                         intGranularity))
        self._mat3DScene.extend(createIntermediatePoints([0, 0.5, -1],
                                                         [-0.5, -0.5, -1],
                                                         intGranularity))

        #===========================
        #Set the Granularised Array.
        #===========================
        self._mat3DScene = np.array(self._mat3DScene)

    def getTestSet3(self):
        #=======================
        #Populate the 3D Points.
        #=======================
        self._mat3DScene = np.matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0],
                                      [0, 1, 1], [1, 0, 0], [1, 0, 1],
                                      [1, 1, 0], [1, 1, 1]])

    def getSmallTestSet(self):
        #=========================================================================
        #Populate a small Test Set mirroring Image Class' Image._image_points Data
        #Structure of (u, v, [x, y, z]).
        #=========================================================================
        self._matSmallTestSet = np.zeros((2, 2, 3))
        self._matSmallTestSet[0, 0] = [1, 1, 1]
        self._matSmallTestSet[0, 1] = [2, 2, 2]
        self._matSmallTestSet[1, 0] = [3, 3, 3]
        self._matSmallTestSet[1, 1] = [4, 4, 4]

    def get3DSceneHeight(self):
        self._mat3DSceneHeight = self._mat3DScene.shape[0]

    def get3DSceneWidth(self):
        self._mat3DSceneWidth = self._mat3DScene.shape[1]

    def getSmallTestSetHeight(self):
        self._matSmallTestSetHeight = self._matSmallTestSet.shape[0]

    def getSmallTestSetWidth(self):
        self._matSmallTestSetWidth = self._matSmallTestSet.shape[1]
      
    def showPolygonClassSypnosis(self):
        #Polygon Class Documentation.
        print poly.__doc__

    def showImageClassSypnosis(self):
        #Image Class Documentation.
        print img.__doc__

    def turnOnAllDisplayOptions(self):
        self._booVerbose = True
        self._booDisplayCamTrans = True
        self._booDisplayCamOrient = True
        self._booPlotPersProj = True
        self._booTestMode = True

    def turnOffAllDisplayOptions(self):
        self._booVerbose = False
        self._booDisplayCamTrans = False
        self._booDisplayCamOrient = False
        self._booPlotPersProj = False
        self._booTestMode = False

    def disp3DScenePoints(self):
        print("self._mat3DScene is:\n")
        print(self._mat3DScene)
        print("\n")
        print("The Number of Rows and Columns of the \"" + "self._mat3DScene" \
              + " Array are:\n")
        print(str(self._mat3DSceneHeight) + " Rows, " \
              + str(self._mat3DSceneWidth) + " Columns.\n")
        print("\n")

    def dispSmallTestSetPoints(self):
        print("self._matSmallTestSet is:\n")
        print(self._matSmallTestSet)
        print("\n")
        print("The Number of Rows and Columns of the \"" \
              + "self._matSmallTestSet" + " Array are:\n")
        print(str(self._matSmallTestSetHeight) + " Rows, " \
              + str(self._matSmallTestSetWidth) + " Columns.\n")
        print("\n")

    def performSelectedTest(self, intSelection):
        #===================
        #Select Test to run.
        #===================
        if(intSelection == 1):
            #====================
            #Run Test Scenario 1.
            #====================
            print("Running Test Scenario 1...\n")
            self.performTestScenario1()
        elif(intSelection == 2):
            #====================
            #Run Test Scenario 2.
            #====================
            print("Running Test Scenario 2...\n")
            self.performTestScenario2()
        else:
            #==========================
            #Unspecified Test Scenario.
            #==========================
            print("You have selected an unspecified Test Scenario!")
                                       
    def performTestScenario1(self):
        #==================================================================
        #1. Test Scenario 1: Cube and Triangle Wireframe Manipulation for
        #calibrating and optimising the Methods in Image Class and Polygon
        #Class.
        #==================================================================
        print("===================")
        print("1. Test Scenario 1.")
        print("===================")
        print("\n")

        #==================
        #a. Initialisation.
        #==================
        print("==================")
        print("a. Initialisation.")
        print("==================")       
        self.getTestSet2()

        if(self._booVerbose):
            #=============
            #Verbose Mode.
            #=============
            self.disp3DScenePoints()
            self.dispSmallTestSetPoints()

        #====================
        #b. Camera Locations.
        #====================
        print("====================")
        print("b. Camera Locations.")
        print("====================")

        #Compute Camera Locations.
        self._matRotatedPoints = self.img._rotByQuatMult(self._arrayCamPos1,
                                                     self._fltTheta,
                                                     self._wx, self._wy,
                                                     self._wz,
                                                     self._intIterations)
        self._arrayCamPos2 = np.array(self._matRotatedPoints[0, :])[0].tolist()
        self._arrayCamPos3 = np.array(self._matRotatedPoints[1, :])[0].tolist()
        self._arrayCamPos4 = np.array(self._matRotatedPoints[2, :])[0].tolist()
        self._matRotatedPoints = np.append(self._arrayCamPos1,
                                           self._matRotatedPoints)

        if(self._booVerbose):
            #=============
            #Verbose Mode.
            #=============
            print("The Camera Position at Frame 1 is:\n")
            print self._arrayCamPos1
            print("\n")
            print("The Camera Position at Frame 2 is:\n")
            print(self._arrayCamPos2)
            print("\n")
            print("The Camera Position at Frame 3 is:\n")
            print(self._arrayCamPos3)
            print("\n")
            print("The Camera Position at Frame 4 is:\n")
            print(self._arrayCamPos4)
            print("\n")

        #Display Camera Translations.
        if(self._booDisplayCamTrans):
            #============================
            #Display Camera Translations.
            #============================
            self.img.dispCamTrans(self._matRotatedPoints, self._strFigureTitle,
                                  booAnnotateCFOnly = False)
            print("\n")

        #=======================
        #c. Camera Orientations.
        #=======================
        print("=======================")
        print("c. Camera Orientations.")
        print("=======================")

        #Compute Camera Orientations.
        self._matCamOrient2 = self.img._rotByRotMat(self._matCamOrient1,
                                                self._fltTheta,
                                                self._wx, self._wy, self._wz, 1)
        self._matCamOrient3 = self.img._rotByRotMat(self._matCamOrient2,
                                                self._fltTheta,
                                                self._wx, self._wy, self._wz, 1)
        self._matCamOrient4 = self.img._rotByRotMat(self._matCamOrient3,
                                                self._fltTheta,
                                                self._wx, self._wy, self._wz, 1)

        #Display Camera Orientations.
        if(self._booDisplayCamOrient):
            #============================
            #Display Camera Orientations.
            #============================
            self.img.dispCamOrient(self._matCamOrient1, self._strFigureTitle1)
            self.img.dispCamOrient(self._matCamOrient2, self._strFigureTitle2)
            self.img.dispCamOrient(self._matCamOrient3, self._strFigureTitle3)
            self.img.dispCamOrient(self._matCamOrient4, self._strFigureTitle4)

        if(self._booVerbose):
            #=============
            #Verbose Mode.
            #=============
            print("The Camera Orientation at Frame 1 is:\n")
            print self._matCamOrient1
            print("\n")
            print("The Camera Orientation at Frame 2 is:\n")
            print(self._matCamOrient2)
            print("\n")
            print("The Camera Orientation at Frame 3 is:\n")
            print(self._matCamOrient3)
            print("\n")
            print("The Camera Orientation at Frame 4 is:\n")
            print(self._matCamOrient4)
            print("\n")
            print("Each Row of the above Matrices represent the X-Axis, ")
            print("Y-Axis and Z-Axis Directions respectively.\n")
            print("\n")

        #===================================================================
        #d. Plot the Images for the Perspective Projection for the 4 Frames.
        #===================================================================
        print("===================================================================")
        print("d. Plot the Images for the Perspective Projection for the 4 \n")
        print("Frames.")
        print("===================================================================")
        self._arrayFr1PersProj = self.img.persProj(self._mat3DScene,
                                                   self._arrayCamPos1,
                                                   self._matCamOrient1)
        self._arrayFr2PersProj = self.img.persProj(self._mat3DScene,
                                              self._arrayCamPos2,
                                              self._matCamOrient2)
        self._arrayFr3PersProj = self.img.persProj(self._mat3DScene,
                                              self._arrayCamPos3,
                                              self._matCamOrient3)
        self._arrayFr4PersProj = self.img.persProj(self._mat3DScene,
                                              self._arrayCamPos4,
                                              self._matCamOrient4)

        if(self._booPlotPersProj):
            #=============================
            #Plot Perspective Projections.
            #=============================
            self.img.plotProj(self._strPlotTitle, self._arrayFr1PersProj,
                         self._arrayFr2PersProj, self._arrayFr3PersProj,
                         self._arrayFr4PersProj)
            print("\n")

    def performTestScenario2(self):
        #=======================================================================
        #2. Test Scenario 2: Vectorisation and Optimisation of Image and Polygon
        #Classes.
        #=======================================================================
        print("===================")
        print("1. Test Scenario 2.")
        print("===================")
        print("\n")

        #==================
        #a. Initialisation.
        #==================
        print("==================")
        print("a. Initialisation.")
        print("==================")       
        self.getTestSet3()

        if(self._booVerbose):
            #=============
            #Verbose Mode.
            #=============
            self.disp3DScenePoints()
            self.dispSmallTestSetPoints()
                
        #====================
        #b. Camera Locations.
        #====================
        print("====================")
        print("b. Camera Locations.")
        print("====================")

        #===============================================================
        #c. Performance Evaluation of Rotation using 3D Scene Points and
        #Rotation Matrix.
        #===============================================================
        print("===============================================================")
        print("c. Performance Evaluation of Rotation using 3D Scene Points and")
        print("Rotation Matrix.")
        print("===============================================================")

        #Start Time Capture.
        import time
        intStart = time.time()

        print "Original 3D Scene Points:\n"
        print self.img._flat_3dpoints
        print "\n"

        self.img._flat_3dpoints_new = self.img._rotByImage(self.img,
                                                            self._fltTheta,
                                                            self._wx,
                                                            self._wy, self._wz)

        #End Time Capture. Calculate Time Elapse.
        intEnd = time.time()

        print "Rotated 3D Scene Points:\n"
        print self.img._flat_3dpoints_new
        print "\n"
        print "Dimensions of the Array of Rotated Points is:\n"
        print self.img._flat_3dpoints_new.shape
        print "\n"
        print "Original 3D Scene Points Height (Rows) is: "
        print self.img.getHeight()
        print "\n"
        print "Original 3D Scene Points Width (Columns) is: "
        print self.img.getWidth()
        print "\n"
        print "The Product of Height and Width = # Pixels is:"
        print self.img.getHeight() * self.img.getWidth()
        print "\n"
        print "The Time Elapsed to perform the Rotation of " \
              + str(self.img.getHeight() * self.img.getWidth()) \
              + " Pixels is: " + str(intEnd - intStart) + " Seconds.\n"

        #====================
        #d. Camera Locations.
        #====================
        print("====================")
        print("d. Camera Locations.")
        print("====================")

        #Test 3D Scene Flat Structure.
        self.getSmallTestSet()
        self._matSmallTestSetFlattened = self._matSmallTestSet.ravel()
        print(self._matSmallTestSetFlattened)
        self._matRotatedPoints = self._mat3DScene * self._matOnes
        print("\n")

        if(self._booTestMode):
            #==========
            #Test Mode.
            #==========
            print "self._mat3DScene is:\n"
            print self._mat3DScene
            print "\n"
            print "self._matOnes is:\n"
            print self._matOnes
            print "\n"
            print "self._matRotatedPoints is:\n"
            print self._matRotatedPoints
            print "\n"

        #===========================
        #e. Perspective Projections.
        #===========================
        print("===========================")
        print("e. Perspective Projections.")
        print("===========================")

        #Test First Frame of Perspective Projection.
        self._arrayFr1PersProj = self.img.persProj(self.img._flat_3dpoints,
                                                   self._arrayCamPos1,
                                                   self._matCamOrient1)

        #Test Second Frame of Perspective Projection.
        self._arrayCamPos2 = self.img._rotByQuatMult(self._arrayCamPos1,
                                                      self._fltTheta,
                                                      self._wx, self._wy,
                                                      self._wz, 1)
        self._matCamOrient2 = self.img._rotByRotMat(self._matCamOrient1,
                                                     self._fltTheta,
                                                     self._wx, self._wy,
                                                     self._wz, 1)
        self._arrayFr2PersProj = self.img.persProj(self.img._flat_3dpoints,
                                                   self._arrayCamPos2,
                                                   self._matCamOrient2)

        #Test Third Frame of Perspective Projection.
        self._arrayCamPos3 = self.img._rotByQuatMult(self._arrayCamPos2,
                                                      self._fltTheta,
                                                      self._wx, self._wy,
                                                      self._wz, 1)
        self._matCamOrient3 = self.img._rotByRotMat(self._matCamOrient2,
                                                     self._fltTheta,
                                                     self._wx, self._wy,
                                                     self._wz, 1)
        self._arrayFr3PersProj = self.img.persProj(self.img._flat_3dpoints,
                                                   self._arrayCamPos3,
                                                   self._matCamOrient3)

        #Test Fourth Frame of Perspective Projection.
        self._arrayCamPos4 = self.img._rotByQuatMult(self._arrayCamPos3,
                                                      self._fltTheta,
                                                      self._wx, self._wy,
                                                      self._wz, 1)
        self._matCamOrient4 = self.img._rotByRotMat(self._matCamOrient3,
                                                     self._fltTheta,
                                                     self._wx, self._wy,
                                                     self._wz, 1)
        self._arrayFr4PersProj = self.img.persProj(self.img._flat_3dpoints,
                                                   self._arrayCamPos4,
                                                   self._matCamOrient4)

        #Plot Perspective Projection.
        self._strPlotTitle = \
                           "Perspective Projection of CS4243 project.jpeg 3D Points"

        if(self._booPlotPersProj):
            #=============================
            #Plot Perspective Projections.
            #=============================
            self.img.plotProj(self._strPlotTitle, self._arrayFr1PersProj,
                         self._arrayFr2PersProj, self._arrayFr3PersProj,
                              self._arrayFr4PersProj)
            print("\n")

    def cleanup(self):
        print "Cleaning up after testing..."

