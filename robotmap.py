from get_wpilib import wpilib
from utilities.smooth_encoder import SmoothEncoder

################### Create objects here ###################

# Joysticks
joystick1 = wpilib.Joystick(1)
joystick2 = wpilib.Joystick(2)


# Drive System
frontLeftMotor = wpilib.Jaguar(3)
rearLeftMotor = wpilib.Jaguar(4)
frontRightMotor = wpilib.Jaguar(1)
rearRightMotor = wpilib.Jaguar(2)
shifters = wpilib.Solenoid(7)

robotDrive = wpilib.RobotDrive(frontLeftMotor, rearLeftMotor, frontRightMotor, rearRightMotor)


# Colector System
upperCollectorMotor = wpilib.Talon(7)
lowerCollectorMotor = wpilib.Talon(8)


# Tilt System
tiltMotor = wpilib.Talon(6)

tiltZeroSwitch = wpilib.DigitalInput(1);
tiltSeventySwitch = wpilib.DigitalInput(3);

tiltEncoder = wpilib.Encoder(5, 6)

# Shooter System
shooterMotor = wpilib.Talon(5)

shooterEncoder = SmoothEncoder(7, 8, True)
shooterEncoder.pid_mode = wpilib.Encoder.kRate
