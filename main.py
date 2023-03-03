#!/usr/bin/python

import time
from lib.MotorDriver import MotorDriver


print("this is a motor driver test code")
motor = MotorDriver()

print("forward 2 s")
motor.run(0, 'forward', 100)
motor.run(1, 'forward', 100)
time.sleep(2)

print("backward 2 s")
motor.run(0, 'backward', 100)
motor.run(1, 'backward', 100)
time.sleep(2)

print("stop")
motor.stop(0)
motor.stop(1)