#!/usr/bin/env python
from __future__ import print_function
from i2cdev import I2C
from math import trunc
from time import sleep
import sys

#I2C PS BUS1 MUX TCA9548 ADDRESS Definitions
Z_IIC_BUS2 = 0x02
Z_IIC_BUS3 = 0x04
Z_IIC_BUS4 = 0x08
Z_IIC_BUS5 = 0x10

#I2C MUX TCA9548 ADDRESS Definitions
TCA9548_U93_ADDR = 0x70 #1110_000X      0XE0
#I2C BUS2 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA Z
MPOD_U3_ADDR  = 0x28 #0101_000X       0X50
MPOD_U24_ADDR = 0x29 #0101_001X 0X52
MPOD_U56_ADDR = 0x2A #0101_010X 0X54
MPOD_U72_ADDR = 0x30 #0110_000X 0X60
MPOD_U91_ADDR = 0x31 #0110_001X 0X62

#I2C BUS3 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA C
MPOD_U34_ADDR  = 0x28 #0101_000X      0X50
MPOD_U42_ADDR  = 0x29 #0101_001X      0X52
MPOD_U114_ADDR = 0x30 #0110_000X        0X60
MPOD_U115_ADDR = 0x31 #0110_001X        0X62
MPOD_U116_ADDR = 0x32 #0110_010X        0X64
MPOD_U117_ADDR = 0x33 #0110_011X        0X66
MPOD_U118_ADDR = 0x34 #0110_100X        0X68
MPOD_U119_ADDR = 0x35 #0110_101X        0X6A
MPOD_U120_ADDR = 0x36 #0110_110X        0X6C
MPOD_U90_ADDR  = 0x37 #0110_111X      0X6E

#I2C BUS4 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA B
MPOD_U33_ADDR  = 0x28 #0101_000X       0X50
MPOD_U27_ADDR  = 0x29 #0101_001X       0X52
MPOD_U98_ADDR  = 0x30 #0110_000X       0X60
MPOD_U100_ADDR = 0x31 #0110_001X       0X62
MPOD_U101_ADDR = 0x32 #0110_010X       0X64
MPOD_U108_ADDR = 0x33 #0110_011X       0X66
MPOD_U109_ADDR = 0x34 #0110_100X       0X68
MPOD_U111_ADDR = 0x35 #0110_101X       0X6A
MPOD_U112_ADDR = 0x36 #0110_110X       0X6C
MPOD_U113_ADDR = 0x37 #0110_111X       0X6E


#I2C BUS5 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA A
MPOD_U32_ADDR  = 0x28 #0101_000X      0X50
MPOD_U25_ADDR  = 0x29 #0101_001X      0X52
MPOD_U96_ADDR  = 0x30 #0110_000X      0X60
MPOD_U102_ADDR = 0x31 #0110_001X        0X62
MPOD_U103_ADDR = 0x32 #0110_010X        0X64
MPOD_U104_ADDR = 0x33 #0110_011X        0X66
MPOD_U105_ADDR = 0x34 #0110_100X        0X68
MPOD_U106_ADDR = 0x35 #0110_101X        0X6A
MPOD_U107_ADDR = 0x36 #0110_110X        0X6C
MPOD_U97_ADDR  = 0x37 #0110_111X      0X6E

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

