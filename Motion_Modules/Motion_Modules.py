# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from .Basic.Basic_Motion import *
from math import *

class Motion_Modules(Basic_Motion):
	width_Cr = 0.0022
	width_LN = 0.0064
	cp_length = 0.13
	sb_length = 0.5
	sb_height = 0.03
	layer_Cr = 3
	layer_LN = 25
	extension = 0.1
	step = 0.0008
	# bent
	R_bent = 1.8
	Dir_bent = 0 # 0 for up, 1 for down
	Tail_extension = 0.5
	
	def Beam_Spliter(self, Cr_or_LN):
		X_reg = self.X - self.extension
		Y_reg = self.Y
		end_point = Point(X_reg, Y_reg)
		
		(n_layer, d0) = (self.layer_Cr, self.width_Cr/2.0 + self.step/2.0) if Cr_or_LN == 0\
		else (self.layer_LN, self.width_LN/2.0 + self.step/2.0)
		
		# inside_0
		d = d0
		end_point.y = Y_reg - self.width_Cr/2.0 - self.sb_height + d
		self.g_spot(end_point)
		self.shutter(1)
		i = 0
		while i < n_layer:
			self.g_line(end_point)
			end_point.x += self.extension
			self.g_line(end_point)
			end_point.add(self.sb_length, self.sb_height)
			self.bezier_s_bent_back(end_point, self.width_Cr, d)
			self.g_line(end_point)
			end_point.x -= self.extension
			self.g_line(end_point)
			end_point.y -= (2.0*self.sb_height + self.width_Cr - 2.0*d - self.step)
			d += self.step
			i += 1
			
		# outside_0
		d = d0
		end_point.y = Y_reg - self.width_Cr/2.0 - self.sb_height - d
		self.X = X_reg
		self.g_spot(end_point)
		self.shutter(1)
		i = 0
		while i < n_layer:
			self.g_line(end_point)
			end_point.x += self.extension
			self.g_line(end_point)
			end_point.add(self.sb_length, self.sb_height)
			self.bezier_s_bent(end_point, -d)
			end_point.x += self.cp_length
			self.g_line(end_point)
			end_point.add(self.sb_length, -self.sb_height)
			self.bezier_s_bent(end_point, -d)
			end_point.x += self.extension
			self.g_line(end_point)
			end_point.y -= self.step
			self.g_line(end_point)
			d += self.step
			i += 1
			if i >= n_layer:
				break
			end_point.x_add(-self.extension)
			self.g_line(end_point)
			end_point.add(-self.sb_length, self.sb_height)
			self.bezier_s_bent(end_point, -d)
			end_point.x -= self.cp_length
			self.g_line(end_point)
			end_point.add(-self.sb_length, -self.sb_height)
			self.bezier_s_bent(end_point, -d)
			end_point.x -= self.extension
			self.g_line(end_point)
			end_point.y -= self.step
			d += self.step
			i += 1
			
		# outside_1
		d = d0
		end_point.change(X_reg, Y_reg + self.width_Cr/2.0 + self.sb_height + d)
		self.g_spot(end_point)
		self.shutter(1)
		i = 0
		while i < n_layer:
			self.g_line(end_point)
			end_point.x += self.extension
			self.g_line(end_point)
			end_point.add(self.sb_length, -self.sb_height)
			self.bezier_s_bent(end_point, d)
			end_point.x += self.cp_length
			self.g_line(end_point)
			end_point.add(self.sb_length, self.sb_height)
			self.bezier_s_bent(end_point, d)
			end_point.x += self.extension
			self.g_line(end_point)
			end_point.y += self.step
			self.g_line(end_point)
			d += self.step
			i += 1
			if i >= n_layer:
				break
				
			end_point.x_add(-self.extension)
			self.g_line(end_point)
			end_point.add(-self.sb_length, -self.sb_height)
			self.bezier_s_bent(end_point, d)
			end_point.x -= self.cp_length
			self.g_line(end_point)
			end_point.add(-self.sb_length, self.sb_height)
			self.bezier_s_bent(end_point, d)
			end_point.x -= self.extension
			self.g_line(end_point)
			end_point.y += self.step
			d += self.step
			i += 1
			
		# inside_1
		d = d0
		end_point.change(X_reg + 2.0*self.extension + 2.0*self.sb_length + self.cp_length,
		Y_reg - self.width_Cr/2.0 - self.sb_height + d)
		self.g_spot(end_point)
		self.shutter(1)
		i = 0
		while i < n_layer:
			self.g_line(end_point)
			end_point.x -= self.extension
			self.g_line(end_point)
			end_point.add(-self.sb_length, self.sb_height)
			self.bezier_s_bent_back(end_point, self.width_Cr, d)
			end_point.x += self.extension
			self.g_line(end_point)
			end_point.y -= (2.0*self.sb_height + self.width_Cr - 2.0*d - self.step)
			d += self.step
			i += 1
			
	def Waveguide_x(self, Cr_or_LN, length):
		X_reg = self.X
		Y_reg = self.Y
		end_point = Point(X_reg, Y_reg)
		
		(d0, n_layer) = (self.width_Cr/2.0 + self.step/2.0, self.layer_Cr) if Cr_or_LN == 0 \
		else (self.width_LN/2.0 + self.step/2.0, self.layer_LN)
		d = d0
		y_inc_or_dec = 0
		end_point.y_add(d)
		self.g_spot(end_point)
		self.x_rect_PSO(y_inc_or_dec, n_layer, length, self.step)
		
		y_inc_or_dec = 1
		end_point.change(X_reg, Y_reg)
		end_point.y_add(-d)
		self.g_spot(end_point)
		self.x_rect_PSO(y_inc_or_dec, n_layer, length, self.step)

	# scan_direction = 0 means horizontal 1 means vertical -1 means auto
	def Rectangle(self, L, H, scan_direction=-1):
		if scan_direction == -1:
			scan_direction = 0 if L > H else 1
		end_point = Point(self.X, self.Y)
		self.g_spot(end_point)
		if scan_direction == 0:
			n_layer = int(ceil(H/self.step))
			new_step = H/float(n_layer)			
			self.x_rect_PSO(0, n_layer, L, new_step)
		else:
			n_layer = int(ceil(L/self.step))
			new_step = L/float(n_layer)
			self.y_rect_PSO(0, n_layer, H, new_step)


	def Bent_Waveguide(self, Cr_or_LN):
		X_reg = self.X - self.extension
		Y_reg = self.Y
		end_point = Point(X_reg, Y_reg)

		(n_layer, d0) = (self.layer_Cr, self.width_Cr/2.0 + self.step/2.0) if Cr_or_LN == 0\
			else (self.layer_LN, self.width_LN/2.0 + self.step/2.0)
		(l0, h0, h_extension) = (self.R_bent, self.R_bent, self.Tail_extension)

		if self.Dir_bent == 0:
			(d, l, h) = (d0, l0 - d0, h0 - d0)
			end_point.y_add(d)
			i = 0
			while i < n_layer:
				self.g_line(end_point)
				end_point.x_add(self.extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x + l, end_point.y)
				end_point.add(l, h)
				self.bezier(X1, Y1, end_point)
				end_point.y_add(h_extension)
				self.g_line(end_point)
				end_point.x_add(-self.step)
				self.g_line(end_point)
				i += 1
				l += -self.step
				h += -self.step
				if i >= n_layer:
					break

				end_point.y_add(-h_extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x, end_point.y - h)
				end_point.add(-l, -h)
				self.bezier(X1, Y1, end_point)
				end_point.x_add(-self.extension)
				self.g_line(end_point)
				end_point.y_add(self.step)
				i += 1
				l += -self.step
				h += -self.step

			(d, l, h) = (d0, l0 + d0, h0 + d0)
			end_point.change(X_reg, Y_reg)
			end_point.y_add(-d)
			i = 0
			while i < n_layer:
				self.g_line(end_point)
				end_point.x_add(self.extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x + l, end_point.y)
				end_point.add(l, h)
				self.bezier(X1, Y1, end_point)
				end_point.y_add(h_extension)
				self.g_line(end_point)
				end_point.x_add(self.step)
				self.g_line(end_point)
				i += 1
				l += self.step
				h += self.step
				if i >= n_layer:
					break

				end_point.y_add(-h_extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x, end_point.y - h)
				end_point.add(-l, -h)
				self.bezier(X1, Y1, end_point)
				end_point.x_add(-self.extension)
				self.g_line(end_point)
				end_point.y_add(-self.step)
				i += 1
				l += self.step
				h += self.step

		else:
			(d, l, h) = (d0, l0 - d0, h0 - d0)
			end_point.y_add(-d)
			i = 0
			while i < n_layer:
				self.g_line(end_point)
				end_point.x_add(self.extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x + l, end_point.y)
				end_point.add(l, -h)
				self.bezier(X1, Y1, end_point)
				end_point.y_add(-h_extension)
				self.g_line(end_point)
				end_point.x_add(-self.step)
				self.g_line(end_point)
				i += 1
				l += -self.step
				h += -self.step
				if i >= n_layer:
					break

				end_point.y_add(h_extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x, end_point.y + h)
				end_point.add(-l, h)
				self.bezier(X1, Y1, end_point)
				end_point.x_add(-self.extension)
				self.g_line(end_point)
				end_point.y_add(-self.step)
				i += 1
				l += -self.step
				h += -self.step

			(d, l, h) = (d0, l0 + d0, h0 + d0)
			end_point.change(X_reg, Y_reg)
			end_point.y_add(d)
			i = 0
			while i < n_layer:
				self.g_line(end_point)
				end_point.x_add(self.extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x + l, end_point.y)
				end_point.add(l, -h)
				self.bezier(X1, Y1, end_point)
				end_point.y_add(-h_extension)
				self.g_line(end_point)
				end_point.x_add(self.step)
				self.g_line(end_point)
				i += 1
				l += self.step
				h += self.step
				if i >= n_layer:
					break

				end_point.y_add(h_extension)
				self.g_line(end_point)
				(X1, Y1) = (end_point.x, end_point.y + h)
				end_point.add(-l, h)
				self.bezier(X1, Y1, end_point)
				end_point.x_add(-self.extension)
				self.g_line(end_point)
				end_point.y_add(self.step)
				i += 1
				l += self.step
				h += self.step
			









		
	

