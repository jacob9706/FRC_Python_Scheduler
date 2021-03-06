
# directory that robot.py is located, relative to this file
robot_path = '../Framework'

import _wpilib, time

class Test(object):

    def __init__(self, robot_module, myrobot):
        self.robot_module = robot_module
        self.myrobot = myrobot
        self.Reset()
        
    def Reset(self):
        self.loop_count = 0
        self.tm = None
        self.tm2 = None
        
    def IsAutonomous(self, tm):
        return False
        
    def IsOperatorControl(self, tm):
        '''Continue operator control for 1000 control loops'''
        if self.tm2 is None:
            self.tm2 = time.time()
        return time.time() - self.tm2 < (2*60)
        


def run_tests( robot_module, myrobot ):

    test = Test( robot_module, myrobot )

    _wpilib.internal.print_components()
    
    _wpilib.internal.on_IsAutonomous = test.IsAutonomous
    _wpilib.internal.on_IsOperatorControl = test.IsOperatorControl
    
    
    _wpilib.internal.enabled = True
    
    test.Reset()
    myrobot.Autonomous()
    
    test.Reset()
    myrobot.OperatorControl()


