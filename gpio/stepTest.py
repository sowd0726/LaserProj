import time
import StepMotor
import sys
import threading

if __name__ == '__main__':
    args = sys.argv
    StepMotorY = StepMotor.C28BYJ48(IN1=0 ,IN2=1, IN3=2, IN4=3)
    StepMotorX = StepMotor.C28BYJ48(IN1=4, IN2=5, IN3=6, IN4=7)
    #Main loop
    StepMotorX.ThreadStep( int(args[1]),0.0010)
    StepMotorY.ThreadStep( int(args[2]),0.0010)
    #StepMoterY.Step(int(args[2]),0.0005)

    StepMotorX.Cleanup()
    StepMotorY.Cleanup()
    print("\nexit program")
