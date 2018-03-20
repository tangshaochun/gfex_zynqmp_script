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

##I2C BUS3 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA C
#MPOD_U34_ADDR  = 0x28 #0101_000X      0X50
#MPOD_U42_ADDR  = 0x29 #0101_001X      0X52
#MPOD_U114_ADDR = 0x30 #0110_000X        0X60
#MPOD_U115_ADDR = 0x31 #0110_001X        0X62
#MPOD_U116_ADDR = 0x32 #0110_010X        0X64
#MPOD_U117_ADDR = 0x33 #0110_011X        0X66
#MPOD_U118_ADDR = 0x34 #0110_100X        0X68
#MPOD_U119_ADDR = 0x35 #0110_101X        0X6A
#MPOD_U120_ADDR = 0x36 #0110_110X        0X6C
#MPOD_U90_ADDR  = 0x37 #0110_111X      0X6E
#
##I2C BUS4 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA B
#MPOD_U33_ADDR  = 0x28 #0101_000X       0X50
#MPOD_U27_ADDR  = 0x29 #0101_001X       0X52
#MPOD_U98_ADDR  = 0x30 #0110_000X       0X60
#MPOD_U100_ADDR = 0x31 #0110_001X       0X62
#MPOD_U101_ADDR = 0x32 #0110_010X       0X64
#MPOD_U108_ADDR = 0x33 #0110_011X       0X66
#MPOD_U109_ADDR = 0x34 #0110_100X       0X68
#MPOD_U111_ADDR = 0x35 #0110_101X       0X6A
#MPOD_U112_ADDR = 0x36 #0110_110X       0X6C
#MPOD_U113_ADDR = 0x37 #0110_111X       0X6E
#
#
##I2C BUS5 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA A
#MPOD_U32_ADDR  = 0x28 #0101_000X      0X50
#MPOD_U25_ADDR  = 0x29 #0101_001X      0X52
#MPOD_U96_ADDR  = 0x30 #0110_000X      0X60
#MPOD_U102_ADDR = 0x31 #0110_001X        0X62
#MPOD_U103_ADDR = 0x32 #0110_010X        0X64
#MPOD_U104_ADDR = 0x33 #0110_011X        0X66
#MPOD_U105_ADDR = 0x34 #0110_100X        0X68
#MPOD_U106_ADDR = 0x35 #0110_101X        0X6A
#MPOD_U107_ADDR = 0x36 #0110_110X        0X6C
#MPOD_U97_ADDR  = 0x37 #0110_111X      0X6E

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
  #print('read done')
  return reg_value

def minipod_mon(i2c_bus_addr,dev_addr):
  temperature=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,28) #temperature

  vh=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,32) #3.3V monitoring VH
  vl=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,33) #3.3V monitoring VL
  voltage1=(int(vh,16)*256+int(vl,16))*0.0001
  vh=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,34) #2.5V monitoring VH
  vl=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,35) #2.5V monitoring VL
  voltage2=(int(vh,16)*256+int(vl,16))*0.0001

  los_h=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,9); #LOS channel 8-11
  los_l=minipod_reg_rd(i2c_bus_addr,dev_addr,0x00,10); #LOS channel 0-7
  los=int(los_h,16)*256+int(los_l,16)
  return int(temperature,16),voltage1,voltage2,los
 
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

#print('----------------MiniPODs connected to processor FPGA A-----------------------')
#print('Refdes    Type    Temperature(C)    3.3V Power(V)    2.5V Power(V)  LOS[11:0]')
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U32_ADDR)
#print("U32       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U25_ADDR)
#print("U25       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U96_ADDR)
#print("U96       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U102_ADDR)
#print("U102      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U103_ADDR)
#print("U103      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U104_ADDR)
#print("U104      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U105_ADDR)
#print("U105      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U106_ADDR)
#print("U106      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U107_ADDR)
#print("U107      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS5,MPOD_U97_ADDR)
#print("U97       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U91_ADDR)
#print("U91/S     RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#
#print('----------------MiniPODs connected to processor FPGA B-----------------------')
#print('Refdes    Type    Temperature(C)    3.3V Power(V)    2.5V Power(V)  LOS[11:0]')
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U33_ADDR)
#print("U33       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U27_ADDR)
#print("U27       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U98_ADDR)
#print("U98       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U100_ADDR)
#print("U100      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U101_ADDR)
#print("U101      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U108_ADDR)
#print("U108      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U109_ADDR)
#print("U109      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U111_ADDR)
#print("U111      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U112_ADDR)
#print("U112      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS4,MPOD_U113_ADDR)
#print("U113      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U91_ADDR)
#print("U91/S     RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#
#print('----------------MiniPODs connected to processor FPGA C-----------------------')
#print('Refdes    Type    Temperature(C)    3.3V Power(V)    2.5V Power(V)  LOS[11:0]')
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U34_ADDR)
#print("U34       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U42_ADDR)
#print("U42       TX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U114_ADDR)
#print("U114      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U115_ADDR)
#print("U115      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U116_ADDR)
#print("U116      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U117_ADDR)
#print("U117      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U118_ADDR)
#print("U118      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U119_ADDR)
#print("U119      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U120_ADDR)
#print("U120      RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS3,MPOD_U90_ADDR)
#print("U90       RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
#temperature,voltage1,voltage2,los=minipod_mon(Z_IIC_BUS2,MPOD_U91_ADDR)
#print("U91/S     RX      {0:d}                {1:.3f}            {2:.3f}          0x{3:X}".format(temperature,voltage1,voltage2,los))
