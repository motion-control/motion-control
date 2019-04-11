from Motion_Modules.Basic.Basic_Motion import *
from Motion_Modules.Basic.Code_Visualization import *
from Motion_Modules.Motion_Modules import *
from math import *

class Unitary_Operator_3lay(Motion_Modules):
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
		self.BS_1(0)
		self.FILE.close()
		
		self.file_create(directory, 'Cr_2')
		self.BS_2(0)
		self.FILE.close()
		
		self.file_create(directory, 'Cr_3')
		self.BS_3(0)
		self.FILE.close()
		
		self.file_create(directory, 'LN_1')
		self.BS_1(1)
		self.FILE.close()
		
		self.file_create(directory, 'LN_2')
		self.BS_2(1)
		self.FILE.close()
		
		self.file_create(directory, 'LN_3')
		self.BS_3(1)
		self.FILE.close()
		
		self.file_create(directory, 'arms_Cr_1')
		self.Arms_1(0)
		self.FILE.close()
		
		self.file_create(directory, 'arms_Cr_2')
		self.Arms_2(0)
		self.FILE.close()
		
		self.file_create(directory, 'arms_Cr_3')
		self.Arms_3(0)
		self.FILE.close()
		
		self.file_create(directory, 'arms_LN_1')
		self.Arms_1(1)
		self.FILE.close()
		
		self.file_create(directory, 'arms_LN_2')
		self.Arms_2(1)
		self.FILE.close()
		
		self.file_create(directory, 'arms_LN_3')
		self.Arms_3(1)
		self.FILE.close()
		
		self.file_create(directory, 'test')
		self.BS_1(0)
		self.BS_1(1)
		self.BS_2(0)
		self.BS_2(1)
		self.BS_3(0)
		self.BS_3(1)
		self.Arms_1(0)
		self.Arms_1(1)
		self.Arms_2(0)
		self.Arms_2(1)
		self.Arms_3(0)
		self.Arms_3(1)
		self.FILE.close()
		print('G0 X{:.6f} Y0.0'.format(self.Xx[0]))
		print('G0 X{:.6f} Y0.0'.format(self.Xx[1]))
		print('G0 X{:.6f} Y0.0'.format(self.Xx[2]))
		print('G0 X{:.6f} Y0.0'.format(self.Xx[3]))
		print('G0 X{:.6f} Y0.0'.format(self.Xx[4]))
		print('G0 X{:.6f} Y0.0'.format(self.Xx[5]))
		
	def BS_1(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		L_BS = 2.0*self.sb_length + self.cp_length
		H_BS = 2.0*self.sb_height + self.width_Cr
		x_BS_1 = self.L_side
		x_BS_2 = x_BS_1 + L_BS + self.L_arm
		self.Xx[0] = x_BS_1
		self.Xx[1] = x_BS_2
		
		# middle
		end_point.change(x_BS_1, 0.0, self.Zz[0])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, 0.0, self.Zz[1])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		# down
		end_point.change(x_BS_1, -2.0*H_BS, self.Zz[0])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, -2.0*H_BS, self.Zz[1])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		# up
		end_point.change(x_BS_1, 2.0*H_BS, self.Zz[0])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, 2.0*H_BS, self.Zz[1])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
	def BS_2(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		L_BS = 2.0*self.sb_length + self.cp_length
		H_BS = 2.0*self.sb_height + self.width_Cr
		x_BS_1 = self.L_side + 2.0*(L_BS + self.L_arm)
		x_BS_2 = x_BS_1 + L_BS + self.L_arm
		self.Xx[2] = x_BS_1
		self.Xx[3] = x_BS_2
		
		# down
		end_point.change(x_BS_1, -H_BS, self.Zz[2])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, -H_BS, self.Zz[3])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		# up
		end_point.change(x_BS_1, H_BS, self.Zz[2])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, H_BS, self.Zz[3])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
	def BS_3(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		L_BS = 2.0*self.sb_length + self.cp_length
		H_BS = 2.0*self.sb_height + self.width_Cr
		x_BS_1 = self.L_side + 4.0*(L_BS + self.L_arm)
		x_BS_2 = x_BS_1 + L_BS + self.L_arm
		self.Xx[4] = x_BS_1
		self.Xx[5] = x_BS_2
		
		# middle
		end_point.change(x_BS_1, 0.0, self.Zz[3])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, 0.0, self.Zz[4])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		# down
		end_point.change(x_BS_1, -2.0*H_BS, self.Zz[3])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, -2.0*H_BS, self.Zz[4])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		# up
		end_point.change(x_BS_1, 2.0*H_BS, self.Zz[3])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, 2.0*H_BS, self.Zz[4])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
	def Arms_1(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		L_BS = 2.0*self.sb_length + self.cp_length
		H_BS = 2.0*self.sb_height + self.width_Cr
		x_side = 0.0
		x_arms_1 = self.L_side + L_BS + self.extension/2.0
		x_arms_2 = x_arms_1 + self.L_arm + L_BS
		length_side = self.L_side - self.extension/2.0
		length_arm = self.L_arm - self.extension
		zz_side = self.Zz[0]
		zz_1 = (self.Zz[0] + self.Zz[1])/2.0
		zz_2 = (self.Zz[1] + self.Zz[2])/2.0
		
		# middle
		end_point.change(x_side, -H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_side, H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_arms_1, -H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, -H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		# up
		end_point.change(x_side, 2.0*H_BS - H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_side, 2.0*H_BS + H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_arms_1, 2.0*H_BS - H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, 2.0*H_BS + H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, 2.0*H_BS - H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, 2.0*H_BS + H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		# down
		end_point.change(x_side, -2.0*H_BS - H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_side, -2.0*H_BS + H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_arms_1, -2.0*H_BS - H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, -2.0*H_BS + H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, -2.0*H_BS - H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, -2.0*H_BS + H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
	def Arms_2(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		L_BS = 2.0*self.sb_length + self.cp_length
		H_BS = 2.0*self.sb_height + self.width_Cr
		x_side = self.L_side + 2.0*(L_BS + self.L_arm) - 0.5*self.extension
		x_arms_1 = self.L_side + 2.0*(L_BS + self.L_arm) + L_BS + self.extension/2.0
		x_arms_2 = x_arms_1 + self.L_arm + L_BS
		length_side = 2.0*(L_BS + self.L_arm) + 0.5*self.extension
		length_arm = self.L_arm - self.extension
		zz_side = (self.Zz[1] + self.Zz[4])/2.0
		zz_1 = (self.Zz[2] + self.Zz[3])/2.0
		zz_2 = (self.Zz[3] + self.Zz[4])/2.0
		
		# side
		end_point.change(x_side, 2.0*H_BS + H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_side, -2.0*H_BS - H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		# up
		end_point.change(x_arms_1, H_BS - H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, H_BS + H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, H_BS - H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, H_BS + H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		# down
		end_point.change(x_arms_1, -H_BS - H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, -H_BS + H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, -H_BS - H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, -H_BS + H_BS/2.0, zz_2)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
	def Arms_3(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		L_BS = 2.0*self.sb_length + self.cp_length
		H_BS = 2.0*self.sb_height + self.width_Cr
		x_arms_1 = self.L_side + 4.0*(L_BS + self.L_arm) + L_BS + self.extension/2.0
		x_arms_2 = x_arms_1 + self.L_arm + L_BS
		length_side = self.L_side - self.extension/2.0
		length_arm = self.L_arm - self.extension
		zz_side = self.Zz[5]
		zz_1 = (self.Zz[4] + self.Zz[5])/2.0
		
		# middle
		end_point.change(x_arms_1, -H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, -H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_arms_2, H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		# up
		end_point.change(x_arms_1, 2.0*H_BS - H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, 2.0*H_BS + H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, 2.0*H_BS - H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_arms_2, 2.0*H_BS + H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		# down
		end_point.change(x_arms_1, -2.0*H_BS - H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_1, -2.0*H_BS + H_BS/2.0, zz_1)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_arm)
		
		end_point.change(x_arms_2, -2.0*H_BS - H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		end_point.change(x_arms_2, -2.0*H_BS + H_BS/2.0, zz_side)
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, length_side)
		
		
directory = os.path.splitext(os.path.basename(__file__))[0]
print('Writing')
Unitary_Operator_3lay(directory)

(x_min, x_max) = (-1.0, 21.0)
(y_min, y_max) = (-0.2, 0.2)
key = 1
Code_Visualization(directory, 'test', x_min, x_max, y_min, y_max, key)

