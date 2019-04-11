# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import numpy as np
import matplotlib. pyplot as plt
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
		
class Code_Visualization():
	X_track = DynamicArray()
	Y_track = DynamicArray()
	Flag = 0 #0 for G90; 1 for G91
	counter = 0 # omit the first and second G0 when G91
	Line = ''
	Resolution = 80.0
	Filename = ''
	suffix = '.pgm'
	X_min = 0.0
	X_max = 10.0
	Y_min = 0.0
	Y_max = 10.0
	Key = 0
	Direction = 0 # 0 for x, 1 for y
	
	
	def __init__(self, directory, filename, x_min, x_max, y_min, y_max, key):
		self.X_min = x_min
		self.X_max = x_max
		self.Y_min = y_min
		self.Y_max = y_max
		self.Key = key
		self.X_track.append(0)
		self.Y_track.append(0)
		self.Filename = os.getcwd() + '/code/' + directory + '/' + filename + self.suffix
		self.Fileread()
		self.plot()
		
	def plot(self):
		fig = plt.figure(figsize=(8,8), dpi=72,facecolor="white");
		axes = plt.subplot(111);
		
		plt.plot(self.X_track.get_data(), self.Y_track.get_data(), 'b-', linewidth=1.0)
		plt.plot(self.X_track.get_data()[0:2], self.Y_track.get_data()[0:2], 'ro-', linewidth=1.0)
		# plt.axis('equal')
		if self.Key:
			plt.xlim(self.X_min, self.X_max)
			plt.ylim(self.Y_min, self.Y_max)
		else:
			plt.axis('equal')
		plt.ylabel('Y(mm)')
		plt.xlabel('X(mm)')
		plt.show()
		
	def Fileread(self):
		f = open(self.Filename, "r+");
		self.Line = f.readline();
		print('Reading')
		self.Classifier();
		while self.Line != '':
			self.Line = f.readline();
			self.Classifier();
			
	def Vector2theta(self, Vect_x, Vect_y):
		L = np.sqrt(Vect_x ** 2 + Vect_y ** 2);
		if Vect_x > 0 and Vect_y > 0:
			return np.arccos(Vect_x / L);
		elif Vect_x <= 0 and Vect_y > 0:
			return np.pi / 2.0 + np.arccos(Vect_y / L);
		elif Vect_x <= 0 and Vect_y <= 0:
			return np.pi + np.arccos(-Vect_x / L);
		else:
			return np.pi * 1.5 + np.arcsin(Vect_x / L);
			
			
	def Theta2point(self, theta, R, Cx, Cy):
		return R * np.cos(theta) + Cx, R * np.sin(theta) + Cy;
		
		
	def Classifier(self):
		if self.Line.find("G90") != -1:
			self.Flag = 0
		if self.Line.find("G91") != -1:
			self.Flag = 1
			self.counter = 0
		if self.Line.find("G0") != -1 and self.Flag == 0:
			self.myLine();
		if self.Line.find("G0") != -1 and self.Flag == 1:
			self.Line_PSO();
		if self.Line.find("MOVEINC") != -1:
			self.Moveinc();
		if self.Line.find("G1") != -1:
			self.myLine();
		if self.Line.find("G2") != -1:
			self.Arc_CW();
		if self.Line.find("G3") != -1:
			self.Arc_CCW();
		if self.Line.find("BEZIER QUAD") != -1:
			self.Bezier_Quad();
		if self.Line.find("BEZIER CUBIC") != -1:
			self.Bezier_Cubic();
			
			
	def myLine(self):
		self.X_track.append(float(self.Line[self.Line.find(" X") + 2: self.Line.find(" Y")]));
		self.Y_track.append(float(self.Line[self.Line.find(" Y") + 2: self.Line.find(" Z")]));
		
	def Line_PSO(self):
		if self.counter < 3:
			self.counter += 1
			return
		l0 = 0.852
		X0 = self.X_track.get_data()[self.X_track._size - 1];
		Y0 = self.Y_track.get_data()[self.Y_track._size - 1];
		dX = float(self.Line[self.Line.find(" X") + 2: self.Line.find(" Y")])
		dY = float(self.Line[self.Line.find(" Y") + 2: self.Line.find(" Z")])
		if self.Direction == 0:
			r_dX = dX/fabs(dX)*(fabs(dX) - 2.0*l0)
			r_dY = dY
		else:
			r_dX = dX
			r_dY = dY/fabs(dY)*(fabs(dY) - 2.0*l0)
		self.X_track.append(X0 + r_dX)
		self.Y_track.append(Y0 + r_dY)
		
	def Moveinc(self):
		if self.counter < 3:
			self.counter += 1
			if self.Line.find("X") != -1:
				self.Direction = 0
			if self.Line.find("Y") != -1:
				self.Direction = 1
			return
		l0 = 0.852
		X0 = self.X_track.get_data()[self.X_track._size - 1];
		Y0 = self.Y_track.get_data()[self.Y_track._size - 1];
		if self.Direction == 0:
			dX = float(self.Line[self.Line.find(" X") + 2: self.Line.find(" 40")])
			r_dX = dX/fabs(dX)*(fabs(dX) - 2.0*l0)
			r_dY = 0.0
		else:
			dY = float(self.Line[self.Line.find(" Y") + 2: self.Line.find(" 40")])
			r_dY = dY/fabs(dY)*(fabs(dY) - 2.0*l0)
			r_dX = 0.0
		self.X_track.append(X0 + r_dX)
		self.Y_track.append(Y0 + r_dY)
		
	def Arc_CW(self):
		X = float(self.Line[self.Line.find(" X") + 2: self.Line.find(" Y")]);
		Y = float(self.Line[self.Line.find(" Y") + 2: self.Line.find(" I")]);
		I = float(self.Line[self.Line.find(" I") + 2: self.Line.find(" J")]);
		J = float(self.Line[self.Line.find(" J") + 2:]);
		X0 = self.X_track.get_data()[self.X_track._size - 1];
		Y0 = self.Y_track.get_data()[self.Y_track._size - 1];
		Cx = X0 + I;
		Cy = Y0 + J;
		Vect_x_start = -I;
		Vect_y_start = -J;
		Vect_x_end = X - X0 - I;
		Vect_y_end = Y - Y0 - J;
		R = np.sqrt(I ** 2 + J ** 2);
		
		theta_start = self.Vector2theta(Vect_x_start, Vect_y_start);
		theta_end = self.Vector2theta(Vect_x_end, Vect_y_end);
		D_theta = theta_start - theta_end;
		if D_theta < 0:
			D_theta = D_theta + 2.0 * np.pi;
		if D_theta == 0:
			D_theta = 2.0 * np.pi;
		d_theta = D_theta / self.Resolution;
		
		for i in range(1, int(self.Resolution) + 1):
			self.X_track.append(self.Theta2point(theta_start - d_theta * i, R, Cx, Cy)[0]);
			self.Y_track.append(self.Theta2point(theta_start - d_theta * i, R, Cx, Cy)[1]);
			
	def Arc_CCW(self):
		X = float(self.Line[self.Line.find(" X") + 2: self.Line.find(" Y")]);
		Y = float(self.Line[self.Line.find(" Y") + 2: self.Line.find(" I")]);
		I = float(self.Line[self.Line.find(" I") + 2: self.Line.find(" J")]);
		J = float(self.Line[self.Line.find(" J") + 2:]);
		X0 = self.X_track.get_data()[self.X_track._size - 1];
		Y0 = self.Y_track.get_data()[self.Y_track._size - 1];
		Cx = X0 + I;
		Cy = Y0 + J;
		Vect_x_start = -I;
		Vect_y_start = -J;
		Vect_x_end = X - X0 - I;
		Vect_y_end = Y - Y0 - J;
		R = np.sqrt(I ** 2 + J ** 2);
		
		theta_start = self.Vector2theta(Vect_x_start, Vect_y_start);
		theta_end = self.Vector2theta(Vect_x_end, Vect_y_end);
		D_theta = theta_end - theta_start;
		if D_theta < 0:
			D_theta = D_theta + 2.0 * np.pi;
		if D_theta == 0:
			D_theta = 2.0 * np.pi;
		d_theta = D_theta / self.Resolution;
		
		for i in range(1, int(self.Resolution) + 1):
			self.X_track.append(self.Theta2point(theta_start + d_theta * i, R, Cx, Cy)[0]);
			self.Y_track.append(self.Theta2point(theta_start + d_theta * i, R, Cx, Cy)[1]);
			
	def Bezier_Quad(self):
		XX = self.Line[self.Line.find(" X,") + 4: self.Line.find(", Y,")];
		YY = self.Line[self.Line.find(" Y,") + 4:];
		X = [];
		Y = [];
		for i in range(0, 3):
			X.append(float(XX.split(', ')[i]));
			Y.append(float(YY.split(', ')[i]));
			
		for i in range(0, int(self.Resolution) + 1):
			t = float(i) / float(self.Resolution);
			self.X_track.append((1 - t)**2 * X[0] + 2 * (1 - t) * t * X[1] + t**2 * X[2]);
			self.Y_track.append((1 - t)**2 * Y[0] + 2 * (1 - t) * t * Y[1] + t**2 * Y[2]);
			
	def Bezier_Cubic(self):
		XX = self.Line[self.Line.find(" X,") + 4: self.Line.find(", Y,")];
		YY = self.Line[self.Line.find(" Y,") + 4: self.Line.find(" TOLERANCE")];
		X = [];
		Y = [];
		for i in range(0, 4):
			X.append(float(XX.split(', ')[i]));
			Y.append(float(YY.split(', ')[i]));
			
		for i in range(0, int(self.Resolution) + 1):
			t = float(i) / float(self.Resolution);
			self.X_track.append((1 - t)**3 * X[0] + 3 * (1 - t)**2 * t * X[1] + 3 * (1 - t) * t**2 * X[2] + t**3 * X[3]);
			self.Y_track.append((1 - t)**3 * Y[0] + 3 * (1 - t)**2 * t * Y[1] + 3 * (1 - t) * t**2 * Y[2] + t**3 * Y[3]);

