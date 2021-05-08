#!/usr/bin/env python
'''
	Autonomous ODE simulator. 
	
'''

import sys, json
import numpy as np
from numpy import sin
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

import pptools

def func(t, x, data):
    v =  []
    for k in np.arange(len(data.dic['func'])):
        v.append(eval(data.dic['func'][k]))
    return v

def poincare_section(t, x, data):
	return x[data.dic['p_index']] - data.dic['p_location']


def main():
	data = pptools.init()
	state0 = data.dic['x0']
	tick = data.dic['tick']
	duration = 0.5
	period = 0.0
	poincare_section.direction = 1
	poincare_section.terminal = True
	running = True	
	time = 0.0
	
	while running:
		traj = []
		if pptools.window_closed(data.ax) == True:
			sys.exit()
		state = solve_ivp(func, (0, duration), state0,
			#method = 'DOP853', 
			method = 'RK45', args = (data,), 
			events = poincare_section, max_step = tick,
			rtol = 1e-12, dense_output = True
		)
		#t = np.arange(0, duration, 0.01)
		#traj = state.sol(t)

		if 'fd_file' in dir(data): 	# dump data to file if defined.
			pptools.dump_data(time, state, data)
		if data.visual_orbit == 1:	# show the orbit
			lines, = plt.plot(
				state.y[data.dispx, :], state.y[data.dispy, :],
				linewidth = 1, color = (0.1, 0.1, 0.3),
				ls = "-", alpha = data.dic['alpha'])
		if state.status == 1:	# A termination event occurred
			data.dic['x0'] = s = state.y_events[0][-1]
			plt.plot(s[data.dispx], s[data.dispy], 'o', 
				markersize = 2, color="red", alpha = data.dic['alpha'])
			period += state.t_events[0][-1]
			data.dic['period'] = period
			if period > duration:
				duration = period * 0.51
			period = 0.0
			poincare_section.terminal = False
		else:
			period += duration
			poincare_section.terminal = True
		state0 = data.now = state.y[:, -1] # data.now: clicked point
		time += state.t[-1]
		plt.pause(0.001) #REQIRED

if __name__ == '__main__':
	main()
