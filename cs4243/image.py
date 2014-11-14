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
2.1.0     dd/mm/yyyy   ???          Added the following new Methods:
                                    getResizedImage, getXAt, getYAt, setXAt,
                                    setYAt, triangulate, getImageFromCam,
                                    getImageFromCam2
2.2.0     07/11/2014   Dave Tan     Added new Method persProj2. Modified
                                    __init__ Constructor Method to flip the
                                    Image by 180 Degrees for non-Darwin
                                    Platform.
2.3.0     09/11/2014   Toh Zijing   Vectorised Method persProj2.
                       Dave Tan
2.4.0     09/11/2014   Dave Tan     Enhanced persProj2 to include Arguments for
                                    plotting Current Frame Camera Translation
                                    and Rotation. Updated Image Class Sypnosis.
                                    Added new Method plotCamTransAndOrient.
"""

#===============
#Initialisation.
#===============
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

    persProj: This Method is a Vectorised Version of persProj.

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
        #if platform.system() == "Darwin":
        #    self._image = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_COLOR)[::-1,::-1]
        #else:
        self._image = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_COLOR)

        self._view = self._image[:]
        self._view_scale = 0.65

        #Stores x,y,z world coords for each point.
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
        self._grids = None
        self._selected2DPoints = []
        self._selectedPoints = []

    def resetImagePoints(self):
        # stores x,y,z world coords for each point
        t_row, t_col = np.ogrid[0:self._image.shape[0], 0:self._image.shape[1]]
        self._image_points[t_row, t_col, 0] = t_col
        self._image_points[t_row, t_col, 1] = t_row
        self._image_points[t_row, t_col, 2] = 0

    def interpolateImagePoints(self, points):
        t_row, t_col = np.ogrid[0:self._image.shape[0], 0:self._image.shape[1]]

        xCoords = [x[0] for x in points]
        yCoords = [x[1] for x in points]

        xValues = [self.getXAt(*p) for p in points]
        yValues = [self.getYAt(*p) for p in points]
        zValues = [self.getZAt(*p) for p in points]

        interpX = griddata(xCoords, yCoords,
                           xValues,
                           t_col.tolist()[0],
                           t_row.transpose().tolist()[0],
                           "linear")
        self._image_points[t_row, t_col, 0] = interpX

        interpY = griddata(xCoords, yCoords,
                           yValues,
                           t_col.tolist()[0],
                           t_row.transpose().tolist()[0],
                           "linear")
        self._image_points[t_row, t_col, 1] = interpY

        interpZ = griddata(xCoords, yCoords,
                           zValues,
                           t_col.tolist()[0],
                           t_row.transpose().tolist()[0],
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

    def getXAt(self, x, y):
        return self._image_points[y][x][0]

    def getYAt(self, x, y):
        return self._image_points[y][x][1]

    def getZAt(self, x, y):
        return self._image_points[y][x][2]

    def setXAt(self, xValue, x, y ):
        self._image_points[y][x][0] = xValue

    def setYAt(self, yValue, x, y ):
        self._image_points[y][x][1] = yValue

    def setZAt(self, zValue, x, y ):
        self._image_points[y][x][2] = zValue
        
    def convertToImageSpace(self, x, y):
        x *= 1.0/self._view_scale
        y *= 1.0/self._view_scale
        return (int(x), int(y))

    def convertToViewSpace(self, x, y):
        x *= self._view_scale
        y *= self._view_scale
        return (int(x), int(y))

    def gridimage(self, points):
        # setup grid
        xwidth = 51
        ywidth = int(xwidth*(float(self.getHeight())/self.getWidth()))
        x, y = np.meshgrid(range(xwidth),range(ywidth))
        x = ((self.getWidth()-1)/(xwidth-1)) * x.flatten()
        y = ((self.getHeight()-1)/(ywidth-1)) * y.flatten()
        gridPoints = np.array(zip(x, y)).astype(np.float32)

        # compute individual grid points
        grid = np.array(range(xwidth*ywidth)).reshape(ywidth, xwidth)
        p1 = grid[0:-1, 0:-1].reshape((xwidth-1)*(ywidth-1))
        p2 = grid[0:-1, 1:xwidth].reshape((xwidth-1)*(ywidth-1))
        p3 = grid[1:ywidth, 1:xwidth].reshape((xwidth-1)*(ywidth-1))
        p4 = grid[1:ywidth, 0:-1].reshape((xwidth-1)*(ywidth-1))
        self._grids = np.array(zip(p1, p2, p3, p4))

        # setup point values
        self._selected2DPoints = gridPoints
        self._selectedPoints = [(self.getXAt(*p),
                                 self.getYAt(*p),
                                 self.getZAt(*p),) for p in self._selected2DPoints]
        self._selectedPoints = np.array(self._selectedPoints).astype(np.float32)

    def getImageFromCam(self, arrayCamTrans, matCamOrient, int_f, doWireframe=True):
        """
        Drawing using selected points + triangles
        """
        destination = self.persProj(self._selectedPoints,
                                    arrayCamTrans,
                                    matCamOrient,
                                    booShowCamTransAndOrient = False,
                                    int_f = int_f)
        destination = np.array(destination).astype(np.float32)
        destination[:,0] += self.getWidth()/2
        destination[:,1] += self.getHeight()/2

        #check for grids to prune
        mask = np.zeros(self._image.shape, dtype=np.uint8)
        finalMask = np.zeros(self._image.shape, dtype=np.uint8)
        wireframe = np.zeros(self._image.shape, dtype=np.uint8)
        indices_p = set()
        grids_p = []

        for grid in self._grids:
            p1,p2,p3,p4 = [destination[p] for p in grid]
            pset = set([tuple(p1), tuple(p2), tuple(p3), tuple(p4)])

            # skip if all points the same
            if len(pset) <= 2:
                continue

            # skip if back facing
            if (np.cross((p2-p1), (p3-p2)) <= 0 and
                np.cross((p3-p2), (p4-p3)) <= 0):
                continue

            # skip points outside
            pall = np.array([p1,p2,p3,p4])
            if not (((pall[:,0] >= -(self.getWidth()*3)).all() and
                     (pall[:,0] < (self.getWidth()*3)).all()) and
                    ((pall[:,1] >= -(self.getHeight()*3)).all() and
                     (pall[:,1] < (self.getHeight()*3)).all())):
                continue

            [indices_p.add(p) for p in grid]
            grids_p.append(grid)
            cv2.fillPoly(mask,
                         np.array([np.array([self._selected2DPoints[p] for p in grid]).astype(np.int)]),
                         (255, 255, 255))
            cv2.fillPoly(finalMask,
                         np.array([np.array([destination[p] for p in grid]).astype(np.int)]),
                         (255, 255, 255))

            # draw wireframe
            cv2.line(wireframe,
                     tuple(destination[grid[0]]),
                     tuple(destination[grid[1]]),
                     (0,255,0))
            cv2.line(wireframe,
                     tuple(destination[grid[1]]),
                     tuple(destination[grid[2]]),
                     (0,255,0))
            cv2.line(wireframe,
                     tuple(destination[grid[2]]),
                     tuple(destination[grid[3]]),
                     (0,255,0))
            cv2.line(wireframe,
                     tuple(destination[grid[3]]),
                     tuple(destination[grid[0]]),
                     (0,255,0))

            """
            cv2.imshow("TEST", cv2.resize(wireframe, (0,0), fx=0.2, fy=0.2))
            cv2.imshow("TEST2", cv2.resize(cv2.bitwise_and(self._image, mask), (0,0), fx=0.2, fy=0.2))
            print grid
            print [self._selected2DPoints[x] for x in grid]
            print [destination[x] for x in grid]
            cv2.waitKey(0)
            """

        indices_p = sorted(list(indices_p))
        destination_p = np.array([destination[x] for x in indices_p])
        selected2DPoints_p = np.array([self._selected2DPoints[x] for x in indices_p])

        # remap/warp image
        t_row, t_col = np.ogrid[0:self.getHeight(), 0:self.getWidth()]
        interp_x = griddata(destination_p[:,0], destination_p[:,1], selected2DPoints_p[:,0],
                            t_col.tolist()[0], t_row.transpose().tolist()[0],
                            "linear")
        interp_y = griddata(destination_p[:,0], destination_p[:,1], selected2DPoints_p[:,1],
                            t_col.tolist()[0], t_row.transpose().tolist()[0],
                            "linear")
        warped = cv2.remap(cv2.bitwise_and(self._image, mask),
                           interp_x.astype(np.float32),
                           interp_y.astype(np.float32),
                           cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT)

        retImage = cv2.bitwise_and(warped, finalMask)
        if doWireframe:
            retImage = np.maximum(wireframe, retImage)
        return retImage

    def getImageFromCamPoints(self, arrayCamTrans, matCamOrient, int_f):
        """
        Drawing using all points
        """
        skip = 75
        newImage = self._image.reshape((self.getHeight()*self.getWidth(), 3))
        newImage = newImage[0:self.getHeight()*self.getWidth():skip]
        newImagePoints = self._image_points.reshape((self.getHeight()*self.getWidth(), 3))
        newImagePoints = newImagePoints[0:self.getHeight()*self.getWidth():skip]

        uvPoints = self.persProj(newImagePoints,
                                 arrayCamTrans,
                                 matCamOrient,
                                 booShowCamTransAndOrient = False,
                                 int_f = int_f).astype(np.float32)
        uvPoints[:,0] += self.getWidth()/2
        uvPoints[:,1] += self.getHeight()/2

        retImage = np.zeros_like(self._image)
        for index, point in enumerate(uvPoints):
            point = tuple(np.array(point).flatten())
            color = tuple([int(x) for x in newImage[index]])
            try:
                cv2.circle(retImage, point, 2, color)
            except OverflowError:
                continue
            except ValueError:
                continue
        return retImage

    def persProj(self, array3DScPts, arrayCamTrans, matCamOrient,
                 booShowCamTransAndOrient = False,
                 strCamTransFigTitle = "Current Frame Camera Translation",
                 strCamOrientFigTitle = "Current Frame Camera Orientation",
                 int_f = 1, int_u0 = 0, int_bu = 1, int_ku = 1, int_v0 = 0,
                 int_bv = 1, int_kv = 1):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        i_f = np.transpose(matCamOrient[0, :])
        j_f = np.transpose(matCamOrient[1, :])
        k_f = np.transpose(matCamOrient[2, :])
        intRows = array3DScPts.shape[0]

        #=============================
        #Compute the (sp - tf) Matrix.
        #=============================
        sp_minus_tf = (array3DScPts - arrayCamTrans)

        #====
        #ufp.
        #====
        fltNumerator = int_f * np.dot(sp_minus_tf, i_f)
        fltDenominator = np.dot(sp_minus_tf, k_f)
        ufp = fltNumerator / fltDenominator

        #====
        #vfp.
        #====
        fltNumerator = int_f * np.dot(sp_minus_tf, j_f)
        fltDenominator = np.dot(sp_minus_tf, k_f)
        vfp = fltNumerator / fltDenominator

        matProjPts = np.array(zip(ufp, vfp))

        #==========================================================
        #Plot the Current Frame Camera Translation and Orientation.
        #==========================================================
        if(booShowCamTransAndOrient):
            self.plotCamTransAndOrient(arrayCamTrans, strCamTransFigTitle,
                                       matCamOrient, strCamOrientFigTitle)
        
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

    def plotCamTransAndOrient(self, arrayCFCamTrans, strCamTransFigTitle,
                              arrayCFCamOrient, strCamOrientFigTitle):
        #========================
        #Camera Translation Plot.
        #========================
        self.dispCamTrans(arrayCFCamTrans, strCamTransFigTitle)

        #========================
        #Camera Orientation Plot.
        #========================
        self.dispCamOrient(arrayCFCamOrient, strCamOrientFigTitle)

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

        
    def _normalise(self, listInput):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        import math as ma
        intLength = len(listInput)
        listInput_normalised = np.zeros(intLength)
        listInput_mag_square = \
                             sum(fltElement * fltElement\
                                 for fltElement in listInput)
        listInput_mag = ma.sqrt(listInput_mag_square)

        #==========================
        #Perform the Normalisation.
        #==========================
        for intIndex in range(0, intLength, 1):
            listInput_normalised[intIndex] = listInput[intIndex] / listInput_mag

        #=============================
        #Return the Normalised Vector.
        #=============================
        return(listInput_normalised)

    def _quatConj(self, q):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        sq = q[0]
        vq = [0, 0, 0]
        neg_vq = [0, 0, 0]
        vq[0] = q[1]
        vq[1] = q[2]
        vq[2] = q[3]
        neg_vq[0] = -1 * vq[0]
        neg_vq[1] = -1 * vq[1]
        neg_vq[2] = -1 * vq[2]

        #======================
        #Compute the Conjugate.
        #======================
        q_conj = np.append(sq, neg_vq)

        #=======================================
        #Return the Conjugate of the Quaternion.
        #=======================================
        return(q_conj)

    def _point2Quat(self, arrPointVector):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        sq = 0
        vq = arrPointVector

        #======================================
        #Compose the Quaternion Representation.
        #======================================
        q = np.append(sq, vq)
        vq = q[1:]

        #===================
        #Return the Outputs.
        #===================
        return(sq, vq, q)

    def _rot2Quat(self, fltTheta, wx, wy, wz):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        import math as ma
        wx, wy, wz = self._normalise([wx, wy, wz])
        vq = np.zeros([1, 3])
        fltTheta_radians = ma.radians(fltTheta)

        #=============================
        #Compute the Scalar Component.
        #=============================
        sq = ma.cos(fltTheta_radians / 2)

        #=============================
        #Compute the Vector Component.
        #=============================
        vq[0, 0] = ma.sin(fltTheta_radians / 2) * wx
        vq[0, 1] = ma.sin(fltTheta_radians / 2) * wy
        vq[0, 2] = ma.sin(fltTheta_radians / 2) * wz

        #========================================================
        #Construct the Quaternion Representation of the Rotation.
        #========================================================
        q = np.append(sq, vq)

        #===============================================================
        #Return the Quarternion Representation of the Rotation provided.
        #===============================================================
        return(sq, vq, q)

    def _quatMult(self, q1, q2):
        #===============
        #Initialisation.
        #===============
        out = [0, 0, 0, 0]
        q1_0 = q1[0]
        q1_1 = q1[1]
        q1_2 = q1[2]
        q1_3 = q1[3]
        q2_0 = q2[0]
        q2_1 = q2[1]
        q2_2 = q2[2]
        q2_3 = q2[3]

        #======================================
        #Perform the Quaternion Multiplication.
        #======================================
        out[0] = (q1_0 * q2_0) - (q1_1 * q2_1) - (q1_2 * q2_2) - (q1_3 * q2_3)
        out[1] = (q1_0 * q2_1) + (q1_1 * q2_0) + (q1_2 * q2_3) - (q1_3 * q2_2)
        out[2] = (q1_0 * q2_2) - (q1_1 * q2_3) + (q1_2 * q2_0) + (q1_3 * q2_1)
        out[3] = (q1_0 * q2_3) + (q1_1 * q2_2) - (q1_2 * q2_1) + (q1_3 * q2_0)

        #==================
        #Return the Result.
        #==================
        return out

    def _quat2Rot(self, q):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        Rq = np.zeros([3, 3])
        q = self._normalise(q)
        q_0 = q[0]
        q_1 = q[1]
        q_2 = q[2]
        q_3 = q[3]

        #============================
        #Compute the Rotation Matrix.
        #============================
        Rq[0, 0] = (q_0 * q_0) + (q_1 * q_1) - (q_2 * q_2) - (q_3 * q_3)
        Rq[0, 1] = 2 * ((q_1 * q_2) - (q_0 * q_3))
        Rq[0, 2] = 2 * ((q_1 * q_3) + (q_0 * q_2))
        Rq[1, 0] = 2 * ((q_1 * q_2) + (q_0 * q_3))
        Rq[1, 1] = (q_0 * q_0) + (q_2 * q_2) - (q_1 * q_1) - (q_3 * q_3)
        Rq[1, 2] = 2 * ((q_2 * q_3) - (q_0 * q_1))
        Rq[2, 0] = 2 * ((q_1 * q_3) - (q_0 * q_2))
        Rq[2, 1] = 2 * ((q_2 * q_3) + (q_0 * q_1))
        Rq[2, 2] = (q_0 * q_0) + (q_3 * q_3) - (q_1 * q_1) - (q_2 * q_2)

        #===========================
        #Return the Rotation Matrix.
        #===========================
        return Rq

    def _rotByQuatMult(self, pt, fltTheta, wx, wy, wz, intIterations):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        matRotatedPoints = np.zeros([1, 3])
        pt2rot = pt

        #===================================================================
        #Perform the Rotation using Quaternion Multiplications and store the
        #Rotated Points in an Array containing the Rotated Points.
        #===================================================================
        for intIndex in range(0, intIterations, 1):
            #======================================================
            #Perform the Rotation using Quaternion Multiplications.
            #======================================================
            sp, vp, p = self._point2Quat(pt2rot)
            sq, vq, q = self._rot2Quat(fltTheta, wx, wy, wz)
            q_conj = self._quatConj(q)
            qp = self._quatMult(q, p)
            p_rot = self._quatMult(qp, q_conj)

            #============================================================
            #Store the Rotated Point, discard the Scalar Portion of qpq*.
            #============================================================
            if(intIndex == 0):
                #====================
                #First Rotated Point.
                #====================
                matRotatedPoints[0, 0] = p_rot[1]
                matRotatedPoints[0, 1] = p_rot[2]
                matRotatedPoints[0, 2] = p_rot[3]
            else:
                #=========================
                #Subsequent Rotated Point.
                #=========================
                arrayTemp = [0, 0, 0]
                arrayTemp[0] = p_rot[1]
                arrayTemp[1] = p_rot[2]
                arrayTemp[2] = p_rot[3]
                matRotatedPoints = np.append([matRotatedPoints], [arrayTemp])

            #==================================
            #Change Starting Point of Rotation.
            #==================================
            pt2rot = [p_rot[1], p_rot[2], p_rot[3]]
            arrayTemp = np.zeros([1, 3])

        #===============================================
        #Return the Array containing the Rotated Points.
        #===============================================
        matRotatedPoints = np.matrix(matRotatedPoints)
        intRows = matRotatedPoints.shape[0]
        intColumns = matRotatedPoints.shape[1]
        intElements = intRows * intColumns
        intNewRows = int(intElements / 3)
        matRotatedPoints = np.reshape(matRotatedPoints, (intNewRows, 3))
        return(matRotatedPoints)

    def _rotByRotMat(self, matCamFr, fltTheta, wx, wy, wz, intIterations):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        matCamFr = np.matrix(matCamFr)
        matCurrentCamFr = np.zeros([3, 3])

        #===============================
        #Obtain the Rotation Quaternion.
        #===============================
        s_qrot, v_qrot, q_rot = self._rot2Quat(fltTheta, wx, wy, wz)
        matRot = np.matrix(self._quat2Rot(q_rot))

        #=======================================================================
        #Perform the Rotation using Matrix Multiplications and store the Rotated
        #Camera Orientations in an n x 3 Array containing the Rotated Points.
        #=======================================================================
        for intIndex in range(0, intIterations, 1):
            #==================================================================
            #Perform the Matrix Multiplication utilisating the Rotation Matrix.
            #==================================================================
            for intSquareIndex in range(0, 3, 1):
                listPt = matCamFr[intSquareIndex, :]
                matNewCamPt = matRot * np.transpose(listPt)
                matCurrentCamFr[intSquareIndex, :] = np.transpose(matNewCamPt)

                #===============================================
                #Store the Rotated Camera Orientation of Points.
                #===============================================
                if(intIndex == 0):
                    #===========================================
                    #First Rotated Camera Orientation of Points.
                    #===========================================
                    matRotatedPoints = matCurrentCamFr
                else:
                    #================================================
                    #Subsequent Rotated Camera Orientation of Points.
                    #================================================
                    matRotatedPoints = np.append([matRotatedPoints],
                                                 matCurrentCamFr)

            #==================================
            #Change Starting Point of Rotation.
            #==================================
            matCamFr = matCurrentCamFr

        #===============================================
        #Return the Array containing the Rotated Points.
        #===============================================
        matRotatedPoints = np.matrix(matRotatedPoints)
        intRows = matRotatedPoints.shape[0]
        intColumns = matRotatedPoints.shape[1]
        intElements = intRows * intColumns
        intNewRows = int(intElements / 3)
        matRotatedPoints = np.reshape(matRotatedPoints, (intNewRows, 3))
        return(matRotatedPoints)

    def _rotByImage(self, objImage3D, fltTheta, wx, wy, wz, intIterations = 1):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        listRotated3DScene = objImage3D._flat_3dpoints

        #===============================
        #Obtain the Rotation Quaternion.
        #===============================
        s_qrot, v_qrot, q_rot = self._rot2Quat(fltTheta, wx, wy, wz)
        matRot = np.matrix(self._quat2Rot(q_rot))

        #===========================================
        #Perform the Rotation using Rotation Matrix.
        #===========================================
        listRotated3DScene = matRot * np.transpose(listRotated3DScene)

        #==========================
        #Return the Rotated Points.
        #==========================
        return(np.transpose(listRotated3DScene))


    
