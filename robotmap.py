from get_wpilib import wpilib

################### Register objects here ###################

# Create Joysticks
joystick1 = wpilib.Joystick(1)
joystick2 = wpilib.Joystick(2)

# Create Motors
leftDriveMotor = wpilib.Victor(1)
rightDriveMotor = wpilib.Victor(2)