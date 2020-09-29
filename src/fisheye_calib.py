"""
Author : Kevin Hsu
Description: This file was used to capture images from the fisheye lens and to test disabling color channels.
"""
import numpy as np
import cv2

DIM = (640, 480)
#calib new cam 1
#K=np.array([[361.69599051993794, 0.0, 335.35532025681607], [0.0, 373.4786659714398, 219.2431499095929], [0.0, 0.0, 1.0]])
#D=np.array([[-0.6890864194293433], [1.5981061572212945], [-2.19065264920203], [1.1717371527060296]])

#calib new cam 2 v1
#K=np.array([[360.219787027477, 0.0, 280.67491971617414], [0.0, 362.04612408869343, 265.28641971527867], [0.0, 0.0, 1.0]])
#D=np.array([[-0.46728165458528625], [0.5609850958819242], [-0.377583864024142], [0.10188132362876111]])

#calib new cam 2
#K=np.array([[368.53352751053285, 0.0, 278.67262302495783], [0.0, 366.2278178165265, 260.0754141370175], [0.0, 0.0, 1.0]])
#D=np.array([[-0.48848435461094664], [0.5480802143008674], [-0.33583964192965526], [0.08069470961117511]])

#calib new cam 2 v3
#K=np.array([[364.5193304371228, 0.0, 280.4984979716664], [0.0, 365.5365761700237, 250.95077713582802], [0.0, 0.0, 1.0]])
#D=np.array([[-0.4685670942312378], [0.5388260014278695], [-0.3328372500453471], [0.07890886696032497]])

#calib new cam 2 v4
#K=np.array([[363.03645769674387, 0.0, 275.8354934761089], [0.0, 363.52220055205896, 250.19861654286797], [0.0, 0.0, 1.0]])
#D=np.array([[-0.4607475942879474], [0.534254751667319], [-0.33174986966526554], [0.07882368066373245]])

K=np.array([[365.9257926579611, 0.0, 278.18826358436525], [0.0, 365.5062577034247, 253.66969821083646], [0.0, 0.0, 1.0]])
D=np.array([[-0.47269037048260093], [0.5378593756701429], [-0.32909122333561375], [0.07752764030841539]])

def undistort(frame):
	img = frame
	h,w = img.shape[:2]
	map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
	undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

	return undistorted_img

def full_undistort(frame, balance=0, dim2=None, dim3=None):
	#img = cv2.imread(frame)
	img = frame
	dim1 = img.shape[:2][::-1]

	assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs same aspect ratio as ones used in calibration"

	if not dim2:
		dim2 = dim1

	if not dim3: 
		dim3 = dim1

	scaled_K = K * dim1[0] / DIM[0]
	scaled_K[2][2] = 1

	new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
	map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
	undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

	return undistorted_img

def main() :
	cap = cv2.VideoCapture(0)
	i = 0
	while True:
		ret, frame = cap.read()

		# Disabling color channels
		#frame[:,:,0] = 0	#Blue
		#[:,:,1] = 0	#Green
		#frame[:,:,2] = 0	#Redq
		cv2.imshow('raw', frame)
		# Undistort
		frame  = undistort(frame)

		# Display the resulting image
		cv2.imshow('Video', frame)
		
		# Hit 'c' to the keyboard to capture image
		#if cv2.waitKey(1) & 0xFF == ord('c'):
		if cv2.waitKey(1) & 0xFF == ord('c'):
			cv2.imwrite('pic{:>02}.jpg'.format(i), frame)
			i += 1

		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


	# Release handle to the webcam
	cap.release()
	cv2.destroyAllWindows()


if __name__ == "__main__" :
    main()
