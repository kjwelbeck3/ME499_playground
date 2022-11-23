from email.utils import parseaddr
from tkinter.font import families
import apriltag
import cv2
import argparse
from matplotlib import pyplot as plt
import numpy as np


class puckTracker:
    def __init__(self, puck_tag_family="tag36h11", stage_tag_family="tag25h9"):

        puck_options = apriltag.DetectorOptions(families=puck_tag_family)
        self.puck_detector = apriltag.Detector(puck_options)

        stage_options = apriltag.DetectorOptions(families=stage_tag_family)
        self.stage_detector = apriltag.Detector(stage_options)

        self.perspective_correction = False

    def locatePuck(self, rgb_img, showLoc=False):
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)
        results = self.puck_detector.detect(gray_img)

        if len(results) == 0:
            return {}

        puck = results[0]
        ptA, ptB, ptC, ptD = puck.corners
        ptA = int(ptA[0]), int(ptA[1]) 
        ptB = int(ptB[0]), int(ptB[1]) 
        ptC = int(ptC[0]), int(ptC[1]) 
        ptD = int(ptD[0]), int(ptD[1]) 
        centroid = (int(puck.center[0]), int(puck.center[1]))

        loc = {
            "corners": [ptA, ptB, ptC, ptD],
            "center": centroid,
            }

        if showLoc:
            cv2.line(rgb_img, ptA, ptB, (0, 255, 0), 2)
            cv2.line(rgb_img, ptB, ptC, (0, 255, 0), 2)
            cv2.line(rgb_img, ptC, ptD, (0, 255, 0), 2)
            cv2.line(rgb_img, ptD, ptA, (0, 255, 0), 2)
            cv2.circle(rgb_img, centroid, 5, (0, 0, 255), -1)
            cv2.imshow("Puck Location", rgb_img)
            cv2.waitKey(0)

        return loc

    def locateCircles(self, rgb_img, showLoc=False):
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)
        gray_img = cv2.medianBlur(gray_img, 3)
        rows = gray_img.shape[0]

        circles =  cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, rows/5,  minRadius=100, maxRadius=340)#,minRadius=20, maxRadius=100)
        if circles is not None:
            circles = np.uint16(np.around(circles))[0,:]

            if showLoc:
                for c in circles:
                    center = (c[0], c[1])
                    cv2.circle(rgb_img, center, 1, (0, 100, 100), 3)
                    
                    radius = c[2]
                    cv2.circle(rgb_img, center, radius, (255, 0, 255), 3)
                
                cv2.imshow("Detected Circles", rgb_img)
                cv2.waitKey(0)

        

        return circles, rgb_img  ## TODO may me memory intensive to keep returing images 

    # def locateGreenPuck(self):
        # pass


    def locateStage(self, rgb_img, showTags=False):

        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)
        results = self.stage_detector.detect(gray_img)

        if len(results) == 0:
            return (False, "Found None")
        
        if len(results) < 3:
            return (False, 'Found {} stage tags'.format(len(results)))

        tagLocs = [] 
        for tag in results:

            ptA, ptB, ptC, ptD = tag.corners
            ptA = int(ptA[0]), int(ptA[1]) 
            ptB = int(ptB[0]), int(ptB[1]) 
            ptC = int(ptC[0]), int(ptC[1]) 
            ptD = int(ptD[0]), int(ptD[1]) 
            centroid = (int(tag.center[0]), int(tag.center[1]))

            loc = {
                "corners": [ptA, ptB, ptC, ptD],
                "center": centroid,
                }
            tagLocs.append(loc)

            if showTags:
                cv2.line(rgb_img, ptA, ptB, (0, 255, 0), 2)
                cv2.line(rgb_img, ptB, ptC, (0, 255, 0), 2)
                cv2.line(rgb_img, ptC, ptD, (0, 255, 0), 2)
                cv2.line(rgb_img, ptD, ptA, (0, 255, 0), 2)
                cv2.circle(rgb_img, centroid, 5, (0, 0, 255), -1)

        if showTags:
            cv2.imshow("Stage Tag Locations", rgb_img)
            cv2.waitKey(0)

        return True, tagLocs

    def overlayTagLocs(self, rgb_img, tagLocs):

        ptA = tagLocs[0]["center"]
        ptB = tagLocs[1]["center"]
        ptC = tagLocs[2]["center"]
        ptA, ptB, ptC = orderABC([ptA, ptB, ptC])
        ptD = calcD([ptA, ptB, ptC])

            
        cv2.line(rgb_img, ptA, ptB, (255, 0, 0), 2)
        cv2.line(rgb_img, ptB, ptC, (255, 0, 0), 2)
        cv2.line(rgb_img, ptC, ptD, (255, 0, 0), 2)
        cv2.line(rgb_img, ptD, ptA, (255, 0, 0), 2)

        # cv2.imshow("Stage Location", rgb_img)
        # cv2.waitKey(0)
        pass

    def frameStage(self, img, tagLocs):
        ptA = tagLocs[0]["center"]
        ptB = tagLocs[1]["center"]
        ptC = tagLocs[2]["center"]
        ptA, ptB, ptC = orderABC([ptA, ptB, ptC])
        ptD = calcD([ptA, ptB, ptC])
        
        cv2.line(img, ptA, ptB, (255, 0, 0), 2)
        cv2.line(img, ptB, ptC, (255, 0, 0), 2)
        cv2.line(img, ptC, ptD, (255, 0, 0), 2)
        cv2.line(img, ptD, ptA, (255, 0, 0), 2) 
        cv2.imshow("Framed Stage", img)
        cv2.waitKey(0) 

        return img, [ptA, ptB, ptC, ptD]

    def framePuck(self, img, loc):
        ptA, ptB, ptC, ptD = loc["corners"]
        cv2.line(img, ptA, ptB, (0, 255, 0), 2)
        cv2.line(img, ptB, ptC, (0, 255, 0), 2)
        cv2.line(img, ptC, ptD, (0, 255, 0), 2)
        cv2.line(img, ptD, ptA, (0, 255, 0), 2)

        cv2.circle(img, loc["center"], 5, (0, 0, 255), 3)

        return img

    def correctPerspective(self, img, rawPts=None, dist=1000, stageDimensions=(7.45, 6.875), showCorrection=False, overrideTransform=False):
        dx_dy = stageDimensions[1]/stageDimensions[0]

        if overrideTransform:    
            raw = map(lambda pt: [pt[0], pt[1]], rawPts)
            # raw = np.float32(list(raw))
            # ref = np.float32([[0,0], [0, 923], [dist, 923], [dist, 0]])
            raw = np.float32(list(raw))
            ref = np.float32([[0,0], [0, int(dist*dx_dy)], [dist, int(dist*dx_dy)], [dist, 0]])

            self.perspective_correction = cv2.getPerspectiveTransform(raw, ref)

        
        newImg = cv2.warpPerspective(img, self.perspective_correction, (dist, int(dist*dx_dy)))
        if showCorrection:
            plt.subplot(121),plt.imshow(img),plt.title('Input')
            plt.subplot(122),plt.imshow(newImg),plt.title('Output')
            plt.show()

        return newImg

    
    def placeGrid(self, image, x_offset, y_offset, x_divs, y_divs, showGrid=False):
        height, width = image.shape[:2]

        grid = {
            "x": np.linspace(x_offset, width-x_offset, x_divs+1).astype(int),
            "y": np.linspace(y_offset, height-y_offset, y_divs+1).astype(int),
            "dx": int((width - x_offset *2)/x_divs),
            "dy": int((height - y_offset *2)/y_divs)
            }

        if showGrid:
            for x in grid["x"]:
                cv2.line(image, (x, grid["y"][0]), (x,grid["y"][-1]), (255, 0, 0), 4)
            for y in grid["y"]:
                cv2.line(image, (grid["x"][0], y), (grid["x"][-1], y), (0, 0, 255), 4)

            cv2.imshow("Gridded Stage", image)
            cv2.waitKey(0)     

        return grid, image

    def locateSubgrid(self, image, grid, centroid, showSubgrid=False):
        x_loc, y_loc = centroid
        x_start, y_start = grid["x"][0], grid["y"][0]
        cell_x, cell_y = int((x_loc - x_start)/grid["dx"]), int((y_loc - y_start)/grid["dy"])

        subgrid_cells = {
            "start": (max(cell_x-2, 0), max(cell_y-2, 0)),
            "end": (min(cell_x+3, len(grid["x"])-1), min(cell_y+3, len(grid["y"])-1))
            }

        subgrid_px = {
            "start": (grid["x"][subgrid_cells["start"][0]], grid["y"][subgrid_cells["start"][1]]),
            "end": (grid["x"][subgrid_cells["end"][0]], grid["y"][subgrid_cells["end"][1]])
        }

        # print(subgrid_px)

        # subgrid_px = {
        #     "start": (2,2),
        #     "end": (500,500)
        # }

        
        
        if showSubgrid:
            cv2.rectangle(image, subgrid_px["start"], subgrid_px["end"], (123,123,0), 2)
            cv2.imshow("SubGrid", image)
            cv2.waitKey(0)
        
        return (cell_x, cell_y), subgrid_cells, subgrid_px, image


    def crop2Stage(self, rgb_img, showLoc):
        pass


    def showImg(image, corner):
        pass


def orderABC(ptsList):
    """ Order in x; order first two in y"""

    ptsList.sort(key=lambda pt : np.linalg.norm([pt[0]+ pt[1]]))
    return ptsList

def calcD(ordered_ptsList):
    
    ptA, ptB, ptC = ordered_ptsList
    dx = ptA[0] - ptB[0]
    dy = ptA[1] - ptB[1]

    ptD = (ptC[0] + dx, ptC[1] + dy)
    return ptD


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", default="/home/kjw/fall22/ME499 Research/PictureSamples/test5.png", help="path to input image containing aprilTag") #required=True
    ap.add_argument("-m", "--mode", default="puck", help="specifiy detection mode: 'stage' or 'puck'")
    args = vars(ap.parse_args())
    
    test_image = cv2.imread(args["image"])

    pT = puckTracker()    
    if args["mode"] == 'puck':
        # pT = puckTracker()
        loc = pT.locatePuck(test_image, True)
        print(loc)

    elif args["mode"] == 'stage':
        # pT = puckTracker(stage_tag_family="tag36h11")
        _, res = pT.locateStage(test_image, True)
        print(res)

    elif args["mode"] == 'transducers':
        circles, _ = pT.locateCircles(test_image, True)
        print(circles)

    elif args["mode"] == "grid-up":
        grid, _ = pT.placeGrid(test_image, 23, 60, 12, 10, True)
        
    elif args["mode"] == "subgrid":
        centroid = pT.locatePuck(test_image)
        print(centroid["center"])
        grid, _ = pT.placeGrid(test_image, 23, 60, 12, 10)
        pT.framePuck(test_image, centroid)
        cell, subgrid_cells, subgrid_px, _ = pT.locateSubgrid(test_image, grid, centroid["center"], True)

        mask = np.zeros((len(grid["y"])-1, len(grid["x"])-1))
        mask[subgrid_cells["start"][1]:subgrid_cells["end"][1], subgrid_cells["start"][0]:subgrid_cells["end"][0]] = 1
        print(mask)

        
