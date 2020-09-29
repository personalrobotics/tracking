import rosbag
from geometry_msgs.msg import WrenchStamped
import matplotlib.pyplot as plt
import numpy as np
import sys

class DraggableLegend:
	def __init__(self, legend):
		self.legend = legend
		self.gotLegend = False
		legend.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
		legend.figure.canvas.mpl_connect('pick_event', self.on_pick)
		legend.figure.canvas.mpl_connect('button_release_event', self.on_release)
		legend.set_picker(self.my_legend_picker)

	def on_motion(self, evt):
		if self.gotLegend:
			dx = evt.x - self.mouse_x
			dy = evt.y - self.mouse_y
			loc_in_canvas = self.legend_x + dx, self.legend_y + dy
			loc_in_norm_axes = self.legend.parent.transAxes.inverted().transform_point(loc_in_canvas)
			self.legend._loc = tuple(loc_in_norm_axes)
			self.legend.figure.canvas.draw()

	def my_legend_picker(self, legend, evt): 
		return self.legend.legendPatch.contains(evt)   

	def on_pick(self, evt): 
		if evt.artist == self.legend:
			bbox = self.legend.get_window_extent()
			self.mouse_x = evt.mouseevent.x
			self.mouse_y = evt.mouseevent.y
			self.legend_x = bbox.xmin
			self.legend_y = bbox.ymin 
			self.gotLegend = 1

	def on_release(self, event):
		if self.gotLegend:
			self.gotLegend = False

bag = rosbag.Bag(sys.argv[1])
#bag = rosbag.Bag('2020-03-16-17-14-23.bag')
time_ft_1 = np.zeros(bag.get_message_count(topic_filters='/forque/forqueSensor'))
data_ft_1 = time_ft_1.copy()
time_gs_1 = np.zeros(bag.get_message_count(topic_filters='/gs_ft_1'))
data_gs_1 = time_gs_1.copy()
time_joint_states = np.zeros(bag.get_message_count(topic_filters='/joint_states'))
data_joint_states = time_joint_states.copy()

iter_gs = 0
iter_ft = 0
iter_js = 0
for topic, msg, t in bag.read_messages():	
	if topic == '/gs_ft_1':
		if iter_gs == 0:
			t0_gs = t.to_nsec()
		time_gs_1[iter_gs] = (t.to_nsec() - t0_gs) * 1e-9
		data_gs_1[iter_gs] = msg.wrench.force.z
		print(msg.wrench.force.z)
		iter_gs += 1
	if topic == '/forque/forqueSensor':
		if iter_ft == 0:
			t0_ft = t.to_nsec()
		time_ft_1[iter_ft] = (t.to_nsec() - t0_ft) * 1e-9
		data_ft_1[iter_ft] = msg.wrench.force.z
		iter_ft += 1
	if topic == '/joint_states':
		if iter_js == 0: 
			t0_js = t.to_nsec()
		time_joint_states[iter_js] = (t.to_nsec() - t0_js) * 1e-9
		data_joint_states[iter_js] = msg.effort[6]
		iter_js += 1

bag.close()


# plt.subplot(2,2,1)
plt.subplot(2,1,1)
plt.plot(time_gs_1,data_gs_1,label='Gelslight Force')
plt.title('Gelslight Force')
# plt.show()
# plt.subplot(2,2,3)
plt.subplot(2,1,2)
plt.plot(time_ft_1,data_ft_1,label='FT Force')
plt.title('FT Force')
# plt.show()
# plt.subplot(2,2,2)
# plt.plot(time_joint_states,data_joint_states,label='Grip Effort')
# plt.title('Grip Effort')

if len(sys.argv) == 3:
	plt.gcf().suptitle(sys.argv[2], fontsize=16)
plt.show()

# plt.title('Shear measurement of strawberry (11.5 g)')
# plt.xlabel('time (s)')
# plt.ylabel('shear')
# drag = DraggableLegend(plt.legend())