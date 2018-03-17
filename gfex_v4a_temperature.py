#!/usr/bin/env python
from __future__ import print_function
from i2cdev import I2C
from math import trunc
from time import sleep
import sys

#I2C PS BUS1 MUX TCA9548 ADDRESS Definitions
SENSOR_IIC_BUS = 0x01 # Sensor I2c bus on gFEX board
Z_IIC_BUS2 = 0x02
Z_IIC_BUS3 = 0x04
Z_IIC_BUS4 = 0x08
Z_IIC_BUS5 = 0x10

#I2C MUX TCA9548 ADDRESS Definitions
TCA9548_U93_ADDR = 0x70 #1110_000X      0XE0

#SENSOR I2C BUS COMPONENTS ADDRESS Definitions
INA226_U81_ADDR  = 0x40 #1000_000X      0X80
BMR4582_U11_ADDR = 0x7F #1111_111X      0XFE
ADM1066_U52_ADDR = 0x34 #0110_100X      0X68
ADM1066_U51_ADDR = 0x35 #0110_101X      0X6A
LTC2499_U2_ADDR  = 0x15 #0010_101X      0X2A
LTC2499_U1_ADDR  = 0x14 #0010_100X      0X28
AD7414_U82_ADDR  = 0x49 #1001_001X      0X92
AD7414_U83_ADDR  = 0x4A #1001_010X      0X94
AD7414_U84_ADDR  = 0x48 #1001_000X      0X90
AD7414_U87_ADDR  = 0x4D #1001_101X      0X9A

#I2C BUS2 COMPONENTS ADDRESS Definitions MiniPODs for Processor FPGA Z
MPOD_U3_ADDR    = 0x28 #0101_000X       0X50
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

#PS I2C BUS0 CONFIGURATION ADDRESS Definitions
SI5345_U137_ADDR = 0x68 #1101_000X      0XD0
def set_i2c_mux(dev_addr,channel):
  i2c = I2C(dev_addr, 1) # device @ 0x70, bus 1
  i2c.write(bytearray([channel]))# set channel
  i2c.close()

def ad7414_reg_write(dev_addr,reg_addr,reg_value):
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([reg_addr,reg_value]))# SENSOR_IIC_BUS is selected
  i2c.close()
def ad7414_reg_read(dev_addr,reg_addr,nbits):
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([reg_addr]))# Reg for read
  reg_value=i2c.read(nbits)# Read N bits.
  i2c.close()
  return reg_value
def ad7414_mon(dev_addr):
  ad7414_reg_write(dev_addr,0x1,0x48) #alert active low
  ad7414_reg_write(dev_addr,0x2,0x3F) #up limit is 63 Degree   
  ad7414_reg_write(dev_addr,0x3,0x80) #low limit is 0 degree
  temperature=ad7414_reg_read(dev_addr,0x0,1)#read the temperature value
  return int(temperature,16)

def ltc2499_temp_mon(dev_addr,reg_addr0,reg_addr1):
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([reg_addr1,reg_addr0]))# Reg for read
  sleep(0.5)
  adc_code=i2c.read(4)# Read 4 bits.
  i2c.close()
  sleep(0.5)
  resolution=2500./0x80000000
  if(int(adc_code,16)==0x3FFFFFFF):
    amplitude=-1
  else:
    amplitude=(int(adc_code,16)-0x40000000)*resolution
  temperature= 326-0.5*amplitude
  return temperature 
#convert a LinearFloat5_11 formatted word into a floating point value
def lin5_11ToFloat(wordValue):
  binValue = int(wordValue,16)
  #binValue=binValue>>8 | (binValue << 8 & 0xFF00)
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

  value = list(read)
  value = value[1]*256 + value[0]
  #print('BMR458 value  is {0:d}' .format(value))
  return '{0:x}'.format(value)
 
# Board Temperature monitoring
print('----------Temperature monitoring of gFEX production board-----------------')
print('REFDES    Device      Temperature(C)    Description')
#set the I2C Mux to SENSOR_IIC_BUS 0x01
set_i2c_mux(TCA9548_U93_ADDR,SENSOR_IIC_BUS)
# Read board temperature sensors AD7414
temperature=ad7414_mon(AD7414_U82_ADDR)
print('U82       AD7414      {0:d}                Upright of the board' .format(temperature))
temperature=ad7414_mon(AD7414_U83_ADDR)
print('U83       AD7414      {0:d}                Down left of the board' .format(temperature))
temperature=ad7414_mon(AD7414_U84_ADDR)
print('U84       AD7414      {0:d}                Up left of the board' .format(temperature))
temperature=ad7414_mon(AD7414_U87_ADDR)
print('U87       AD7414      {0:d}                Down right of the board' .format(temperature))

# LTM4630A power modules Temperature monitoring
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB0)
#print('U122      LTM4630A    {0:d}                Power module of INT_A_0.85V' .format(trunc(temperature)))
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB8)
#print('U77       LTM4630A    {0:d}                Power module of MGTAVCC_A_0.9V' .format(trunc(temperature)))
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB1)
#print('U30       LTM4630A    {0:d}                Power module of MGTAVTT_A_1.2V' .format(trunc(temperature)))
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB9)
#print('U123      LTM4630A    {0:d}                Power module of INT_B_0.85V' .format(trunc(temperature))) 
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB2)
#print('U124      LTM4630A    {0:d}                Power module of MGTAVCC_B_0.9V' .format(trunc(temperature)))
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBA)
#print('U40       LTM4630A    {0:d}                Power module of MGTAVTT_B_1.2V' .format(trunc(temperature)))
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB3)
#print('U126      LTM4630A    {0:d}                Power module of INT_C_0.85V' .format(trunc(temperature))) 
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBB)
#print('U125      LTM4630A    {0:d}                Power module of MGTAVCC_C_0.9V' .format(trunc(temperature)))
#temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB4)
#print('U44       LTM4630A    {0:d}                Power module of MGTAVTT_C_1.2V' .format(trunc(temperature)))
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBC)
print('U66       LTM4630A    {0:d}                DDR4_VDDQ_1.2V/MGTAVTT_Z_1.2V' .format(trunc(temperature))) 
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB5)
print('U73       LTM4650A    {0:d}                Power module of INT_Z_0.85V' .format(trunc(temperature)))
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBD)
print('U55       LTM4630A    {0:d}                Power module of 2.5V' .format(trunc(temperature)))
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB6)
print('U59       LTM4630A    {0:d}                MGTAVCC_Z_0.9V/3.3V' .format(trunc(temperature)))

#12V power module BMR458 temperature
reg_value=bmr458_mon(BMR4582_U11_ADDR,0x8D)
temperature=lin5_11ToFloat(reg_value)
print('U11       BMR458      {0:d}                12V DC/DC Converter' .format(trunc(temperature)))
