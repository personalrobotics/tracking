import find_marker
import numpy as np
import cv2
import time
import marker_dectection
import marker_displacement
import sys
import setting
import rospy
from geometry_msgs.msg import Wrench

##### ROS COMMENT
rospy.init_node('gelsight', anonymous=True)
pub = rospy.Publisher('dot_displacement', Wrench, queue_size=10)
marker_wrench = Wrench()

marker_wrench.force.x = 0
marker_wrench.force.y = 0
marker_wrench.torque.x = 0
marker_wrench.torque.y = 0
marker_wrench.torque.z = 0

calibrate = False

if len(sys.argv) > 1:
    if sys.argv[1] == 'calibrate':
        calibrate = True

#gelsight_version = 'Bnz'
gelsight_version = 'HSR'

# cap = cv2.VideoCapture("data/GelSight_Twist_Test.mov")
#cap = cv2.VideoCapture("data/GelSight_Shear_Test.mov")
cap = cv2.VideoCapture(0)


# Resize scale for faster image processing
setting.init()
RESCALE = setting.RESCALE

# Create Mathing Class
m = find_marker.Matching(
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
fourcc = cv2.VideoWriter_fourcc(*'XVID')

if gelsight_version == 'HSR':
    out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (640,480))
else:
    #out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (1280//RESCALE,720//RESCALE))
    out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (1280//RESCALE,960//RESCALE))

#for i in range(30): ret, frame = cap.read()

# num_markers = []

while(True):
#for i in range(200):

    # capture frame-by-frame
    ret, frame = cap.read()
    if not(ret): 
        break

    frame_raw = frame.copy()

    # resize (or unwarp)
    if gelsight_version == 'HSR':
        #frame = marker_dectection.init_HSR(frame)
        frame = marker_dectection.init_HSR_full(frame, balance=1)
    else:
        frame = marker_dectection.init(frame)
    # frame = marker_dectection.init_HSR(frame)

    # find marker masks
    mask = marker_dectection.find_marker(frame)

    # find marker centers
    mc = marker_dectection.marker_center(mask, frame)
    
    #### Record len(mc) and tune marker_center so that the std is low
    #num_markers.append(len(mc))

    if calibrate == False:
        tm = time.time()
        # # matching init
        m.init(mc)
        #print(m)
        # # matching
        m.run()
        print("dt:", time.time() - tm)
        # print("m: ", type(m))
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
        # TODO: Uncomment below
        marker_dectection.draw_flow(frame, flow)

    mask_img = mask.astype(frame[0].dtype)
    mask_img = cv2.merge((mask_img, mask_img, mask_img))

    # cv2.imshow('raw',frame_raw)
    cv2.imshow('frame',frame)

    if calibrate:
        # Display the mask 
        cv2.imshow('mask',mask_img)

    out.write(frame)

    z_dist = marker_displacement.avg_z_displacement(flow)
    print("Force Z: ", z_dist)
    z_torque = marker_displacement.avg_z_curl(flow)
    print("Torque Z: ", z_torque)
    
    ##### ROS COMMENT
    
    marker_wrench.force.z = z_dist
    marker_wrench.torque.z = z_torque
    pub.publish(marker_wrench)
    

    #print(frame.shape)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
