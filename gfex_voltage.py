#!/usr/bin/env python
from __future__ import print_function
from i2cdev import I2C
from math import trunc
from time import sleep
import sys

from constants import *

#convert a LinearFloat5_11 formatted word into a floating point value
def lin5_11ToFloat(wordValue):
  binValue = int(wordValue,16)
  #binValue=binValue>>8 | (binValue << 8 & 0xFF00)
  #print('{0:s}' binValue)

  #wordValue = ' '.join(format(x, 'b') for x in bytearray(wordValue))
  exponent = binValue>>11      #extract exponent as MS 5 bits
  mantissa = binValue & 0x7ff  #extract mantissa as LS 11 bits

  #sign extended exponent
  if exponent > 0x0F: exponent |= 0xE0
  if exponent > 127: exponent -= 2**8
  #sign extended mantissa
  if mantissa > 0x03FF: mantissa |= 0xF800
  if mantissa > 32768: mantissa -= 2**16
  # compute value as
  return mantissa * (2**exponent)

from smbus import SMBusWrapper, i2c_msg
def bmr458_mon(dev_addr,reg_addr):
  with SMBusWrapper(1) as bus:
    write = i2c_msg.write(dev_addr, [reg_addr])
    read = i2c_msg.read(dev_addr, 2)
    bus.i2c_rdwr(write, read)
    sleep(1)
  value = list(read)
  #print("[{0}]".format(', '.join(map(str, value))))
  value = value[1]*256 + value[0]
  #print('BMR458 value  is {0:d}' .format(value))
  return '{0:x}'.format(value)
#set the i2c mux channel
i2c = I2C(TCA9548_U93_ADDR, 1) # device @ 0x70, bus 1
i2c.write(bytearray([SENSOR_IIC_BUS]))# SENSOR_IIC_BUS is selected
i2c.close()
#12V power module BMR458 Voltage
reg_value=bmr458_mon(BMR4582_U11_ADDR,0x88)
voltage=lin5_11ToFloat(reg_value)
print('BMR458 DC/DC input voltage is {0:.2f} V' .format(voltage))

reg_value=bmr458_mon(BMR4582_U11_ADDR,0x8B)
voltage=2**(-11)*int(reg_value,16)
print('BMR458 DC/DC output voltage is {0:.2f} V' .format(voltage))

reg_value=bmr458_mon(BMR4582_U11_ADDR,0x8C)
current=lin5_11ToFloat(reg_value)
print('BMR458 DC/DC output current is {0:.2f} A' .format(current))
print('gFEX board current power consumpution is {0:.2f} W'.format(voltage*current))


