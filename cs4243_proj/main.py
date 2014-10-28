#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv

viewport = "image"
view_img = None
mode = None

startPos = None
curPos = (-1, -1)

lines = []
drawingLines = []


def show_image(image, image_title):
    """
    Displays given image
    """
    cv2.namedWindow(image_title)
    cv2.imshow(image_title, image)

def handlePolygonMode(event, x, y, flags, param):
    if mode != 'p':
        return

    global startPos, lines
    if event == cv2.EVENT_MOUSEMOVE:
        pass
    elif event == cv2.EVENT_LBUTTONDOWN:
        print x, y
        if startPos:
            lines.append( [startPos[:], (x, y)] )
            startPos = (x, y)
        else:
            startPos = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        pass

def handleMouseEvents(event, x, y, flags, param):
    global curPos
    curPos = (x, y)
    handlePolygonMode(event, x, y, flags, param)

def handleKeyboardEvents(key):
    # draw polygon mode
    global mode, startPos
    if key == ord('p'):
        print "Polygon mode"
        mode = 'p'
    # selection mode
    elif key == ord('s'):
        print "Selection mode"
        mode = 's'
    # extraction mode
    elif key == ord('e'):
        print "Extraction mode"
        mode = 'e'
    # clear mode
    elif key == ord('c'):
        print "Clear mode"
        mode = None
        startPos = None

def display():
    img = view_img[:]
    for line in lines:
        cv2.line(img, line[0], line[1], (0,255,0,), 2)
    cv2.imshow(viewport, img)




class Project():
    def __init__():
        self._mode = None
        self._view_img = None

    def _mainLoop():
        # main view
        cv2.namedWindow(viewport)
        mode = 'p'

        # callback to handle mouse events
        cv2.setMouseCallback(viewport, handleMouseEvents)

        # initial display
        display()

        # main loop
        while(1):
            # keyboard events
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            handleKeyboardEvents(key)

    def run(image_path):
        self.view_img = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_COLOR)[::-1, ::-1]
        self.view_img = cv2.resize(view_img, (0,0), fx=0.6, fy=0.6)

        mainLoop()

        cv2.destroyAllWindows()
