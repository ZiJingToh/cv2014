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
1.3.0     06/11/2014   Dave Tan     Introduced codes to test 2D Perspective
                                    Projection.
2.0.0     07/11/2014   Dave Tan     Moved all codes into a new Test Class and
                                    converted all Functions to Test Class
                                    Methods.
"""

#==================
#1. Initialisation.
#==================
print("==================")
print("a. Initialisation.")
print("==================")
from test import Test
strWorkingDirectory = "F:\Python\CS4243\Project\CS4243_V3.0.0_Baseline_Dave\cs4243"
strImageFileName = "project.jpeg"
test = Test(strWorkingDirectory, "..\\" + strImageFileName)
print("\n")

#=========
#2. Tests.
#=========
print("=========")
print("2. Tests.")
print("=========")
print("\n")

#==================================
#a. Perform selected Test Scenario.
#==================================
print("==================================")
print("a. Perform selected Test Scenario.")
print("==================================")
test.turnOffAllDisplayOptions()
test.performSelectedTest(1)



