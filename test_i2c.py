#!/usr/bin/env python
from periphery import I2C

from constants import *

i2c = I2C("/dev/i2c-0")

read = I2C.Message([0x2]*2, read=True)
i2c.transfer(SI5345_U137_ADDR, [I2C.Message([0x01, 0x0])])
i2c.transfer(SI5345_U137_ADDR, [I2C.Message([0x02])])
i2c.transfer(SI5345_U137_ADDR, [read])
i2c.close()

print bytes(bytearray(read.data)).encode('hex') == '4553'
