#!/usr/bin/env python

import find_marker
import numpy as np
import cv2
import time
import marker_dectection
import marker_displacement
import sys
import setting
import rospy
from geometry_msgs.msg import Wrench, WrenchStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

## Action Server
import actionlib
import pr_control_msgs.msg

class tareAction(object):
    # No feedback
    #_feedback = 

    _result = pr_control_msgs.msg.TriggerAction
    # ^ DEFINITEL WRONG

    def __init__(self, name):
        self._action_name = "/forque/bias_controller/trigger"
        self._as = actionlib.SimpleActionServer(self._action_name, pr_control_msgs.msg.TriggerAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()

    def execute_cb(self, goal):
        #self._result.success = True
        success = True
        self._result.message = "I failed"

        rospy.loginfo('Taring Gelslight Sensor')

        global m
        m = find_marker.Matching(
            N_=setting.N_, 
            M_=setting.M_, 
            fps_=setting.fps_, 
            x0_=setting.x0_, 
            y0_=setting.y0_, 
            dx_=setting.dx_, 
            dy_=setting.dy_)

        # TODO: Check if it really succeeded
        if success:
            self._result.message = ""
            self._result.success = True
            rospy.loginfo("Completed Taring GelSligt Sensor")
            # self._as.publish_feedback(self._feedback)
            self._as.set_succeeded(self._result)

def gelsightTare(setting):
    m = find_marker.Matching(
        N_=setting.N_, 
        M_=setting.M_, 
        fps_=setting.fps_, 
        x0_=setting.x0_, 
        y0_=setting.y0_, 
        dx_=setting.dx_, 
        dy_=setting.dy_)
    return m


##### ROS COMMENT
rospy.init_node('gelsight', anonymous=True)
server = tareAction(rospy.get_name())
# pub = rospy.Publisher('gs_ft_{}'.format(sys.argv[1]), WrenchStamped, queue_size=10)
# pub = rospy.Publisher('gs_ft_1', WrenchStamped, queue_size=10)
pub = rospy.Publisher('forque/forqueSensor', WrenchStamped, queue_size=10)
marker_wrench = WrenchStamped()
#camera_pub = rospy.Publisher('gs_cam_{}'.format(sys.argv[1]), Image, queue_size=10)
raw_camera_pub = rospy.Publisher('gs_raw_cam_1', Image, queue_size=10)
camera_pub = rospy.Publisher('gs_cam_1', Image, queue_size=10)
br = CvBridge()
marker_wrench.wrench.force.x = 0
marker_wrench.wrench.force.y = 0
marker_wrench.wrench.force.z = 0
marker_wrench.wrench.torque.x = 0
marker_wrench.wrench.torque.y = 0
marker_wrench.wrench.torque.z = 0

calibrate = False

if len(sys.argv) > 1:
    if sys.argv[1] == 'calibrate':
        calibrate = True

both_fingers_flag = False
rescale = 2
# Use both sensors
if int(sys.argv[1] == 2):
    rescale = 3
    both_fingers_flag = True
# Define rescale
if len(sys.argv) == 3:
    rescale = float(sys.argv[2])


#gelsight_version = 'Bnz'
gelsight_version = 'HSR'

# NOTE: Camera order depends on order of plugging
if not both_fingers_flag:
    cap = cv2.VideoCapture(0, cv2.CAP_V4L)
    cap.set(3, int(1080 / rescale))
    cap.set(4, int(1920 / rescale))
    try: 
        setting.init(1, rescale)
    except ValueError: 
        print "Invalid number of arguments passed"

    # Create Mathing Class
    m = find_marker.Matching(
        N_=setting.N_, 
        M_=setting.M_, 
        fps_=setting.fps_, 
        x0_=setting.x0_, 
        y0_=setting.y0_, 
        dx_=setting.dx_, 
        dy_=setting.dy_)

else:
    cap = cv2.VideoCapture(1, cv2.CAP_V4L)
    cap.set(3, int(1080 / rescale))
    cap.set(4, int(1920 / rescale))
    cap2 = cv2.VideoCapture(0, cv2.CAP_V4L)
    cap2.set(3, int(1080 / rescale))
    cap2.set(4, int(1920 / rescale))

    try: 
        setting.init(1, rescale)
    except ValueError: 
        print "Invalid number of arguments passed"

    # Create Mathing Class
    m = find_marker.Matching(
        N_=setting.N_, 
        M_=setting.M_, 
        fps_=setting.fps_, 
        x0_=setting.x0_, 
        y0_=setting.y0_, 
        dx_=setting.dx_, 
        dy_=setting.dy_)

    try: 
        setting.init(2, rescale)
    except ValueError: 
        print "Invalid number of arguments passed"

    # Create Mathing Class
    m2 = find_marker.Matching(
        N_=setting.N_, 
        M_=setting.M_, 
        fps_=setting.fps_, 
        x0_=setting.x0_, 
        y0_=setting.y0_, 
        dx_=setting.dx_, 
        dy_=setting.dy_)

"""
N_, M_: the row and column of the marker array
x0_, y0_: the coordinate of upper-left marker
dx_, dy_: the horizontal and vertical interval between adjacent markers
"""

# save video
#fourcc = cv2.VideoWriter_fourcc(*'XVID')

'''
if gelsight_version == 'HSR':
    out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (640,480))
else:
    #out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (1280//RESCALE,720//RESCALE))
    out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (1280//RESCALE,960//RESCALE))
'''

frameid = 0
while(True):
    # tm = time.time()
    # capture frame-by-frame

    ret, frame = cap.read()
    # cv2.imshow('frame',frame)
    frame_raw = frame.copy()

    if not(ret): 
        break

    # resize (or unwarp)
    if gelsight_version == 'HSR':
        frame = marker_dectection.init_HSR_full(frame, balance=1)
    else:
        frame = marker_dectection.init(frame)

    # find marker masks
    mask = marker_dectection.find_marker(frame)
    # cv2.imshow("Mask", mask2)
    # find marker centers
    mc = marker_dectection.marker_center(mask, frame)

    if both_fingers_flag:
        ret2, frame2 = cap2.read()
        cv2.imshow('frame2',frame2)
        if not(ret2): 
            break
        if gelsight_version == 'HSR':
            # frame = marker_dectection.init_HSR_full(frame, balance=1)
            frame2 = marker_dectection.init_HSR_full(frame2, balance=1)
        else:
            # frame = marker_dectection.init(frame)
            frame2 = marker_dectection.init(frame2)

        mask2 = marker_dectection.find_marker(frame2)
        mc2 = marker_dectection.marker_center(mask2, frame2)


    if calibrate == False:
        # # matching init
        m.init(mc)
        
        # # matching
        m.run()
        
        #print("dt: {}".format(time.time() - tm))
        # print(len(mc))
    
        # # matching result
        """
        output: (Ox, Oy, Cx, Cy, Occupied) = flow
            Ox, Oy: N*M matrix, the x and y coordinate of each marker at frame 0
            Cx, Cy: N*M matrix, the x and y coordinate of each marker at current frame
            Occupied: N*M matrix, the index of the marker at each position, -1 means inferred. 
                e.g. Occupied[i][j] = k, meaning the marker mc[k] lies in row i, column j.
        """
        flow = m.get_flow()
        
        # # draw flow
        marker_dectection.draw_flow(frame, flow)
        

        if both_fingers_flag:
            m2.init(mc2)
            m2.run()
            print(len(mc2))
            flow2 = m2.get_flow()
            marker_dectection.draw_flow(frame2, flow2)


    mask_img = mask.astype(frame[0].dtype)
    mask_img = cv2.merge((mask_img, mask_img, mask_img))

    # cv2.imshow('raw',frame_raw)
    cv2.imshow('GelSlight 1',frame)
    im = br.cv2_to_imgmsg(frame)
    im_raw = br.cv2_to_imgmsg(frame_raw)
    
    camera_pub.publish(im)
    raw_camera_pub.publish(im_raw)

    z_dist = marker_displacement.avg_z_displacement(flow)
    # print("GS1 Force Z: {}".format(z_dist))
    z_torque = marker_displacement.avg_z_curl(flow)
    # print("GS1 Torque Z: {}".format(z_torque))
    

    if both_fingers_flag:
        mask_img2 = mask2.astype(frame2[0].dtype)
        mask_img2 = cv2.merge((mask_img2, mask_img2, mask_img2))
        cv2.imshow('GelSlight 2',frame2)
        im2 = br.cv2_to_imgmsg(frame2)

        z_dist2 = marker_displacement.avg_z_displacement(flow2)
        print("GS2 Force Z: {}".format(z_dist2))
        z_torque2 = marker_displacement.avg_z_curl(flow2)
        print("GS2 Torque Z: {}".format(z_torque2))
    
    
    marker_wrench.wrench.force.z = z_dist
    marker_wrench.wrench.torque.z = z_torque
    
    # tm = time.time()
    # # ns = int(str(tm - int(tm)).split('.')[1])
    # ns = int("{:.9f}".format(tm - int(tm)).split('.')[1])
    # ns = int(np.trunc(ns / 1000))
    # marker_wrench.header.stamp.secs = tm
    # marker_wrench.header.stamp.nsecs = ns
    tm = rospy.get_rostime()
    marker_wrench.header.stamp.secs = tm.secs
    marker_wrench.header.stamp.nsecs = tm.nsecs
    marker_wrench.header.frame_id = str(frameid)
    frameid += 1
    pub.publish(marker_wrench)

    #cv2.waitKey()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
#out.release()
cv2.destroyAllWindows()
rospy.spin()