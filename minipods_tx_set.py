#!/usr/bin/env python
from __future__ import print_function
from i2cdev import I2C
from math import trunc
from time import sleep
import sys

from constants import *

def minipod_reg_wr(i2c_bus_addr,dev_addr,page_addr,reg_addr,reg_value):
  i2c = I2C(TCA9548_U93_ADDR, 1) # device @ 0x70, bus 1
  i2c.write(bytearray([i2c_bus_addr]))# select I2C Bus
  i2c.close()
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([127,page_addr]))# set the page
  i2c.write(bytearray([reg_addr,reg_value]))#write the value to the reg_addr
  #print('write done')
  i2c.close()

def minipod_reg_rd(i2c_bus_addr,dev_addr,page_addr,reg_addr):
  i2c = I2C(TCA9548_U93_ADDR, 1) # device @ 0x70, bus 1
  i2c.write(bytearray([i2c_bus_addr]))# select I2C Bus
  i2c.close()
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([127,page_addr]))# set the page
  i2c.write(bytearray([reg_addr]))#set reg_addr
  reg_value=i2c.read(1)# Read N bits.
  i2c.close()
  print('read back is 0x{0:x}' .format(int(reg_value,16)))
  return reg_value
def minpod_check (i2c_bus_addr,dev_addr):
  for i in range(228, 234):
    minipod_reg_rd(i2c_bus_addr,dev_addr,0x01,i)
def minipod_set(i2c_bus_addr, dev_addr,reg_value):
  for i in range(228,234):
    minipod_reg_wr(i2c_bus_addr,dev_addr,0x01,i,reg_value)

minipod_set(Z_IIC_BUS2,MPOD_U3_ADDR,0x33)
minipod_set(Z_IIC_BUS2,MPOD_U24_ADDR,0x33)
minipod_set(Z_IIC_BUS2,MPOD_U56_ADDR,0x33)
minipod_set(Z_IIC_BUS3,MPOD_U34_ADDR,0x33)
minipod_set(Z_IIC_BUS3,MPOD_U42_ADDR,0x33)
minipod_set(Z_IIC_BUS4,MPOD_U33_ADDR,0x33)
minipod_set(Z_IIC_BUS4,MPOD_U27_ADDR,0x33)
minipod_set(Z_IIC_BUS5,MPOD_U32_ADDR,0x33)
minipod_set(Z_IIC_BUS5,MPOD_U25_ADDR,0x33)

# MiniPODs monitoring
print('---------MiniPOD TX U3------')
minpod_check(Z_IIC_BUS2,MPOD_U3_ADDR)
print('---------MiniPOD TX U24------')
minpod_check(Z_IIC_BUS2,MPOD_U24_ADDR)
print('---------MiniPOD TX U56------')
minpod_check(Z_IIC_BUS2,MPOD_U56_ADDR)
print('---------MiniPOD TX U34------')
minpod_check(Z_IIC_BUS3,MPOD_U34_ADDR)
print('---------MiniPOD TX U42------')
minpod_check(Z_IIC_BUS3,MPOD_U42_ADDR)
print('---------MiniPOD TX U33------')
minpod_check(Z_IIC_BUS4,MPOD_U33_ADDR)
print('---------MiniPOD TX U27------')
minpod_check(Z_IIC_BUS4,MPOD_U27_ADDR)
print('---------MiniPOD TX U34------')
minpod_check(Z_IIC_BUS5,MPOD_U32_ADDR)
print('---------MiniPOD TX U34------')
minpod_check(Z_IIC_BUS5,MPOD_U25_ADDR)

