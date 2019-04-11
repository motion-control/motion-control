from Motion_Modules.Basic.Basic_Motion import *
from Motion_Modules.Basic.Code_Visualization import *
from Motion_Modules.Motion_Modules import *
from math import *

class Perfect_MZI_Loss(Motion_Modules):
	width_Cr = 0.0022
	width_LN = 0.0064
	cp_length = 0.12
	sb_length = 0.5
	sb_height = 0.03
	layer_Cr = 3
	layer_LN = 25
	step = 0.0008
	
	# bent
	R_bent = 1.8
	Dir_bent = 1 # 0 for up, 1 for down
	Tail_extension = 0.5
	
	L_arm_side = 1.5
	L_arm_middle = 2.5
	L_loss = 5.0
	L_sum = 20.0
	extension = 0.0
	Zz = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	Xx = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	L_BS = sb_length*2.0 + cp_length
	H_BS = 2.0*sb_height + width_Cr
	L_side = (L_sum - (2.0*(L_BS + L_arm_side) + (L_BS + L_arm_middle)\
	+ (L_BS + L_loss) + R_bent))/2.0
	print("L_side: {:.3f}".format(L_side))
	
	
	def __init__(self, directory):
		self.file_create(directory, 'Cr_1')
		self.loop_head(1)
		self.BS_1(0)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'Cr_2')
		self.loop_head(1)
		self.BS_2(0)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'Cr_3')
		self.loop_head(1)
		self.Bent_waveguides(0)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'LN_1')
		self.loop_head(1)
		self.BS_1(1)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'LN_2')
		self.loop_head(1)
		self.BS_2(1)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'LN_3')
		self.loop_head(1)
		self.Bent_waveguides(1)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'Arms_Cr_1')
		self.loop_head(1)
		self.Arms_1(0)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'Arms_LN_1')
		self.loop_head(1)
		self.Arms_1(1)
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'Electrods_1')
		self.loop_head(1)
		self.Electrods_1()
		self.loop_end()
		self.FILE.close()
		
		self.file_create(directory, 'test')
		self.BS_1(0)
		self.BS_1(1)
		self.BS_2(0)
		self.BS_2(1)
		self.Bent_waveguides(0)
		self.Bent_waveguides(1)
		self.Arms_1(0)
		self.Arms_1(1)
		self.Arms_2(0)
		self.Arms_2(1)
		self.Electrods_1()
		self.Electrods_2()
		self.Electrods_3()
		self.FILE.close()
		
		self.file_create(directory, 'Ele_test')
		self.Electrods_1()
		self.Electrods_2()
		self.Electrods_3()
		self.FILE.close()
		
		print('G0 X{:.6f} Y0.0'.format(self.Xx[0]))
		
	def BS_1(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		x_BS_1 = self.L_side
		x_BS_2 = x_BS_1 + self.L_BS + self.L_arm_side
		self.Xx[0] = x_BS_1
		self.Xx[1] = x_BS_2
		
		end_point.change(x_BS_1, 0.0, self.Zz[0]) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, 0.0, self.Zz[1])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
	def BS_2(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		x_BS_1 = self.L_side + (2.0*self.L_BS + self.L_arm_side + self.L_arm_middle)
		x_BS_2 = x_BS_1 + self.L_BS + self.L_arm_side
		self.Xx[2] = x_BS_1
		self.Xx[3] = x_BS_2
		
		end_point.change(x_BS_1, 0.0, self.Zz[2]) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
		end_point.change(x_BS_2, 0.0, self.Zz[3])
		self.g_spot(end_point)
		self.shutter(1)
		self.Beam_Spliter(Cr_or_LN)
		
	def Bent_waveguides(self, Cr_or_LN):
		end_point = Point(0.0, 0.0)
		(L_BS, H_BS) = (self.L_BS, self.H_BS)
		x_bw_1 = self.L_side + 2.0*(L_BS + self.L_arm_side) + \
		(L_BS + self.L_arm_middle) + L_BS + self.extension
		x_bw_2 = x_bw_1 + self.L_loss - self.extension
		(y_bw_1, y_bw_2) = (H_BS/2.0, -H_BS/2.0) if self.Dir_bent==0 \
		else (-H_BS/2.0, H_BS/2.0)
		self.Xx[4] = x_bw_1
		self.Xx[5] = x_bw_2
		
		end_point.change(x_bw_1, y_bw_1, self.Zz[4]) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Bent_Waveguide(Cr_or_LN)
		
		end_point.change(x_bw_2, y_bw_2, self.Zz[5]) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Bent_Waveguide(Cr_or_LN)
		
		
	def Arms_1(self, Cr_or_LN):
		H_BS = self.H_BS
		end_point = Point(0.0, 0.0)
		x_side = 0.0
		x_arm_1 = self.L_side + self.L_BS + self.extension/2.0
		x_arm_2 = x_arm_1 + self.L_BS + self.L_arm_side
		
		l_side = self.L_side - 0.5*self.extension
		l_arm_1 = self.L_arm_side - self.extension
		l_arm_2 = self.L_arm_middle - self.extension
		
		z_side = self.Zz[0]
		z_arm_1 = (self.Zz[0] + self.Zz[1])/2.0
		z_arm_2 = (self.Zz[1] + self.Zz[2])/2.0
		
		end_point.change(x_side, 0.5*H_BS, z_side) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_side)
		end_point.change(x_side, -0.5*H_BS, z_side) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_side)
		
		end_point.change(x_arm_1, 0.5*H_BS, z_arm_1) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_arm_1)
		end_point.change(x_arm_1, -0.5*H_BS, z_arm_1) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_arm_1)
		
		end_point.change(x_arm_2, 0.5*H_BS, z_arm_2) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_arm_2)
		end_point.change(x_arm_2, -0.5*H_BS, z_arm_2) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_arm_2)
		
	def Arms_2(self, Cr_or_LN):
		H_BS = self.H_BS
		end_point = Point(0.0, 0.0)
		x_arm_1 = self.L_side + (self.L_BS + self.L_arm_side)\
		+ (self.L_BS + self.L_arm_middle) + self.L_BS + self.extension/2.0
		x_arm_2 = x_arm_1 + self.L_BS + self.L_arm_side
		
		l_arm_1 = self.L_arm_side - self.extension
		l_arm_2 = self.L_loss - self.extension
		
		z_arm_1 = (self.Zz[2] + self.Zz[3])/2.0
		z_arm_2 = (self.Zz[4] + self.Zz[5])/2.0
		
		end_point.change(x_arm_1, 0.5*H_BS, z_arm_1) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_arm_1)
		end_point.change(x_arm_1, -0.5*H_BS, z_arm_1) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_arm_1)
		
		HH = 0.5*self.H_BS if self.Dir_bent == 1 else -0.5*self.H_BS
		end_point.change(x_arm_2, HH, z_arm_2) # two parameters is OK too
		self.g_spot(end_point)
		self.shutter(1)
		self.Waveguide_x(Cr_or_LN, l_arm_2)
		
	def Electrods_1(self):
		end_point = Point(0.0, 0.0)
		(L_BS, H_BS, L_side, L_arm_side, L_arm_middle) = (self.L_BS, self.H_BS,\
		self.L_side, self.L_arm_side, self.L_arm_middle)
		width_ord_groove = 0.03
		width_ele_groove = 0.01
		width_ele = 0.07
		
		x_ele = [0.0]*8
		y_ele = [0.0]*8
		l = [0.0]*8
		h = [0.0]*8
		
		(x_ele[0], y_ele[0]) = (L_side + L_BS - width_ord_groove, -H_BS/2.0 - width_ele_groove - 4.0*(width_ele + width_ord_groove))
		(x_ele[1], y_ele[1]) = (x_ele[0], y_ele[0])
		(x_ele[2], y_ele[2]) = (x_ele[0], H_BS/2.0 + width_ele_groove/2.0 + width_ele)
		(x_ele[3], y_ele[3]) = (x_ele[0] + width_ord_groove, H_BS/2.0 - width_ele_groove/2.0)
		(x_ele[4], y_ele[4]) = (x_ele[3] + L_arm_side - width_ord_groove, -H_BS/2.0 - width_ele_groove/2.0)
		(x_ele[5], y_ele[5]) = (x_ele[3] + width_ele, y_ele[4])
		(x_ele[6], y_ele[6]) = (x_ele[5], y_ele[5] - 3.0*(width_ele + width_ord_groove))
		(x_ele[7], y_ele[7]) = (x_ele[6], y_ele[6])
		
		(l[0], h[0]) = (width_ord_groove, H_BS + width_ele_groove + 5.0*(width_ele + width_ord_groove))
		(l[1], h[1]) = (width_ord_groove + L_arm_side + L_BS, width_ord_groove)
		(l[2], h[2]) = (l[1], h[1])
		(l[3], h[3]) = (L_arm_side, width_ele_groove)
		(l[4], h[4]) = (width_ord_groove, H_BS + width_ele_groove)
		(l[5], h[5]) = (l[3] - width_ele, h[3])
		(l[6], h[6]) = (width_ord_groove, 3.0*(width_ele + width_ord_groove))
		(l[7], h[7]) = (L_arm_side + L_BS, width_ord_groove)
		
		for i in range(0, 8):
			end_point.change(x_ele[i], y_ele[i])
			self.g_spot(end_point)
			self.Rectangle(l[i], h[i])
			
	def Electrods_2(self):
		end_point = Point(0.0, 0.0)
		(L_BS, H_BS, L_side, L_arm_side, L_arm_middle) = (self.L_BS, self.H_BS,\
		self.L_side, self.L_arm_side, self.L_arm_middle)
		width_ord_groove = 0.03
		width_ele_groove = 0.01
		width_ele = 0.07
		
		x_ele = [0.0]*9
		y_ele = [0.0]*9
		l = [0.0]*9
		h = [0.0]*9
		
		(x_ele[0], y_ele[0]) = (L_side + L_BS*2.0 + L_arm_side - width_ord_groove, -H_BS/2.0 - width_ele_groove/2.0 - 3.0*(width_ele + width_ord_groove))
		(x_ele[1], y_ele[1]) = (x_ele[0], -H_BS/2.0 - width_ele_groove - 4.0*(width_ele + width_ord_groove))
		(x_ele[2], y_ele[2]) = (x_ele[0], H_BS/2.0 + width_ele_groove/2.0 + width_ele)
		(x_ele[3], y_ele[3]) = (x_ele[0] + width_ord_groove, H_BS/2.0 - width_ele_groove/2.0)
		(x_ele[4], y_ele[4]) = (x_ele[3] + L_arm_middle - width_ord_groove, -H_BS/2.0 - width_ele_groove/2.0)
		(x_ele[5], y_ele[5]) = (x_ele[3] + width_ele, y_ele[4])
		(x_ele[6], y_ele[6]) = (x_ele[5], y_ele[5] - 2.0*(width_ele + width_ord_groove))
		(x_ele[7], y_ele[7]) = (x_ele[6], y_ele[6])
		(x_ele[8], y_ele[8]) = (x_ele[0], y_ele[0])
		
		(l[0], h[0]) = (width_ord_groove, H_BS + width_ele_groove + 3.0*(width_ele + width_ord_groove))
		(l[1], h[1]) = (width_ord_groove + L_arm_middle + L_BS, width_ord_groove)
		(l[2], h[2]) = (l[1], h[1])
		(l[3], h[3]) = (L_arm_middle, width_ele_groove)
		(l[4], h[4]) = (width_ord_groove, H_BS + width_ele_groove)
		(l[5], h[5]) = (l[3] - width_ele, h[3])
		(l[6], h[6]) = (width_ord_groove, 2.0*(width_ele + width_ord_groove))
		(l[7], h[7]) = (L_arm_middle + L_BS, width_ord_groove)
		(l[8], h[8]) = (L_arm_middle + L_BS, width_ord_groove)
		
		for i in range(0, 9):
			end_point.change(x_ele[i], y_ele[i])
			self.g_spot(end_point)
			self.Rectangle(l[i], h[i])
			
	def Electrods_3(self):
		end_point = Point(0.0, 0.0)
		(L_BS, H_BS, L_side, L_arm_side, L_arm_middle) = (self.L_BS, self.H_BS,\
		self.L_side, self.L_arm_side, self.L_arm_middle)
		width_ord_groove = 0.03
		width_ele_groove = 0.01
		width_ele = 0.07
		
		x_ele = [0.0]*14
		y_ele = [0.0]*14
		l = [0.0]*14
		h = [0.0]*14
		
		(x_ele[0], y_ele[0]) = (L_side + L_BS*3.0 + L_arm_side + L_arm_middle - width_ord_groove, -H_BS/2.0 - width_ele_groove/2.0 - 2.0*(width_ele + width_ord_groove))
		(x_ele[1], y_ele[1]) = (x_ele[0], -H_BS/2.0 - width_ele_groove - 4.0*(width_ele + width_ord_groove))
		(x_ele[2], y_ele[2]) = (x_ele[0], H_BS/2.0 + width_ele_groove/2.0 + width_ele)
		(x_ele[3], y_ele[3]) = (x_ele[0] + width_ord_groove, H_BS/2.0 - width_ele_groove/2.0)
		(x_ele[4], y_ele[4]) = (x_ele[3] + L_arm_side - width_ord_groove, -H_BS/2.0 - width_ele_groove/2.0)
		(x_ele[5], y_ele[5]) = (x_ele[3] + width_ele, y_ele[4])
		(x_ele[6], y_ele[6]) = (x_ele[5], y_ele[5] - 1.0*(width_ele + width_ord_groove))
		(x_ele[7], y_ele[7]) = (x_ele[6], y_ele[6])
		(x_ele[8], y_ele[8]) = (x_ele[0], y_ele[0])
		(x_ele[9], y_ele[9]) = (x_ele[0], y_ele[0] - (width_ele + width_ord_groove))
		(x_ele[10], y_ele[10]) = (x_ele[9] + L_arm_side + width_ord_groove - 3.0*width_ord_groove - 2.0*width_ele, -H_BS/2.0 - width_ele_groove - 4.0*(width_ele + width_ord_groove) + width_ord_groove)
		(x_ele[11], y_ele[11]) = (x_ele[10] + width_ele + width_ord_groove, y_ele[10])
		(x_ele[12], y_ele[12]) = (x_ele[11] + width_ele + width_ord_groove, y_ele[10])
		(x_ele[13], y_ele[13]) = (x_ele[12] + width_ele + width_ord_groove, y_ele[10])
		
		(l[0], h[0]) = (width_ord_groove, H_BS + width_ele_groove + 2.0*(width_ele + width_ord_groove))
		(l[1], h[1]) = (width_ord_groove + L_arm_side + width_ele + width_ord_groove, width_ord_groove)
		(l[2], h[2]) = (l[1], h[1])
		(l[3], h[3]) = (L_arm_side, width_ele_groove)
		(l[4], h[4]) = (width_ord_groove, H_BS + width_ele_groove)
		(l[5], h[5]) = (l[3] - width_ele, h[3])
		(l[6], h[6]) = (width_ord_groove, 1.0*(width_ele + width_ord_groove))
		(l[7], h[7]) = (L_arm_side - width_ele, width_ord_groove)
		(l[8], h[8]) = (L_arm_side + width_ord_groove - 1.0*width_ord_groove - width_ele, width_ord_groove)
		(l[9], h[9]) = (L_arm_side + width_ord_groove - 2.0*width_ord_groove - 2.0*width_ele, width_ord_groove)
		(l[10], h[10]) = (width_ord_groove, width_ele + width_ord_groove)
		(l[11], h[11]) = (width_ord_groove, h[10] + width_ele + width_ord_groove)
		(l[12], h[12]) = (width_ord_groove, h[11] + width_ele + width_ord_groove)
		(l[13], h[13]) = (width_ord_groove, H_BS + width_ele_groove + 5.0*(width_ele + width_ord_groove) - width_ord_groove)
		
		for i in range(0, 14):
			end_point.change(x_ele[i], y_ele[i])
			self.g_spot(end_point)
			self.Rectangle(l[i], h[i])
			
			
			
			
			
			
directory = os.path.splitext(os.path.basename(__file__))[0]
print('Writing')
Perfect_MZI_Loss(directory)

(x_min, x_max) = (2.5, 11)
(y_min, y_max) = (-0.5, 0.2)
key = 0
Code_Visualization(directory, 'test', x_min, x_max, y_min, y_max, key)

