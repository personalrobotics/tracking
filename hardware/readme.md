# CAD Files
The Solidworks CAD files for the Gelslight sensor may be found [here](https://github.com/KHsu2/fingergelsight).

# Fabrication Tutorials

The instructions with pictures for fabricating the Gelslight sensors may be found [here](https://robotfeeding.io/hardware/gelsight-mini-tactile-sensor/)

The print-friendly wiki for fabricating Gelslight sensors may be found [here](https://github.com/personalrobotics/pr_docs/wiki/Gelsight-Mini-Sensor-Fabrication).

## Fabrication Equipment at UW
* 3D Printer, Laser Cutter
	* UW Makerspaces: [The Mill](https://hfs.uw.edu/The-MILL/Maker-Space-1), [Area 01](https://www.washington.edu/area01/), [The 8](https://hfs.uw.edu/The-8)
	* UW CSE Manufacturing Lab (ask Rosario)
	* UW ME [Machine Shop](https://www.me.washington.edu/shops/machine/printers) 
	* Note: Ask employees or shop master for operation instructions 
* Silicone Manufacturing Equipment
	* Fume hood, vacuum chamber, toaster oven
	* Located in [ECE/EEB B031](https://www.washington.edu/maps/#!/ece)

## Material Locations
* [Misumi TD-BL31105 (Small fisheye camera)](http://www.misumi.com.tw/PLIST.ASP): 
* [3D Print Filament](): 
* [Acrylic](): 
* 

## Removing Kinova KG-2 Distal Phalanxes
The distal phalanx (fingertip) is secured by a pin at the joint and by an actuating bar that feeds through the proximal phalanx. First, remove the pair of bolts at the joint located furthest from the base, then use a small rod to push out the pin. Next, free the distal phalanx from the actuating bar by gently prying the rubber. Be careful not to stretch rubber excessively. 

## Attaching Gelslight
The base of the Gelslight is designed much like the original KG-2 distal phalanx. Attach the Gelslight to the actuating bar by the largest holes, then insert the pin through the joint and the Gelslight, and fasten the bolts to the pin. Plug both USBs into the wrist controller. The fingers are now ready to use.

<img src="pictures/nano_port_id.PNG" width="400"/>

## Preventing Fork Handle Slippage
An issue with the underactuated design of the Kinova PR2 gripper fingers is that the finger joints are not stiff. This means that slippage may occur between the fork handle and the Gelslight sensor pad when forces act on the fork. This is highly undesirable because the force estimation from dot tracking depends on the assumption that no slipping occurs. 

The current solution to this is to completely open the fingers using the manual control stick. Now close the fingers completely around the fork handle. Ensure that the sensor pads of the Gelslight's are flush with the sides of the fork handle. Now wrap painter's tape several times around both proximal phalanxes to improve the stiffness of the finger joints. 