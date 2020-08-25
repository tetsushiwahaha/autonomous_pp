import sys, json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages



class DataStruct():
	def __init__(self):
		if len(sys.argv) != 2:
			print(f"Usage: python {sys.argv[0]} filename")
			sys.exit(0)
		fd = open(sys.argv[1], 'r')
		self.dict = json.load(fd)
		fd.close()
		self.param_ptr = 0
		self.ax =None
		self.fig =None
		self.dispx = 0
		self.dispy = 1
		self.now = [0.0, 0.0]
		if self.dict.get('alpha', None) == None:
			self.dict['alpha'] = 1.0

def init():
	plt.rcParams['keymap.save'].remove('s')
	plt.rcParams['keymap.quit'].remove('q')
	data = DataStruct()

	data.fig = plt.figure(figsize=(10, 10))
	data.ax = data.fig.add_subplot(111)

	redraw_frame(data)
	data.visual_orbit = 1

	plt.connect('button_press_event', 
		lambda event: on_click(event, data))
	plt.connect('key_press_event', 
		lambda event: keyin(event, data))
#	plt.connect('close_event', 
#		lambda event: closeall(event, data))
#	plt.connect('figure_enter_event', 
#		lambda event: figureenter(event, data))
#	data.fig.canvas.get_tk_widget().focus_force()

	show_param(data)
	return data


def redraw_frame(data):
	xr = data.dict['xrange']
	yr = data.dict['yrange']
	data.ax.set_xlim(xr)
	data.ax.set_ylim(yr)
	data.ax.set_xlabel('x', fontsize=12)
	data.ax.set_ylabel('y', fontsize=12)
	data.ax.grid(c='gainsboro', zorder=9)


class jsonconvert(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.integer):
			return int(obj)
		elif isinstance(obj, np.floating):
			return float(obj)
		elif isinstance(obj, np.ndarray):
			return obj.tolist()
		else:
			return super(jsonconvert, self).default(obj)

def window_closed(ax):
	fig = ax.figure.canvas.manager
	mgr = plt._pylab_helpers.Gcf.figs.values()
	return fig not in mgr

def keyin(event, data):
	ptr = data.param_ptr
	dim = len(data.dict['x0'])
	if event.key == '+':
		data.dispx += 1
		if data.dispx >= dim:
			data.dispx = 0
		data.dispy = data.dispx + 1
		if data.dispy >= dim:
			data.dispy = 0
	if event.key == '-':
		data.dispx -= 1
		if data.dispx < 0 :
			data.dispx = dim - 1
		data.dispy -= 1
	elif event.key == 'q':
		plt.close('all') 
		print("quit")	
		sys.exit()
	elif event.key == 'w':
		jd = json.dumps(data.dict, cls = jsonconvert)
		print(jd)
		with open("__ppout__.json", 'w') as fd:
			json.dump(data.dict, fd, indent=4, cls = jsonconvert)
		print("now writing...", end="")
		pdf = PdfPages('snapshot.pdf')
		pdf.savefig()
		pdf.close()
		print("done.")
	elif event.key == ' ' or event.key == 'e':
		plt.cla()
		redraw_frame(data)
	elif event.key == 'f':
		plt.cla()
		redraw_frame(data)
		data.visual_orbit = 1 - data.visual_orbit
	elif event.key == 's':
		for i in data.dict['params']:
			print(i, end=' ')
		print(data.dict['x0'])
		print(data.dict['period'])
	elif event.key == 'p':
		data.param_ptr += 1
		if data.param_ptr >= len(data.dict['params']):
			data.param_ptr = 0
		print(f"changable parameter: {data.param_ptr}")
	elif event.key == 'up':
		ptr = data.param_ptr
		data.dict['params'][ptr] += data.dict['dparams'][ptr] 
	elif event.key == 'down':
		ptr = data.param_ptr
		data.dict['params'][ptr] -= data.dict['dparams'][ptr] 
	show_param(data)
	return

def show_param(data):
	s = ""
	cnt = 0
	for key in data.dict['params']:
		s += " param{:d}: {:.5f}  ".format(cnt, key) 
		cnt += 1
	plt.title(s, color='b')

def on_click(event, data):
	if event.xdata == None or event.ydata == None:
		return
	s0 = data.now
	s0[data.dispx] = event.xdata
	s0[data.dispy] = event.ydata
	print(s0)
	plt.plot(s0[data.dispx], s0[data.dispy], 'o', markersize = 2, color="blue")
	# copies an average value to the rest state variables
	avg = (s0[data.dispx] + s0[data.dispy])/2.0
	for i in np.arange(len(s0)):
		if (i != data.dispx and i != data.dispy):
			s0[i] = avg
	redraw_frame(data)
	show_param(data)
	data.now = s0
	return

def figureenter(event, data):
	print("xxxxxxxxxxxxx")
	return

def on_close():
	running = False
