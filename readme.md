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

```
pip3 install pybind11 numpy opencv-python
```

## Example

```
make
python3 src/tracking.py
```
## Configuration

Configuration based on different marker settings (marker number/color/size/interval)


### Step 1: Marker detection

The marker detection is in	`src/marker_detection.py`

Modify the code based on the marker color & size using the script

```
python3 src/test_find_marker.py
```

**Set Parameters**:

* `src/marker_detection/find_marker`: The kernel size in GaussianBlur, it depends on marker size. should could cover the whole marker.
* `src/marker_detection/find_marker`: change `yellowMin, yellowMax` based on markers' color in HSV space.
* `src/marker_detection/marker_center`: change the `areaThresh1, areaThresh2` for the minimal and maximal size of markers



### Step 2: Marker matching

The definition of the first guesses for marker matching are in

`src/setting.py`

Modify the values using the script
```
python3 src/test_settings.py
```
Slide the adjuster bars 

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
cd ~/*/gelslight_tracking
python3 src/tracking.py 1 2
```

which takes the sensor identifier flag and the image rescale value as arguments, respectively. 

* A higher rescale value decreases the resolution of the image which increases the frequency of the dot tracking algorithm. Changing this value will require modifying the settings.
* Press *q* to terminate the program.

**Running on ADA**
Transfer the files into the Nvidia Jetson Nano onboard ADA.

SSH into the Nano with x forwarding
```
ssh -X nano
```
then either run the base tracking script or the tracking with taring action script (if running the feeding demo without the ATI F/T sensor).
```
cd ~/nano/*/gelslight_tracking
python3 src/tracking_w_taring_action.py
```
## Output

**Tracking**

The tracking algorithms will display the camera feed and print the force and torque in the Z-direction. The gelsight node initialized by these scripts publishes the camera feed and a 6-DOF Wrench (2 implemented).

**Matching**

The Matching Class has a function `get_flow`. It return the flow information:

```
flow = m.get_flow()

output: (Ox, Oy, Cx, Cy, Occupied) = flow
    Ox, Oy: N*M matrix, the x and y coordinate of each marker at frame 0
    Cx, Cy: N*M matrix, the x and y coordinate of each marker at current frame
    Occupied: N*M matrix, the index of the marker at each position, -1 means inferred. 
        e.g. Occupied[i][j] = k, meaning the marker mc[k] lies in row i, column j.
```

