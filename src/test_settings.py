from __future__ import print_function
import cv2
import argparse
import numpy as np
import sys
import marker_dectection
import find_marker
import setting


rescale = int(sys.argv[1])
low_x0 = 0
low_y0 = 0
low_dx = 0
low_dy = 0
low_rescale = 1
max_x0 = 1080 / rescale
max_y0 = 1920 / rescale
max_dx = 40
max_dy = 40
max_rescale = 10
window_capture_name = 'Video Capture'
window_setting_name = 'Setting'
x0_name = 'x0'
y0_name = 'y0'
dx_name = 'dx'
dy_name = 'dy'
rescale_name = 'Rescale'


def rescale_trackbar(val):
    cv2.setTrackbarPos(rescale_name, window_setting_name, val)

def x0_trackbar(val):
    global low_x0
    low_x0 = val
    cv2.setTrackbarPos(x0_name, window_setting_name, low_x0)

def y0_trackbar(val):
    global low_y0
    low_y0 = val
    cv2.setTrackbarPos(y0_name, window_setting_name, low_y0)

def dx_trackbar(val):
    global low_dx
    low_dx = val
    cv2.setTrackbarPos(dx_name, window_setting_name, low_dx)

def dy_trackbar(val):
    global low_dy
    low_dy = val
    cv2.setTrackbarPos(dy_name, window_setting_name, low_dy)

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_setting_name)
cv2.createTrackbar(x0_name, window_setting_name, low_x0, max_x0, x0_trackbar)
cv2.createTrackbar(y0_name, window_setting_name, low_y0, max_y0, y0_trackbar)
cv2.createTrackbar(dx_name, window_setting_name, low_dx, max_dx, dx_trackbar)
cv2.createTrackbar(dy_name, window_setting_name, low_dy, max_dy, dy_trackbar)

cap = cv2.VideoCapture(0, cv2.CAP_V4L)
# cap = cv2.VideoCapture(0)
cap.set(3, int(1080 / rescale))
cap.set(4, int(1920 / rescale))

while True:
    m = find_marker.Matching(
        N_=8, 
        M_=14, 
        fps_=30, 
        x0_=low_x0, 
        y0_=low_y0, 
        dx_=low_dx, 
        dy_=low_dy)

    setting.init(1,rescale)

    ret, frame = cap.read()
    if frame is None:
        break

    scale = 22
    blur = cv2.GaussianBlur(frame, (int(scale/3), int(scale/3)), 0)

    # subtract the surrounding pixels to magnify difference between markers and background
    diff = frame.astype(np.float32) - blur
    
    diff *= 4.0
    diff[diff<0.] = 0.
    diff[diff>255.] = 255.
    diff = cv2.GaussianBlur(diff, (int(scale/3), int(scale/3)), 0)
    #cv2.imshow("diff", diff)

    # Switch image from BGR colorspace to HSV
    hsv = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2HSV)

    #frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    yellowMin = (0, 125, 12)
    yellowMax = (50, 255, 50)
    mask = cv2.inRange(hsv, yellowMin, yellowMax)

    mc = marker_dectection.marker_center(mask, frame)

    m.init(mc)
    m.run()
    flow = m.get_flow()
    marker_dectection.draw_flow(frame, flow)

    cv2.imshow(window_capture_name, frame)
    cv2.imshow(window_setting_name, frame)
    
    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break