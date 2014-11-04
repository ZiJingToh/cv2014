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
1.0.0     26/10/2014   Dave Tan     Initial Version of Image Class
                                    incorporating the Methods: __init__,
                                    persproj, plotproj.
2.0.0     01/11/2014   ???          Added the following Methods:
                                    resetImagePoints, interpolateImagePoints,
                                    getView, getWidth, getHeight, getViewScale,
                                    getCoordsFor, getZAt, setZAt,
                                    convertToImageSpace, convertToViewSpace,
                                    show_image, update_image, delete_image,
                                    save_image.
"""


import platform
from matplotlib.mlab import griddata
import numpy as np
import cv2


class Image:
    """
    ************
    Class Image.
    ************
    =========
    Sypnosis.
    =========
    This is a Class representing the Image Object.

    ========
    Methods.
    ========
    __init__: This is the Constructor Method for Class Image.
    
    persProj: This Method performs the Perspective Projection and returns the 2D
    Array containing the Projected Points.

    plotProj: This Method names the Plot of the 2 x 2 SubPlots according to the
    Title provided. This Function is used to plot the Perspective Projection of
    4 Frames.
    """
    #========
    #Methods.
    #========
    def __init__(self, project_window, image_path):
        #===================
        #Constructor Method.
        #===================
        if platform.system() == "Darwin":
            self._image = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_COLOR)[::-1,::-1]
        else:
            self._image = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_COLOR)

        self._view = self._image[:]
        self._view_scale = 0.65

        self._flat_3dpoints = []
        self._image_new = None

        # stores x,y,z world coords for each point
        self._image_points = np.zeros_like(self._image, np.int)
        self.resetImagePoints()
        print "The Dimensions of the Image are:\n"
        print self._image_points.shape
        print "\n"

    def resetImagePoints(self):
        # stores x,y,z world coords for each point
        t_row, t_col = np.ogrid[0:self._image.shape[0], 0:self._image.shape[1]]
        self._image_points[t_row, t_col, 0] = t_col
        self._image_points[t_row, t_col, 1] = t_row
        self._image_points[t_row, t_col, 2] = 0

    def interpolateImagePoints(self, points):
        t_row, t_col = np.ogrid[0:self._image.shape[0], 0:self._image.shape[1]]
        values = [self.getZAt(*p) for p in points]
        interpZ = griddata([x[0] for x in points], [x[1] for x in points], values,
                           t_col.tolist()[0], t_row.transpose().tolist()[0],
                           "linear")
        self._image_points[t_row, t_col, 2] = interpZ

    def getFlat3DPoints(self):
        #===============
        #Initialisation.
        #===============
        print "Getting Flat3DPoints...\n"

        #If anyone can help to vectorise the Double for Loop, the performance
        #would increase by leaps and bounds.

        """
        for intRowIndex in range(0, self.getHeight(), 1):
            for intColumnIndex in range(0, self.getWidth(), 1):
                if((intRowIndex == 0) and (intColumnIndex == 0)):
                    #===============
                    #First 3D Point.
                    #===============
                    self._flat_3dpoints = \
                    self._image_points[intRowIndex][intColumnIndex]
                else:
                    #====================
                    #Subsequent 3D Point.
                    #====================
                    self._flat_3dpoints = \
                    np.append([self._flat_3dpoints],
                              self._image_points[intRowIndex][intColumnIndex])
        """

        #=========================================
        #Compose the 3D Scene Point List Property.
        #=========================================
        #Using the Double for Loop above takes too long, will look into
        #vectorisation of this portion after work today. So temporarily using
        #a Mock-Up 8 by 3 List to test the Rotation via Polygon Class Method
        #rotByImage. Hence the above codes are commented out for the time-being.
        self._flat_3dpoints = np.matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0],
                                      [0, 1, 1], [1, 0, 0], [1, 0, 1],
                                      [1, 1, 0], [1, 1, 1]])
        
    def getView(self):
        """
        Returns a copy of current view
        """
        return cv2.resize(self._view, (0,0),
                          fx=self._view_scale,
                          fy=self._view_scale)

    def getWidth(self):
        return self._image.shape[1]

    def getHeight(self):
        return self._image.shape[0]

    def getViewScale(self):
        return self._view_scale

    def getCoordsFor(self, x, y):
        return self._image_points[y][x]

    def getZAt(self, x, y):
        return self._image_points[y][x][-1]

    def setZAt(self, zValue, x, y ):
        self._image_points[y][x][-1] = zValue
        
    def convertToImageSpace(self, x, y):
        x *= 1.0/self._view_scale
        y *= 1.0/self._view_scale
        return (int(x), int(y))

    def convertToViewSpace(self, x, y):
        x *= self._view_scale
        y *= self._view_scale
        return (int(x), int(y))

    def persProj(self, array3DScPts, arrayCamTrans, matCamOrient, int_f = 1,
                 int_u0 = 0, int_bu = 1, int_ku = 1, int_v0 = 0, int_bv = 1,
                 int_kv = 1):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        i_f = np.transpose(matCamOrient[0, :])
        j_f = np.transpose(matCamOrient[1, :])
        k_f = np.transpose(matCamOrient[2, :])
        ufp = []
        vfp = []
        intRows = array3DScPts.shape[0]
        matProjPts = np.zeros([1, 2])

        for intRowIndex in range(0, intRows, 1):
            #===============================
            #Extract Current 3D Coordinates.
            #===============================
            listCurrent3DPt = array3DScPts[intRowIndex, :]
            sp_minus_tf = listCurrent3DPt - arrayCamTrans

            #====
            #ufp.
            #====
            fltNumerator = int_f * np.dot(np.transpose(sp_minus_tf), i_f)
            fltDenominator = np.dot(np.transpose(sp_minus_tf), k_f)
            ufp = (fltNumerator / fltDenominator) * int_bu + int_u0
            
            #====
            #vfp.
            #====           
            fltNumerator = int_f * np.dot(np.transpose(sp_minus_tf), j_f)
            fltDenominator = np.dot(np.transpose(sp_minus_tf), k_f)
            vfp = (fltNumerator / fltDenominator) * int_bv + int_v0

            #=============================
            #Store the Projected 2D Point.
            #=============================
            if(intRowIndex == 0):
                #=========================
                #First Projected 2D Point.
                #=========================
                matProjPts = [ufp, vfp]
            else:
                #=========================
                #Subsequent Rotated Point.
                #=========================
                matProjPts = np.append(matProjPts, [ufp, vfp])

        #==========================
        #Return the 2D Coordinates.
        #==========================
        matProjPts = np.matrix(matProjPts)
        intRows = matProjPts.shape[0]
        intColumns = matProjPts.shape[1]
        intElements = intRows * intColumns
        intNewRows = int(intElements / 2)
        matProjPts = np.reshape(matProjPts, (intNewRows, 2))
        return(matProjPts)

    def plotProj(self, strPlotTitle, arrayFr1PersProj, arrayFr2PersProj,
                 arrayFr3PersProj, arrayFr4PersProj):
        #===============
        #Initialisation.
        #===============
        import matplotlib
        import matplotlib.pyplot as plt
        plt.suptitle(strPlotTitle)

        #=======================================================
        #Build the Subplots comprising the 3D-to-2D Projections.
        #=======================================================
        for i in range(1, 5):
            #======================
            #Configure the Subplot.
            #======================
            plt.subplot(2, 2, i)
            plt.title("Frame " + str(i))
            plt.xlabel("X")
            plt.ylabel("Y")
            x = eval("arrayFr" + str(i) + "PersProj[:, 0]")
            y = eval("arrayFr" + str(i) + "PersProj[:, 1]")
            
            #=================
            #Draw the Subplot.
            #=================
            plt.plot(x, y, 'r.')

        #======================================================
        #Display the 3D-to-2D Projection Plot for the 4 Frames.
        #======================================================
        plt.show()

    def show_image(self, image, image_title):
        cv2.namedWindow(image_title)
        cv2.imshow(image_title, image)

    def update_image(self, cur_image, new_image, image_title):
        newx,newy = new_image.shape[1]/2, new_image.shape[0]/2 #new size (w,h)
        cur_image = cv2.resize(cur_image,(newx,newy))
        cv2.destroyAllWindows()    
        cv2.imshow(image_title, new_image)

    def delete_image(self):
        ''' might need to add in delete image file '''
        cv2.destroyAllWindows()

    def save_image(self, image_filename, image):
        cv2.imwrite(image_filename,image)
