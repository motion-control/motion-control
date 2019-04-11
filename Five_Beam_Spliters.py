from Motion_Modules.Basic.Basic_Motion import *
from Motion_Modules.Basic.Code_Visualization import *
from Motion_Modules.Motion_Modules import *
from math import *

class Five_beam_Spliters(Motion_Modules):
	width_Cr = 0.0022
	width_LN = 0.0064
	cp_lengthes = [0.110, 0.115, 0.120, 0.125, 0.130]
	cp_length = 0.0
	sb_length = 0.5
	sb_height = 0.03
	layer_Cr = 3
	layer_LN = 25
	step = 0.0008
	
	L_sum = 3.0
	extension = 0.05
	L_side = (L_sum - (2.0*sb_length + cp_length))/2.0
	
	
	def __init__(self, directory):
		self.file_create(directory, 'Cr')
		self.loop_head(1)
		self.BS(0)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'LN')
		self.BS(1)
		self.FILE.close()
		
		self.file_create(directory, 'Arms_Cr')
		self.Arms(0)
		self.FILE.close()
		
		self.file_create(directory, 'Arms_LN')
		self.Arms(1)
		self.FILE.close()
		
		self.file_create(directory, 'test')
		self.BS(0)
		self.BS(1)
		self.Arms(0)
		self.Arms(1)
		self.FILE.close()
		
		
	def BS(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		H_BS = 2.0*self.sb_height + self.width_Cr
		
		for i in range(0, 5):
			self.cp_length = self.cp_lengthes[i]
			self.L_side = (self.L_sum - (2.0*self.sb_length + self.cp_length))/2.0
			end_point.change(self.L_side, 2.0*H_BS*i)
			self.g_spot(end_point)
			self.shutter(1)
			self.Beam_Spliter(Cr_or_LN)
			
	def Arms(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		H_BS = 2.0*self.sb_height + self.width_Cr
		
		for i in range(0, 5):
			self.cp_length = self.cp_lengthes[i]
			self.L_side = (self.L_sum - (2.0*self.sb_length + self.cp_length))/2.0
			L_BS = 2.0*self.sb_length + self.cp_length
			
			L_left_side = 0.0
			L_right_side = self.L_side + L_BS + self.extension*0.5
			
			end_point.change(L_left_side, 2.0*H_BS*i + 0.5*H_BS)
			self.g_spot(end_point)
			self.shutter(1)
			self.Waveguide_x(Cr_or_LN, self.L_side - 0.5*self.extension)
			
			end_point.change(L_left_side, 2.0*H_BS*i - 0.5*H_BS)
			self.g_spot(end_point)
			self.shutter(1)
			self.Waveguide_x(Cr_or_LN, self.L_side - 0.5*self.extension)
			
			end_point.change(L_right_side, 2.0*H_BS*i + 0.5*H_BS)
			self.g_spot(end_point)
			self.shutter(1)
			self.Waveguide_x(Cr_or_LN, self.L_side - 0.5*self.extension)
			
			end_point.change(L_right_side, 2.0*H_BS*i - 0.5*H_BS)
			self.g_spot(end_point)
			self.shutter(1)
			self.Waveguide_x(Cr_or_LN, self.L_side - 0.5*self.extension)
			
			
directory = os.path.splitext(os.path.basename(__file__))[0]
print('Writing')
Five_beam_Spliters(directory)

(x_min, x_max) = (0, 3)
(y_min, y_max) = (-0.1, 0.6)
key = 1
Code_Visualization(directory, 'test', x_min, x_max, y_min, y_max, key)

