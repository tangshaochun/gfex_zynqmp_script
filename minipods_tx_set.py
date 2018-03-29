#!/usr/bin/env python
from __future__ import print_function

from periphery import I2C
from constants import *
from configurations import board

def minipod_reg_wr(i2c_bus_addr,dev_addr,page_addr,reg_addr,reg_value):
  i2c = I2C("/dev/i2c-1")
  i2c.transfer(TCA9548_U93_ADDR, [I2C.Message([i2c_bus_addr])]) # select i2c bus
  i2c.transfer(dev_addr, [I2C.Message([127,page_addr])])        # set the page
  i2c.transfer(dev_addr, [I2C.Message([reg_addr,reg_value])])   # write the value to the reg_addr
  i2c.close()

def minipod_reg_rd(i2c_bus_addr,dev_addr,page_addr,reg_addr):
  i2c = I2C("/dev/i2c-1")
  i2c.transfer(TCA9548_U93_ADDR, [I2C.Message([i2c_bus_addr])]) # select i2c bus

  read = I2C.Message([0x0], read=True)
  i2c.transfer(dev_addr, [I2C.Message([127,page_addr])]) # set the page
  i2c.transfer(dev_addr, [I2C.Message([reg_addr])])      # set reg_addr
  i2c.transfer(dev_addr, [read])
  i2c.close()

  print('read back is 0x{0:x}' .format(read.data[0]))
  return read.data[0]


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
