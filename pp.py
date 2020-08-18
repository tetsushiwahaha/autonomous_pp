# Autonomous ODE simulator. 
# Special Thank to S. Amoh on 2020/05/09
#

import sys, json
import numpy as np
from numpy import sin
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

import pptools

def func(t, x, data):
    v =  []
    for k in np.arange(len(data.dict['func'])):
        v.append(eval(data.dict['func'][k]))
    return v

def poincare(t, x, data):
	return x[data.dict['p_index']] - data.dict['p_position']


def main():
	data = pptools.init()
	state0 = data.dict['x0']
	tick = data.dict['tick']
	duration = 10.0
	period = 0
	#poincare.direction = -1
	running = True	
	
	while running:
		if pptools.window_closed(data.ax) == True:
			sys.exit()
		state = solve_ivp(func, (0, duration), state0,
			#method = 'DOP853', 
			method = 'RK45', 
			args=(data,), events = poincare, max_step = tick,
			rtol = 1e-6, dense_output = True)
		if data.visual_orbit == 1:
			lines, = plt.plot(
				state.y[data.dispx, :], state.y[data.dispy, :],
				linewidth = 1, color = (0.1, 0.1, 0.3),
				ls = "-", alpha = data.dict['alpha'])
		if len(state.y_events[0]) != 0: # On the poincare section
			period += state.t_events[0][0]
			data.dict['period'] = period
			data.dict['x0'] = s = state.y_events[0][-1]
			plt.plot(s[data.dispx], s[data.dispy], 'o', 
				markersize = 2, color="red",
				 alpha = data.dict['alpha'])
			period = duration - state.t_events[0][-1]
		else:
			period += duration
		state0 = data.now = state.y[:, -1]
		plt.pause(0.001) #REQIRED

if __name__ == '__main__':
	main()
