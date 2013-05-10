
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
        '''Run a full 15 seconds of autonomous mode, then exit'''
        if self.tm is None:
            self.tm = time.time()
        return time.time() - self.tm < 15
        
    def IsOperatorControl(self, tm):
        if self.loop_count < 1:
            self.loop_count += 1
            return True
        return False
        


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


