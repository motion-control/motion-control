from Motion_Modules.Basic.Basic_Motion import *
from Motion_Modules.Basic.Code_Visualization import *
from Motion_Modules.Motion_Modules import *
from math import *

class Template(Motion_Modules):
	width_Cr = 0.0022
	width_LN = 0.0064
	cp_length = 0.12
	sb_length = 0.5
	sb_height = 0.03
	layer_Cr = 3
	layer_LN = 25
	step = 0.0008
	
	L_arm = 2.3
	L_sum = 20.0
	extension = 0.05
	Zz = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	Xx = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	L_side = (L_sum - 3.0*(2.0*(sb_length*2.0 + cp_length) + 2.0*L_arm) + L_arm)/2.0
	
	
	def __init__(self, directory):
		self.file_create(directory, 'Cr_1')
		self.loop_head(1)
		self.BS_1(0)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'test')
		self.BS_1(0)
		self.FILE.close()
		
		print('G0 X{:.6f} Y0.0'.format(self.Xx[0]))
		
	def BS_1(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		L_BS = 2.0*self.sb_length + self.cp_length
		H_BS = 2.0*self.sb_height + self.width_Cr
		x_BS_1 = self.L_side
		self.Xx[0] = x_BS_1
		self.Xx[1] = x_BS_2
		
		end_point.change(x_BS_1, 0.0, self.Zz[0]) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		
directory = os.path.splitext(os.path.basename(__file__))[0]
print('Writing')
Template(directory)

(x_min, x_max) = (0, 20)
(y_min, y_max) = (-0.2, 0.2)
key = 1
Code_Visualization(directory, 'test', x_min, x_max, y_min, y_max, key)

