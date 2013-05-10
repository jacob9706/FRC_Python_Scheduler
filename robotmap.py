from get_wpilib import wpilib

################### Register objects here ###################

# Create Joysticks
joystick1 = wpilib.Joystick(1)

# Create Motors
leftDriveMotor = wpilib.Jaguar(1)
rightDriveMotor = wpilib.Jaguar(2)