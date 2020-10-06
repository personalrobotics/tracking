from __future__ import print_function
import cv2
import argparse
import numpy as np
import sys
import marker_dectection
import find_marker
import setting

# max_value = 255
# max_value_H = 360//2
# low_H = 0
# low_S = 0
# low_V = 0
# high_H = max_value_H
# high_S = max_value
# high_V = max_value
# window_capture_name = 'Video Capture'
# window_detection_name = 'Object Detection'
# low_H_name = 'Low H'
# low_S_name = 'Low S'
# low_V_name = 'Low V'
# high_H_name = 'High H'
# high_S_name = 'High S'
# high_V_name = 'High V'


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


# def on_low_H_thresh_trackbar(val):
#     global low_H
#     global high_H
#     low_H = val
#     low_H = min(high_H-1, low_H)
#     cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
# def on_high_H_thresh_trackbar(val):
#     global low_H
#     global high_H
#     high_H = val
#     high_H = max(high_H, low_H+1)
#     cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
# def on_low_S_thresh_trackbar(val):
#     global low_S
#     global high_S
#     low_S = val
#     low_S = min(high_S-1, low_S)
#     cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
# def on_high_S_thresh_trackbar(val):
#     global low_S
#     global high_S
#     high_S = val
#     high_S = max(high_S, low_S+1)
#     cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
# def on_low_V_thresh_trackbar(val):
#     global low_V
#     global high_V
#     low_V = val
#     low_V = min(high_V-1, low_V)
#     cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
# def on_high_V_thresh_trackbar(val):
#     global low_V
#     global high_V
#     high_V = val
#     high_V = max(high_V, low_V+1)
#     cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_setting_name)
# cv.createTrackbar(rescale_name, window_setting_name, low_rescale, max_rescale, rescale_trackbar)
cv2.createTrackbar(x0_name, window_setting_name, low_x0, max_x0, x0_trackbar)
cv2.createTrackbar(y0_name, window_setting_name, low_y0, max_y0, y0_trackbar)
cv2.createTrackbar(dx_name, window_setting_name, low_dx, max_dx, dx_trackbar)
cv2.createTrackbar(dy_name, window_setting_name, low_dy, max_dy, dy_trackbar)


# cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
# cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
# cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
# cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
# cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
# cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

cap = cv2.VideoCapture(0, cv2.CAP_V4L)
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