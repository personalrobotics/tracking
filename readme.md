The Gelslight is the PRL's vision-based tactile sensor designed to replace the ATI Nano-25 F/T sensor used for sensorized feeding on ADA. Inspired by MIT's GelSight sensor, the Gelslight achieves the smallest form factor of its class of sensors by using a miniature wide-angle camera, clever design, and precision manufacturing equipment. 

# Installation
Clone into the src folder of your catkin workspace. 
```shell
$ git clone https://github.com/personalrobotics/gelslight_tracking.git
```

# Marker Tracking Algorithm

## Dependencies

* opencv (v 4.\*.\*)
* pybind11
* numpy
* rospy

## Running

The dot tracking script `tracking.py` takes two argument: sensor id and rescale value. These inputs are used to select the dot tracking configuration in the `setting.py` file.

```
make
python3 src/tracking.py 1 3
```



## Configuration

Configuration based on different marker settings (marker number/color/size/interval)


### Step 1: Marker detection

The marker detection is implemented in	`src/marker_detection.py`.

Modify values using the `test_find_marker.py` script.

```
python3 src/test_find_marker.py
```

**Set Parameters**:

* `src/marker_detection/find_marker`: The scale of the GaussianBlur on line 22. This value depends on the size of the marker on the screen.
* `src/marker_detection/find_marker`: change `yellowMin, yellowMax` on lines 35 and 36 based on markers' color in HSV space.
* `src/marker_detection/marker_center`: change the `areaThresh1, areaThresh2` on lines 50 and 51 for the minimum and maximum size of markers



### Step 2: Marker matching

The definition of the first guesses for marker matching are in

`src/setting.py`

Modify the values using the `test_settings.py` script which takes the rescale value as an argument. Slide the adjuster bars until white dots corresponding to the markers appear on a black background.

* RESCALE: scale down
* N, M: the row and column of the marker array
* x0, y0: the coordinate of upper-left marker (in original size)
* dx, dy: the horizontal and vertical interval between adjacent markers (in original size)
* fps_: the desired frame per second, the algorithm will find the optimal solution in 1/fps seconds

### Step 3: Dot tracking
**Base version**

Launch roscore.
```
roscore
```

In another terminal, run the script
```
cd ~/<path_to_ws>/src/gelslight_tracking
python3 src/tracking.py 1 3
```

which takes the sensor identifier flag and the image rescale value as arguments, respectively. 

* A higher rescale value decreases the resolution of the image which increases the frequency of the dot tracking algorithm. Changing this value will require modifying the settings.
* Press *q* to terminate the program.

**Running on ADA**
Transfer the files into the Nvidia Jetson Nano onboard ADA. 

Turn on ADA. SSH into the Nano with x forwarding and set weebo as the Ros Master
```
ssh -X nano
useweebo
```
Either run the base tracking script or the tracking with taring action script (if running the feeding demo without the ATI F/T sensor). Note that Nano uses python2 rather than python3. 
```
cd ~/catkin_ws/src/gelslight_tracking
python2 src/tracking_w_taring_action.py 1 3
```

**Note**: The USB ports on the Nano which the sensors are plugged into affect the ordering of the camera ports when powering on ADA. 

## Output

**Tracking**

The tracking algorithms will display the camera feed and print the force and torque in the Z-direction. The gelsight node initialized by these scripts publishes the camera feed and a 6-DOF Wrench (2 implemented).

## Common Issues
* ZeroDivisionError likely means you are using the Intel RealSense camera rather than the Gelslight camera. Ensure the sensors are plugged into the correct ports and reboot ADA. Or change the cv2.VideoCapture camera index  in the code. 

* If the Gelslight sensor feed has large green and/or red arrows, refer to the marker matching section. The ideal initial image should consist of green arrows with 0 length which will appear as dots. If you are having trouble closing video windows, refer to [this](https://unix.stackexchange.com/questions/113893/how-do-i-find-out-which-process-is-using-my-v4l2-webcam).
* `Import Error: /<path_to_ws>/gelslight_tracking/src/find_marker.so` is an issue with the defined python version in the makefile. Update the python calls in `/<path_to_ws>/gelslight_tracking/makefile`. Note that python3 is used when running on Weebo and python2 is used when running on Nano. 
