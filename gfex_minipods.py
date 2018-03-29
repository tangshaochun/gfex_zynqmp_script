#!/usr/bin/env python
from __future__ import print_function
from i2cdev import I2C
from math import trunc
from time import sleep
import sys

from periphery import I2C
from constants import *
from configurations import board

def minipod_reg_wr(i2c_bus_addr,dev_addr,page_addr,reg_addr,reg_value):
  i2c = I2C("/dev/i2c-1")
  i2c.transfer(TCA9548_U93_ADDR, [I2C.Message([i2c_bus_addr])]) # select i2c bus

  i2c.transfer(dev_addr, [I2C.Message([127,page_addr])])    # set the page
  i2c.transfer(dev_addr, [I2C.Message([reg_addr,reg_value])]) # write the value to the reg_addr
  i2c.close()

def minipod_reg_rd(i2c_bus_addr,dev_addr,page_addr,reg_addr):
  i2c = I2C("/dev/i2c-1")
  i2c.transfer(TCA9548_U93_ADDR, [I2C.Message([i2c_bus_addr])]) # select i2c bus

  read = I2C.Message([0x0])
  i2c.transfer(dev_addr, [I2C.Message([127,page_addr])]) # set the page
  i2c.transfer(dev_addr, [I2C.Message([reg_addr])])      # set reg_addr
  i2c.transfer(dev_addr, [read])

  i2c.close()

  return read.data[0]

def minipod_mon(i2c_bus_addr,dev_addr):
  temperature=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,28) #temperature

  vh=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,32) #3.3V monitoring VH
  vl=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,33) #3.3V monitoring VL
  voltage1 = (vh*256 + vl)*0.0001
  vh=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,34) #2.5V monitoring VH
  vl=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,35) #2.5V monitoring VL
  voltage2 = (vh*256 + vl)*0.0001

  los_h=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,9); #LOS channel 8-11
  los_l=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,10); #LOS channel 0-7
  los = los_h*256 + los_l
  return temperature,voltage1,voltage2,los

# MiniPODs monitoring
print('----------------MiniPODs connected to ZYNQ Ultrascale+-----------------------')
print('Refdes    Type    Temperature(C)    3.3V Power(V)    2.5V Power(V)  LOS[11:0]')
temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U3_ADDR)
print("U3        TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U24_ADDR)
print("U24       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U56_ADDR)
print("U56       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U72_ADDR)
print("U72       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))

if board == 'v4b':
  print('----------------MiniPODs connected to processor FPGA A-----------------------')
  print('Refdes    Type    Temperature(C)    3.3V Power(V)    2.5V Power(V)  LOS[11:0]')
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U32_ADDR)
  print("U32       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U25_ADDR)
  print("U25       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U96_ADDR)
  print("U96       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U102_ADDR)
  print("U102      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U103_ADDR)
  print("U103      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U104_ADDR)
  print("U104      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U105_ADDR)
  print("U105      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U106_ADDR)
  print("U106      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U107_ADDR)
  print("U107      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U97_ADDR)
  print("U97       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U91_ADDR)
  print("U91/S     RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))

  print('----------------MiniPODs connected to processor FPGA B-----------------------')
  print('Refdes    Type    Temperature(C)    3.3V Power(V)    2.5V Power(V)  LOS[11:0]')
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U33_ADDR)
  print("U33       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U27_ADDR)
  print("U27       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U98_ADDR)
  print("U98       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U100_ADDR)
  print("U100      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U101_ADDR)
  print("U101      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U108_ADDR)
  print("U108      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U109_ADDR)
  print("U109      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U111_ADDR)
  print("U111      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U112_ADDR)
  print("U112      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U113_ADDR)
  print("U113      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U91_ADDR)
  print("U91/S     RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))

  print('----------------MiniPODs connected to processor FPGA C-----------------------')
  print('Refdes    Type    Temperature(C)    3.3V Power(V)    2.5V Power(V)  LOS[11:0]')
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U34_ADDR)
  print("U34       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U42_ADDR)
  print("U42       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U114_ADDR)
  print("U114      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U115_ADDR)
  print("U115      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U116_ADDR)
  print("U116      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U117_ADDR)
  print("U117      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U118_ADDR)
  print("U118      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U119_ADDR)
  print("U119      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U120_ADDR)
  print("U120      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U90_ADDR)
  print("U90       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
  temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U91_ADDR)
  print("U91/S     RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
