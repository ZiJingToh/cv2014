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
          01/11/2014   Dave Tan     Added new Methods: getFlat3DPoints, IsNaN,
                                    dispCamTrans, dispCamOrient.
2.0.1     04/11/2014   Dave Tan     Removed all Class Attributes and stick to
                                    Instance Attributes.
          05/11/2014   Dave Tan     Vectorised Method getFlat3DPoints.
"""

import platform
from matplotlib.tri import Triangulation, TriAnalyzer
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

    getFlat3DPoints: This Method gets the n x 3 List of 3D Points from the Image
    Class _image_points Instance Attribute.

    IsNaN: This Method evaluates whether the Scalar Input is a NaN and returns
    the Boolean Result, True if NaN and False otherwise.

    dispCamTrans: This Method returns the Camera Translation Points provided by
    the n x 3 Input Matrix containing the very first Point plus other Rotated
    Points.

    dispCamOrient: This Method returns the Camera Orientation with the i, j and
    k Axes plotted.
    """

    #============================
    #Class Properties/Attributes.
    #============================
    #Reserved for Global Class Attributes, if any. Instance Attributes are
    #initialised in __init__ Constructor Method.

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

        # stores x,y,z world coords for each point
        self._image_points = np.zeros_like(self._image, np.int)
        self.resetImagePoints()
        print "The Dimensions of the Image are:\n"
        print self._image_points.shape
        print "\n"

        #Old and New Flat 3D Points.
        self._flat_3dpoints = []
        self._flat_3dpoints_new = []

        #Extract 3D Points.
        self.getFlat3DPoints()

        # store triangulation after points are selected
        self._tri = None
        self._triImages = []
        self._selectedPoints = []

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
        self._flat_3dpoints = self._image_points.ravel().reshape(-1, 3)
        
    def getView(self):
        """
        Returns a copy of current view
        """
        return cv2.resize(self._view, (0,0),
                          fx=self._view_scale,
                          fy=self._view_scale)

    def getResizedImage(self, image):
        return cv2.resize(image, (0,0),
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

    def triangulate(self, points):
        x, y = np.meshgrid(range(15),range(11))
        x = (self._image.shape[1]/14) * x.flatten()
        y = (self._image.shape[0]/10) * y.flatten()

        extendedPoints = np.array([(p[0],p[1],self.getZAt(*p)) for p in zip(x, y)]).astype(np.float32)

        self._selectedPoints = points.astype(np.float32)
        self.selectedPoints = np.concatenate((self._selectedPoints, extendedPoints))
        self._newSelectedPoints = self._selectedPoints.copy()
        self._tri = Triangulation(points[:,0],
                                  points[:,1])
        self._tri.set_mask(TriAnalyzer(self._tri).get_flat_tri_mask())
        self._triImages = []

        # cache image for each triangle
        for triangle in self._tri.get_masked_triangles():
            triPoints = np.array([self._selectedPoints[p][0:2] for p in triangle])

            # cut out triangle image - create mask
            mask = np.zeros(self._image.shape, dtype=np.uint8)
            cv2.fillPoly(mask,
                         np.array([triPoints.astype(np.int)]),
                         (255, 255, 255))
            #mask = cv2.erode(mask, (3, 3))

            # apply the mask
            maskedImage = cv2.bitwise_and(self._image, mask)            
            
            self._triImages.append(maskedImage)

        #self._newSelectedPoints[:,0] = ((self._newSelectedPoints[:,0] - 770))
        #self._newSelectedPoints[:,1] = ((self._newSelectedPoints[:,1] - 740))
        #for index, point in enumerate(self._newSelectedPoints):
        #    z = point[-1]
        #    point[0] -= 770
        #    point[1] -= 740
        #    if z > 0:
        #        point *= np.interp(z,[0,1000],[1,3])
        #    point[-1] = z
        #    self._newSelectedPoints[index] = point

    def getImageFromCam(self, arrayCamTrans, matCamOrient, int_f):
        """
        Drawing using all points
        """
        uvPoints = self.persProj(self._selectedPoints,
                                 arrayCamTrans,
                                 matCamOrient,
                                 int_f = int_f).astype(np.float32)
        uvPoints[:,0] += self.getWidth()/2
        uvPoints[:,1] += self.getHeight()/2

        rows, cols, ch = self._image.shape

        newImage = np.zeros_like(self._image)
        for index, triangle in enumerate(self._tri.get_masked_triangles()):
            newTriPoints = np.array([uvPoints[p] for p in triangle])
            # skip if facing back
            if np.cross(newTriPoints[1]-newTriPoints[0], newTriPoints[2]-newTriPoints[1]) <= 0:
                continue
            originalTriPoints = np.array([self._selectedPoints[p][0:2] for p in triangle])
            M = cv2.getAffineTransform(originalTriPoints, newTriPoints)
            dst = cv2.warpAffine(self._triImages[index], M, (cols, rows))
            newImage = np.maximum(dst, newImage)
        return newImage

    def getImageFromCam2(self, arrayCamTrans, matCamOrient):
        """
        Drawing using selected points + triangles
        """
        newImage = self._image.reshape((self.getHeight()*self.getWidth(), 3))
        newImage = newImage[0:self.getHeight()*self.getWidth():75]
        newImagePoints = self._image_points.reshape((self.getHeight()*self.getWidth(), 3))
        newImagePoints = newImagePoints[0:self.getHeight()*self.getWidth():75]

        uvPoints = self.persProj(newImagePoints,
                                 arrayCamTrans,
                                 matCamOrient,
                                 int_f = 350).astype(np.float32)
        uvPoints[:,0] += self.getWidth()/2
        uvPoints[:,1] += self.getHeight()/2

        retImage = np.zeros_like(self._image)
        for index, point in enumerate(uvPoints):
            point = tuple(np.array(point).flatten())
            color = tuple(newImage[index])
            cv2.circle(retImage, point, 2, [int(x) for x in color] )
        
        return retImage

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
            ufp = ((fltNumerator / fltDenominator) if fltDenominator > 0 else 0) * int_bu + int_u0
            
            #====
            #vfp.
            #====           
            fltNumerator = int_f * np.dot(np.transpose(sp_minus_tf), j_f)
            fltDenominator = np.dot(np.transpose(sp_minus_tf), k_f)
            vfp = ((fltNumerator / fltDenominator) if fltDenominator > 0 else 0) * int_bv + int_v0

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

    def IsNaN(self, varScalarInput):
        #=====================================================================
        #Evaluate whether the Scalar Intput is NaN. This is the usual way to
        #test for NaN to see if it's equal to itself, as NaN won't be equal to
        #itself.
        #=====================================================================
        booIsNaN = (varScalarInput != varScalarInput)

        #==================
        #Return the Result.
        #==================
        return(booIsNaN)

    def dispCamTrans(self, mat1stPlusRotatedPoints, strFigureTitle,
                     intxMin = -5, intxMax = 5, intyMin = -5, intyMax = 5,
                     intzMin = -5, intzMax = 5):
        def reprojectlabels(event):
            #==============================================================
            #Transform 3D Co-Ordinates to get new 2D Projection onto the XZ
            #Plane.
            #==============================================================
            listTX, listTZ, _ = proj3d.proj_transform(listX, listZ, listY,
                                                      axCurrent.get_proj())

            #===================
            #Compensate for NaN.
            #===================
            for intIndex in range(listTX.shape[0]):
                #==============================
                #For Transformed X-Coordinates.
                #==============================
                if(self.IsNaN(listTX[intIndex])):
                    listTX[intIndex] = 0.00001

                #==============================
                #For Transformed Z-Coordinates.
                #==============================
                if(self.IsNaN(listTZ[intIndex])):
                    listTZ[intIndex] = 0.000001

                #=====================================
                #Compute the updated Label Cordinates.
                #=====================================
                for i in range(len(listX)):
                    labelCurrent = listLabels[i]
                    labelCurrent.xy = listTX[i], listTZ[i]
                    labelCurrent.update_positions(figCurrent.canvas.renderer)
                    figCurrent.canvas.draw()

            #==============================
            #Return to the Calling Routine.
            #==============================
            return

        #===============
        #Initialisation.
        #===============
        np.seterr(divide = 'ignore', invalid = 'ignore')
        import matplotlib
        import matplotlib.pyplot as pltCurrent
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d
        import pylab
        import math as ma

        figCurrent = pltCurrent.figure()
        axCurrent = figCurrent.gca(projection = '3d')
        axCurrent.set_xlabel('x')
        axCurrent.set_ylabel('z')
        axCurrent.set_zlabel('y')
        axCurrent.set_xlim(intxMin, intxMax)
        axCurrent.set_ylim(intyMin, intyMax)
        axCurrent.set_zlim(intzMin, intzMax)
        axCurrent.invert_xaxis()
        axCurrent.invert_yaxis()
        axCurrent.invert_zaxis()
        listLabels = []
        uintElevation = 30
        uintAzimuth = 75
        axCurrent.view_init(uintElevation, uintAzimuth)
        axCurrent.set_title(strFigureTitle, fontdict = None, loc = u'center')
        strColour = 'blue'
        figCurrent.add_axes(axCurrent)
        matAllPoints = np.array(mat1stPlusRotatedPoints)
        intColumns = 3
        matAllPoints = np.reshape(matAllPoints, (-1, intColumns))
        intRows = matAllPoints.shape[0]

        #======================================
        #Re-orientate Points w.r.t. X-Z-Y Axes.
        #======================================
        listX = matAllPoints[:, 0]
        listY = matAllPoints[:, 1]
        listZ = matAllPoints[:, 2]
        intPoints = len(listX)

        #=====================================================================
        #Transform 3D Co-Ordinates to get new 2D Projection onto the XZ Plane.
        #=====================================================================
        listTX, listTZ, _ = proj3d.proj_transform(listX, listZ, listY,
                                                  axCurrent.get_proj())

        #===================
        #Compensate for NaN.
        #===================
        for intIndex in range(listTX.shape[0]):
            #==============================
            #For Transformed X-Coordinates.
            #==============================
            if(self.IsNaN(listTX[intIndex])):
                listTX[intIndex] = 0.000001

            #==============================
            #For Transformed Z-Coordinates.
            #==============================
            if(self.IsNaN(listTZ[intIndex])):
                listTZ[intIndex] = 0.000001

        #======================================================================
        #Plot the Rotated Points in a 3D Scatter Plot. Can't use zdir = 'y' due
        #to Inverted Y-Axis, i.e. +y into Paper.
        #======================================================================
        axCurrent.scatter(listX, listZ, listY, s = 20, c = strColour,
                          depthshade = True)

        #==============================================================
        #Build the Initial Label List by looping through Data Points to
        #initially annotate Scatter Plot and populate the Labels List.
        #==============================================================
        for i in range(intPoints):
            #======================================
            #Build the Label for the Current Point.
            #======================================
            strAnnotation = 'Camera Position at Frame: ' + str(i + 1) + ' [' \
                            + str(int(listX[i])) + ',' + str(int(listY[i])) \
                            + ',' + str(int(listZ[i]))+']'

            labelCurrent = \
                         axCurrent.annotate(strAnnotation, xycoords='data',
                                            xy = (listTX[i], listTZ[i]),
                                            xytext = (-30, 30),
                                            textcoords = 'offset points',
                                            ha = 'right', va = 'top',
                                            fontsize = 6,
                                            bbox = \
                                            dict(boxstyle = \
                                                 'round, pad = 0.5',
                                                 fc = 'yellow',
                                                 alpha = 0.5),
                                            arrowprops = dict(arrowstyle = '->',
                                                              connectionstyle \
                                                              = 'arc3, rad=0'))
            listLabels.append(labelCurrent)

        #===============================================================
        #Rebuild Positions when Mouse Button is released after Rotation.
        #===============================================================
        figCurrent.canvas.mpl_connect('button_release_event', reprojectlabels)

        #===========================
        #Display the Rotated Points.
        #===========================
        pltCurrent.show()

    def dispCamOrient(self, matCamOrient, strFigureTitle, intxMin = -5,
                      intxMax = 5, intyMin = -5, intyMax = 5, intzMin = -5,
                      intzMax = 5):
        def reprojectlabels(event):
            #===============================================================
            #Transform 3D Co-Ordinates to get new 2D Projection onto the XZ
            #Plane.
            #===============================================================
            listTX, listTZ, _ = proj3d.proj_transform(listX, listZ, listY,
                                                      axCurrent.get_proj())

            #===================
            #Compensate for NaN.
            #===================
            for intIndex in range(listTX.shape[0]):
                #==============================
                #For Transformed X-Coordinates.
                #==============================
                if(self.IsNaN(listTX[intIndex])):
                    listTX[intIndex] = 0.00001

                #==============================
                #For Transformed Z-Coordinates.
                #==============================
                if(self.IsNaN(listTZ[intIndex])):
                    listTZ[intIndex] = 0.000001

            #=====================================
            #Compute the updated Label Cordinates.
            #=====================================
            for i in range(len(listX)):
                labelCurrent = listLabels[i]
                labelCurrent.xy = listTX[i], listTZ[i]
                labelCurrent.update_positions(figCurrent.canvas.renderer)
                figCurrent.canvas.draw()

            #==============================
            #Return to the Calling Routine.
            #==============================
            return

        #===============
        #Initialisation.
        #===============
        np.seterr(divide = 'ignore', invalid = 'ignore')
        import matplotlib
        import matplotlib.pyplot as pltCurrent
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d
        import pylab
        import math as ma
        figCurrent = pltCurrent.figure()
        axCurrent = figCurrent.gca(projection = '3d')
        axCurrent.set_xlabel('x')
        axCurrent.set_ylabel('z')
        axCurrent.set_zlabel('y')
        axCurrent.set_xlim(intxMin, intxMax)
        axCurrent.set_ylim(intyMin, intyMax)
        axCurrent.set_zlim(intzMin, intzMax)
        axCurrent.invert_xaxis()
        axCurrent.invert_yaxis()
        axCurrent.invert_zaxis()
        listLabels = []
        uintElevation = 45
        uintAzimuth = 75
        axCurrent.view_init(uintElevation, uintAzimuth)
        axCurrent.set_title(strFigureTitle, fontdict = None, loc = u'center')
        strColour = 'red'
        figCurrent.add_axes(axCurrent)
        matAllPoints = np.array(matCamOrient)
        intColumns = 3
        matAllPoints = np.reshape(matAllPoints, (-1, intColumns))
        intRows = matAllPoints.shape[0]

        #======================================
        #Re-orientate Points w.r.t. X-Z-Y Axes.
        #======================================
        listX = matAllPoints[:, 0]
        listY = matAllPoints[:, 1]
        listZ = matAllPoints[:, 2]
        intPoints = len(listX)

        #=====================================================================
        #Transform 3D Co-Ordinates to get new 2D Projection onto the XZ Plane.
        #=====================================================================
        listTX, listTZ, _ = proj3d.proj_transform(listX, listZ, listY,
                                                  axCurrent.get_proj())

        #===================
        #Compensate for NaN.
        #===================
        for intIndex in range(listTX.shape[0]):
            #==============================
            #For Transformed X-Coordinates.
            #==============================
            if(self.IsNaN(listTX[intIndex])):
                listTX[intIndex] = 0.000001

            #==============================
            #For Transformed Z-Coordinates.
            #==============================
            if(self.IsNaN(listTZ[intIndex])):
                listTZ[intIndex] = 0.000001

        #======================================================================
        #Plot the Rotated Points in a 3D Scatter Plot. Can't use zdir = 'y' due
        #to Inverted Y-Axis, i.e. +y into Paper.
        #======================================================================
        axCurrent.scatter(listX, listZ, listY, s = 20, c = strColour,
                          depthshade = True)

        #==============================================================
        #Build the Initial Label List by looping through Data Points to
        #initially annotate Scatter Plot and populate the Labels List.
        #==============================================================
        for i in range(intPoints):
            #======================================
            #Build the Label for the Current Point.
            #======================================
            labelCurrent = \
                         axCurrent.annotate("k-j-i", xy = (listTX[i],
                                                           listTZ[i]),
                                            xycoords = 'data',
                                            xytext=(0.0, 0.0),
                                            textcoords = 'data',
                                            ha = u'center', va = u'center',
                                            fontsize = 6,
                                            arrowprops =
                                            dict(arrowstyle = "->",
                                                 connectionstyle = "arc3"))

            listLabels.append(labelCurrent)

        #===============================================================
        #Rebuild Positions when Mouse Button is released after Rotation.
        #===============================================================
        figCurrent.canvas.mpl_connect('button_release_event', reprojectlabels)

        #===============================
        #Display the Camera Orientation.
        #===============================
        pltCurrent.show()


    
