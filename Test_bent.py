from Motion_Modules.Basic.Basic_Motion import *
from Motion_Modules.Basic.Code_Visualization import *
from Motion_Modules.Motion_Modules import *
from math import *

class Test_bent(Motion_Modules):
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
    Dir_bent = 0 # 0 for up, 1 for down
    Tail_extension = 0.5
    
    
    def __init__(self, directory):        
        self.file_create(directory, 'test')
        self.bent(0)
        self.bent(1)
        self.FILE.close()
        
    def bent(self, Cr_or_LN):
        end_point = Point(0.0, 0.0)        
        end_point.change(0.0, 0.1) # two parameters is OK too
        self.g_spot(end_point)
        self.shutter(1)
        self.Dir_bent = 0
        self.Bent_Waveguide(Cr_or_LN)
        
        end_point.change(0.0, -0.1) # two parameters is OK too
        self.g_spot(end_point)
        self.shutter(1)
        self.Dir_bent = 1
        self.Bent_Waveguide(Cr_or_LN)


        
        
directory = os.path.splitext(os.path.basename(__file__))[0]
print('Writing')
Test_bent(directory)

(x_min, x_max) = (0, 20)
(y_min, y_max) = (-0.2, 0.2)
key = 0
Code_Visualization(directory, 'test', x_min, x_max, y_min, y_max, key)

