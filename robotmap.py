from get_wpilib import wpilib

################### Register objects here ###################

# Create Joysticks
joystick1 = wpilib.Joystick(1)
joystick2 = wpilib.Joystick(2)

# Create Motors
frontLeftMotor = wpilib.Jaguar(3)
rearLeftMotor = wpilib.Jaguar(4)
frontRightMotor = wpilib.Jaguar(1)
rearRightMotor = wpilib.Jaguar(2)

robotDrive = wpilib.RobotDrive(frontLeftMotor, rearLeftMotor, frontRightMotor, rearRightMotor)

# Create Solenoid
shifters = wpilib.Solenoid(1)