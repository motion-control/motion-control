# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import os
from math import *

class DynamicArray():
	def __init__(self):
		self._data = np.zeros(10)
		self._size = 0
		
	def get_data(self):
		return self._data[:self._size]
		
	def append(self, value):
		if len(self._data) == self._size:
			self._data = np.resize(self._data, int(len(self._data)*1.25))
		self._data[self._size] = value
		self._size += 1
		
class Point():
	def __init__(self, x, y, z=-9999):
		self.x = x
		self.y = y
		self.z = z
		
	def add(self, x, y, z=-9999):
		self.x += x
		self.y += y
		self.z = z if z==-9999 else self.z + z
		
	def x_add(self, x):
		self.x += x
		
	def y_add(self, y):
		self.y += y
		
	def z_add(self, z):
		self.z += z
		
	def change(self, x, y, z=-9999):
		self.x = x
		self.y = y
		self.z = z
		
	def x_change(self, x):
		self.x = x
		
	def y_change(self, y):
		self.y = y
		
	def z_change(self, z):
		self.z = z
		
class Basic_Motion():
	X = 999.0
	Y = 999.0
	Z = 999.0
	VELOCITY = 3.0
	FILE = type('file', (), {})()
	ex_width = 0.01
	
	def file_create(self, directory, filename):
		file_directory = os.getcwd() + '/code/' + directory
		suffix = '.pgm'
		entire_filename = file_directory + '/' + filename + suffix
		
		if not os.path.exists(file_directory):
			os.makedirs(file_directory)
			
		self.FILE = open(entire_filename, 'w')
		self.FILE.write("DVAR $Myi\n")
		self.FILE.write("G90\n")
		self.FILE.write("F{:.6f}\n".format(self.VELOCITY))
		
		
	def g_line(self, Point):
		if Point.z == -9999:
			if not (Point.x == self.X and Point.y == self.Y):
				self.FILE.write("F{:.6f}\n".format(self.VELOCITY))
				self.FILE.write("G1 X{:.6f} Y{:.6f}\n".format(Point.x, Point.y))
				self.X = Point.x
				self.Y = Point.y
		else:
			if not (Point.x == self.X and Point.y == self.Y and Point.z == self.Z):
				self.FILE.write("F{:.6f}\n".format(self.VELOCITY))
				self.FILE.write("G1 X{:.6f} Y{:.6f} Z{:.6f}\n".format(Point.x, Point.y, Point.z))
				self.X = Point.x
				self.Y = Point.y
				self.Z = Point.z
				
	
	def loop_head(self, loop):
		self.FILE.write("FOR $Myi = 1 TO {:d} STEP 1\n".format(loop))

	def loop_end(self):
		self.FILE.write("NEXT $Myi\n")
				
	def shutter(self, key):
		if key==0:
			self.FILE.write("$DO[8].X = 1\n")
		else:
			self.FILE.write("$DO[8].X = 0\n")
			
			
	def g_spot(self, Point):
		self.shutter(1)
		if Point.z == -9999:
			self.FILE.write("G0 X{:.6f} Y{:.6f}\n".format(Point.x, Point.y))
		else:
			self.FILE.write("G0 X{:.6f} Y{:.6f} Z{:.6f}\n".format(Point.x, Point.y, Point.z))
			Point.z = -9999
		self.FILE.write("DWELL 0.1\n")
		self.X = Point.x
		self.Y = Point.y
		
		
	def g_arc(self, c_x, c_y, r, phi, Point):
		if phi > 0:
			head = 'G2 '
		else:
			head = 'G3 '
		if self.X - c_x >=0:
			rr = (self.Y - c_y)
			if rr > 1.0:
				rr = 1.0
			if rr < -1.0:
				rr = -1.0
			ang_0 = acos(rr)
		else:
			rr = (self.Y - c_y)/r
			if rr > 1.0:
				rr = 1.0
			if rr < -1.0:
				rr = -1.0
			ang_0 = 2.0 * pi - acos(rr)
		end_angle = ang_0 + phi
		x0 = c_x + r * sin(end_angle)
		y0 = c_y + r * cos(end_angle)
		I = c_x - self.X
		J = c_y - self.Y
		self.X = x0
		self.Y = y0
		Point.x = self.X
		Point.y = self.Y
		command = head + 'X{:.6f} Y{:.6f} I{:.6f} J{:.6f}\n'.format(self.X, self.Y, I, J)
		self.FILE.write(command)
		
		
	def bezier(self, x1, y1, Point, x2=-999, y2=-999):
		if x2 == -999:
			command = "BEZIER QUAD X, {:.6f}, {:.6f}, {:.6f}, Y, {:.6f}, {:.6f}, {:.6f}\n".format(self.X, x1, Point.x, self.Y, y1, Point.y)
			self.FILE.write(command)
		else:
			command = "BEZIER CUBIC X, {:.6f}, {:.6f}, {:.6f}, {:.6f}, Y, {:.6f}, {:.6f}, {:.6f}, {:.6f}\n".format(self.X, x1, x2, Point.x, self.Y, y1, y2, Point.y)
			self.FILE.write(command)
		self.X = Point.x
		self.Y = Point.y
		
		
	def bezier_cubic_calculator(self, L, H, d, h):
		x0 = (L**2 + H**2)/(4.0*L)
		move = d*sin(0.5*atan(H/(L - 2*x0)))# + H*L/(fabs(H*L))*(d/fabs(d))*self.ex_width
		
		Y0 = 0.0
		Y1 = 0.0
		Y2 = H
		Y3 = H
		
		precision = 0.00001
		t_max = 1.0
		t_min = 0.0
		t = (t_max + t_min)/2.0
		
		while t_max - t_min > precision:
			y = (1.0 - t)**3*Y0 + 3.0*(1.0 - t)**2*t*Y1 + 3.0*(1.0 - t)*t**2*Y2 + t**3*Y3
			if y < h:
				t_min = t
			else:
				t_max = t
			t = (t_max + t_min)/2.0
			
		return t
		
		
	def x_rect_PSO(self, y_inc_or_dec, num_of_layers, length, step):
		Vel = 40
		t0 = 0.04
		l0 = 0.852
		l_sum = length + l0 * 2
		Dt = int((length/Vel)*1000000)
		
		if y_inc_or_dec == 1:
			step = -step
			
		self.FILE.write('PSOCONTROL X RESET\n')
		self.FILE.write('PSOPULSE X TIME {:.0f}, {:.0f} CYCLES 1\n'.format(Dt, Dt))
		self.FILE.write('PSOOUTPUT X PULSE\n')
		self.FILE.write('G91\n')
		self.FILE.write('G0 X{:.6f} Y{:.6f}\n'.format(-l0, -step))
		self.FILE.write('MOVEINC X{:.6f} {:.6f}\n'.format(l_sum, Vel))
		self.FILE.write('DWELL {:.6f}\n'.format(t0))
		self.FILE.write('WAIT MOVEDONE X\n')
		self.FILE.write('G0 X{:.6f} Y{:.6f}\n'.format(-l_sum, step))
		
		for i in range(0, num_of_layers):
			self.FILE.write('MOVEINC X{:.6f} {:.6f}\n'.format(l_sum, Vel))
			self.FILE.write('DWELL {:.6f}\n'.format(t0))
			self.FILE.write('PSOCONTROL X FIRE\n')
			self.FILE.write('WAIT MOVEDONE X\n')
			self.FILE.write('G0 X{:.6f} Y{:.6f}\n'.format(-l_sum, step))
			
		self.FILE.write('G90\n')
		
		
	def y_rect_PSO(self, x_inc_or_dec, num_of_layers, length, step):
		Vel = 40
		t0 = 0.04
		l0 = 0.852
		l_sum = length + l0 * 2
		Dt = int((length/Vel)*1000000)
		
		if x_inc_or_dec == 1:
			step = -step
			
		self.FILE.write('PSOCONTROL Y RESET\n')
		self.FILE.write('PSOPULSE Y TIME {:.0f}, {:.0f} CYCLES 1\n'.format(Dt, Dt))
		self.FILE.write('PSOOUTPUT Y PULSE\n')
		self.FILE.write('G91\n')
		self.FILE.write('G0 X{:.6f} Y{:.6f}\n'.format(-step, -l0))
		self.FILE.write('MOVEINC Y{:.6f} {:.6f}\n'.format(l_sum, Vel))
		self.FILE.write('DWELL {:.6f}\n'.format(t0))
		self.FILE.write('WAIT MOVEDONE Y\n')
		self.FILE.write('G0 X{:.6f} Y{:.6f}\n'.format(step, -l_sum))
		
		for i in range(0, num_of_layers):
			self.FILE.write('MOVEINC Y{:.6f} {:.6f}\n'.format(l_sum, Vel))
			self.FILE.write('DWELL {:.6f}\n'.format(t0))
			self.FILE.write('PSOCONTROL Y FIRE\n')
			self.FILE.write('WAIT MOVEDONE Y\n')
			self.FILE.write('G0 X{:.6f} Y{:.6f}\n'.format(step, -l_sum))
			
		self.FILE.write('G90\n')
		
		
	# d>0 means y > y0
	def bezier_s_bent(self, Point, d):
		L = Point.x - self.X
		H = Point.y - self.Y
		x0 = (L**2 + H**2)/(4.0*L)
		move = d*sin(0.5*atan(H/(L - 2.0*x0))) + H*L/(fabs(H*L))*(d/fabs(d))*self.ex_width
		
		X0 = self.X
		X1 = X0 + x0 - move
		X2 = X0 + L - x0 - move
		X3 = X0 + L
		
		Y0 = self.Y
		Y1 = Y0
		Y2 = Y0 + H
		Y3 = Y2
		
		self.bezier(X1, Y1, Point, x2=X2, y2=Y2)
		
		
	def bezier_s_bent_back(self, Point, w_wg, d):
		L = Point.x - self.X
		H = Point.y - self.Y
		x0 = (L**2 + H**2)/(4.0*L)
		move = d*sin(0.5*atan(H/(L - 2*x0))) + H*L/(fabs(H*L))*(d/fabs(d))*self.ex_width
		h = H + w_wg/2.0 - d
		t = self.bezier_cubic_calculator(L, H, d, h)
		
		X0 = self.X
		X1 = X0 + x0 - move
		X2 = X0 + L - x0 - move
		X3 = X0 + L
		
		Y0 = self.Y
		Y1 = Y0
		Y2 = Y0 + H
		Y3 = Y2
		Y_middle = Y0 + h
		
		Px = (1.0 - t)**3*X0 + 3.0*(1.0 - t)**2*t*X1 + 3.0*(1.0 - t)*t**2*X2 + t**3*X3
		Py = Y0 + h
		A = (3.0*(1.0 - t)**2*(Y1 - Y0) + 6.0*(1.0 - t)*t*(Y2 - Y1) + 3.0*t**2*(Y3 - Y2))\
		/(3.0*(1.0 - t)**2*(X1 - X0) + 6.0*(1.0 - t)*t*(X2 - X1) + 3.0*t**2*(X3 - X2))
		
		if Py > Y0 + H*0.5:
			X2 = (-A*Px*(L - 2.0*x0) + H*X1 + L*(Py - Y1) - 2.0*Py*x0 + 2.0*x0*Y1)/\
			(-A*L + 2*A*x0 + H)
			
			
			Y2 = (A*(-H*Px + H*X1 - L*Y1 + 2*x0*Y1) + H*Py)/(-A*L + 2*A*x0 + H)
			Point.x = Px
			Point.y = Py
			
			self.bezier(X1, Y1, Point, x2=X2, y2=Y2)
			
			X0_mirror = self.X
			Y0_mirror = self.Y
			X1_mirror = X2
			Y1_mirror = 2.0*Y_middle - Y2
			X2_mirror = X1
			Y2_mirror = 2.0*Y_middle - Y1
			
			Point.x = X0
			Point.y = 2.0*Y_middle - Y0
			
			self.bezier(X1_mirror, Y1_mirror, Point, x2=X2_mirror, y2=Y2_mirror)
			
		else:
			X1 = (Y0-Py)/A + Px
			X2 = X1
			Y1 = Y0
			Y2 = Y1
			Point.x = Px
			Point.y = Py
			self.bezier(X1, Y1, Point)
			X0_mirror = self.X
			Y0_mirror = self.Y
			X1_mirror = X2
			Y1_mirror = 2.0 * Y_middle - Y2
			X2_mirror = X1
			Y2_mirror = 2.0 * Y_middle - Y1
			Point.x = X0
			Point.y = 2.0 * Y_middle - Y0
			self.bezier(X1_mirror, Y1_mirror, Point)
			
pass

