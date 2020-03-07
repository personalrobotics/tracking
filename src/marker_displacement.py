import numpy as np

def avg_z_displacement(flow):
	Ox, Oy, Cx, Cy, Occupied = flow
	total_dist = 0
	num_occupied = 0
	for i in range(len(Ox)):
		for j in range(len(Ox[i])):
			if Occupied[i][j] > -1:
				x = int(Cx[i][j]) - int(Ox[i][j]) 
				y = int(Cy[i][j]) - int(Oy[i][j])
				total_dist = np.cos(np.arctan2(y,x)) * np.sqrt(x**2 + y**2)
				num_occupied += 1
	return total_dist / num_occupied

def avg_z_curl(flow):
	Ox, Oy, Cx, Cy, Occupied = flow
	xlen = len(Ox)
	ylen = len(Ox[0])
	v_grad_x = np.true_divide(np.gradient(Cy, axis=1), np.gradient(Ox, axis=1))
	u_grad_y = np.true_divide(np.gradient(Cx, axis=0), np.gradient(Oy, axis=0))
	curl_z = np.add(v_grad_x, u_grad_y)
	return sum(sum(curl_z))/(xlen*ylen)