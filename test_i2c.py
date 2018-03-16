#!/usr/bin/env python
from i2cdev import I2C
i2c = I2C(0x68, 0) # device @ 0x68, bus 0
i2c.write(bytearray(0x0003)) # register for base part number
value = i2c.read(2)
print value == '4553'
