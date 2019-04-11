from Motion_Modules.Basic.Basic_Motion import *
from Motion_Modules.Basic.Code_Visualization import *
from Motion_Modules.Motion_Modules import *
from math import *

class Test_rect(Motion_Modules):
	def __init__(self, directory):
		self.file_create(directory, 'test')
		self.test()
		self.FILE.close()

	def test(self):
		L = 1.0
		H = 0.1
		end_point = Point(0.0, 0.0, 0.0)
		self.g_spot(end_point)
		self.Rectangle(L, H)
		L = 0.2
		H = 0.3
		end_point.change(0.0, 0.2)
		self.g_spot(end_point)
		self.Rectangle(L, H)
		L, H = 0.2, 0.2
		end_point.change(0.4, 0.2)
		self.g_spot(end_point)
		self.Rectangle(L, H)
		
directory = os.path.splitext(os.path.basename(__file__))[0]
print('Writing')
Test_rect(directory)

(x_min, x_max) = (0, 20)
(y_min, y_max) = (-0.2, 0.2)
key = 0
Code_Visualization(directory, 'test', x_min, x_max, y_min, y_max, key)

