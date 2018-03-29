#!/usr/bin/env python
from periphery import I2C
i2c = I2C("/dev/i2c-0")

read = I2C.Message([0x0]*2, read=True)
i2c.transfer(0x68, [I2C.Message([0x0003]), read])
i2c.close()

print bytes(bytearray(data.read)).encode('hex') == '4553'
