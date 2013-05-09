try:
    import wpilib
except ImportError:
    import sys
    sys.path.append('../fake-wpilib/lib/')
    import fake_wpilib as wpilib

    import _wpilib
    _wpilib.internal.enabled = True
    def start_auto(tm):
        #print(tm)
        return tm > 2 and tm < 17
    _wpilib.internal.on_IsAutonomous = start_auto

    def start_tele(tm):
        #print(tm)
        return tm > 17 and tm < 30
    _wpilib.internal.on_IsOperatorControl = start_tele