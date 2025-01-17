# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:18:12 2024

@author: public
"""
import time
import serial
import motorized_control_function as mcf

mcf.read_position("x")
mcf.read_position("y")
mcf.read_position("z")

mcf.motor_control("x",4,-10000)
#mcf.motor_control("y",4,-10000)
mcf.motor_control("z",4,-10000)

mcf.read_position("x")
mcf.read_position("y")
mcf.read_position("z")


mcf.initialize_all()
mcf.quit_motor()
'''start = time.time()
for i in range(10):
    for j in range(10):
        mcf.motor_control("x",4,-4000*j+20000) #2.5um step
        time.sleep(0.1)
    mcf.motor_control("z",4,-4000*i+20000)
    time.sleep(0.1)
end = time.time()
print(end-start)'''
