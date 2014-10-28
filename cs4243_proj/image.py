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
"""

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
    
    persproj: This Method performs the Perspective Projection and returns the 2D
    Array containing the Projected Points.

    plotproj: This Method names the Plot of the 2 x 2 SubPlots according to the
    Title provided. This Function is used to plot the Perspective Projection of
    4 Frames.
    """
    
    #======================
    #Properties/Attributes.
    #======================
    intAttribute = None
    
    #========
    #Methods.
    #========
    def __init__(self):
        #===================
        #Constructor Method.
        #===================
        self.intAttribute = 1
        print "intAttribute initialised to: " + str(self.intAttribute)

    def persproj(self, array3DScPts, arrayCamTrans, matCamOrient, int_f = 1,
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

    def plotproj(self, strPlotTitle, arrayFr1PersProj, arrayFr2PersProj,
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

    

    
