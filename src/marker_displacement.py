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
