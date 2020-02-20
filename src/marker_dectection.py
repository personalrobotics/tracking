import cv2
import numpy as np
import setting

def init(frame):
    RESCALE = setting.RESCALE
    return cv2.resize(frame, (0, 0), fx=1.0/RESCALE, fy=1.0/RESCALE)

def find_marker(frame):
    RESCALE = setting.RESCALE
    # Blur image to remove noise
    
    #A good filter
    #scale = 63
    #blur = cv2.GaussianBlur(frame, (int(scale/RESCALE), int(scale/RESCALE)), 0)
    #frame = frame[120:430]
    # For BnR (Fisheye no dewarping)
    scale = 22
    blur = cv2.GaussianBlur(frame, (int(scale/RESCALE), int(scale/RESCALE)), 0)

    # subtract the surrounding pixels to magnify difference between markers and background
    diff = frame.astype(np.float32) - blur
    
    diff *= 4.0
    diff[diff<0.] = 0.
    diff[diff>255.] = 255.
    diff = cv2.GaussianBlur(diff, (int(scale/RESCALE), int(scale/RESCALE)), 0)
    cv2.imshow("diff", diff)

    # Switch image from BGR colorspace to HSV
    hsv = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2HSV)
    
    cv2.imshow("Pre-Mask", hsv)

    yellowMin = (20, 170, 10)
    yellowMax = (50, 255, 50)

    #cv2.imshow("HSV", hsv)

    # Sets pixels to white if in yellow range, else will be set to black
    mask = cv2.inRange(hsv, yellowMin, yellowMax)
    cv2.imshow("mask", mask)

    return mask

def marker_center(mask, frame):
    RESCALE = setting.RESCALE
    
    #areaThresh1=90/RESCALE**2
    areaThresh1=10/RESCALE**2
    areaThresh2=3000/RESCALE**2
    MarkerCenter = []

    contours=cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours[0])<25:  # if too little markers, then give up
        print("Too few markers detected: ", len(contours))
        return MarkerCenter

    for contour in contours[0]:
        x,y,w,h = cv2.boundingRect(contour)
        AreaCount=cv2.contourArea(contour)
        # print(AreaCount)
        if AreaCount>areaThresh1 and AreaCount<areaThresh2 and abs(np.max([w, h]) * 1.0 / np.min([w, h]) - 1) < 5:
            t=cv2.moments(contour)
            # print("moments", t)
            # MarkerCenter=np.append(MarkerCenter,[[t['m10']/t['m00'], t['m01']/t['m00'], AreaCount]],axis=0)
            mc = [t['m10']/t['m00'], t['m01']/t['m00']]
            # if t['mu11'] < -100: continue
            MarkerCenter.append(mc)
            # print(mc)
            cv2.circle(frame, (int(mc[0]), int(mc[1])), 1, ( 0, 0, 255 ), 2, 6);

    # 0:x 1:y
    #print("Number of markers: ", len(MarkerCenter))
    return MarkerCenter

def draw_flow(frame, flow):
    Ox, Oy, Cx, Cy, Occupied = flow
    K = 0
    for i in range(len(Ox)):
        for j in range(len(Ox[i])):
            pt1 = (int(Ox[i][j]), int(Oy[i][j]))
            pt2 = (int(Cx[i][j] + K * (Cx[i][j] - Ox[i][j])), int(Cy[i][j] + K * (Cy[i][j] - Oy[i][j])))
            color = (0, 255, 0)
            if Occupied[i][j] <= -1:
                color = (127, 127, 255)
            
            #cv2.arrowedLine(frame, pt1, pt2, color, 2,  tipLength=0.2)
            cv2.circle(frame, pt2, 5, ( 0, 255, 0 ), 2, 6)


def warp_perspective(img):

    TOPLEFT = (175,230)
    TOPRIGHT = (380,225)
    BOTTOMLEFT = (10,410)
    BOTTOMRIGHT = (530,400)

    WARP_W = 215
    WARP_H = 215

    points1=np.float32([TOPLEFT,TOPRIGHT,BOTTOMLEFT,BOTTOMRIGHT])
    points2=np.float32([[0,0],[WARP_W,0],[0,WARP_H],[WARP_W,WARP_H]])

    matrix=cv2.getPerspectiveTransform(points1,points2)

    result = cv2.warpPerspective(img, matrix, (WARP_W,WARP_H))

    return result


def init_HSR(img):
    DIM=(640, 480)
    #img = cv2.resize(img, DIM)

    # K=np.array([[225.57469247811056, 0.0, 280.0069549918857], [0.0, 221.40607131318117, 294.82435570493794], [0.0, 0.0, 1.0]])
    # D=np.array([[0.7302503082668154], [-0.18910060205317372], [-0.23997727800712282], [0.13938490908400802]])

    # calib for broken camera
    #K=np.array([[361.48260057678084, 0.0, 326.3038808664325], [0.0, 363.0042323004205, 231.28905831858228],[0.0, 0.0, 1.0]])
    #D=np.array([[-0.5126093819524806],[0.6843819910316263],[-0.5364453924581161],[0.16900928490249337]])

    # fisheye v2_2_4 calib
    #K=np.array([[365.9257926579611, 0.0, 278.18826358436525], [0.0, 365.5062577034247, 253.66969821083646], [0.0, 0.0, 1.0]])
    #D=np.array([[-0.47269037048260093], [0.5378593756701429], [-0.32909122333561375], [0.07752764030841539]])

    K=np.array([[511.42214429243734, 0.0, 242.67652843738074], [0.0, 511.7551005079224, 274.6988332309846], [0.0, 0.0, 1.0]])
    D=np.array([[-0.4966193781227207], [0.5424952885130186], [-0.3224294757793182], [0.05028594411558891]])


    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    #return warp_perspective(undistorted_img)
    return undistorted_img

def init_HSR_full(img, balance=1.0, dim2=None, dim3=None):
    DIM=(640,480)
    #img = cv2.resize(img, DIM)
    dim1 = img.shape[:2][::-1]
    #print(dim1)

    #New camera #1 calibrations
    #K=np.array([[361.69599051993794, 0.0, 335.35532025681607], [0.0, 373.4786659714398, 219.2431499095929],[0.0, 0.0, 1.0]])
    #D=np.array([[-0.6890864194293433],[1.5981061572212945],[-2.19065264920203],[1.1717371527060296]])
    
    #K=np.array([[511.42214429243734, 0.0, 242.67652843738074], [0.0, 511.7551005079224, 274.6988332309846], [0.0, 0.0, 1.0]])
    #D=np.array([[-0.4966193781227207], [0.5424952885130186], [-0.3224294757793182], [0.05028594411558891]])

    #K=np.array([[365.9257926579611, 0.0, 278.18826358436525], [0.0, 365.5062577034247, 253.66969821083646], [0.0, 0.0, 1.0]])
    #D=np.array([[-0.47269037048260093], [0.5378593756701429], [-0.32909122333561375], [0.07752764030841539]])

    #=np.array([[512.9171513693165, 0.0, 246.6190435638709], [0.0, 513.6171597790584, 276.2478715985629], [0.0, 0.0, 1.0]])
    #=np.array([[-0.4941345242254273], [0.4736556693658705], [-0.1259589487063504], [-0.1117894657018813]])

    # 2019-09-14_1:
    #K=np.array([[486.15363072192906, 0.0, 270.42512893511275], [0.0, 486.55654445883226, 265.0125487429911], [0.0, 0.0, 1.0]])
    #D=np.array([[-0.511105857290584], [0.7196025363844903], [-0.5529533063605124], [0.15126765925490118]])

    # 2019-09-14_2
    #K=np.array([[486.5991603143406, 0.0, 270.82310139540164], [0.0, 487.68983523599314, 264.61844281601236], [0.0, 0.0, 1.0]])
    #D=np.array([[-0.5337258565360732], [0.8651318105365522], [-0.9028615039586585], [0.43533340680925414]])

    K=np.array([[486.5991603143406, 0.0, 320], [0.0, 487.68983523599314, 264.61844281601236], [0.0, 0.0, 1.0]])
    D=np.array([[-0.53], [1.05], [-.9], [.7]])




    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs same aspect ratio as ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1

    scaled_K = K * dim1[0]/DIM[0]
    scaled_K[2][2] = 1

    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    return undistorted_img
