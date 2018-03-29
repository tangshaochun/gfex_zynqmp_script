#!/usr/bin/env python
from __future__ import print_function
from math import trunc
from time import sleep
import sys

from periphery import I2C
from constants import *
from configurations import board

def set_i2c_mux(dev_addr,channel):
  i2c = I2C("/dev/i2c-1")
  i2c.transfer(dev_addr, [I2C.Message([channel])])
  i2c.close()

def ad7414_reg_write(dev_addr,reg_addr,reg_value):
  i2c = I2C("/dev/i2c-1")
  i2c.transfer(dev_addr, [I2C.Message([reg_addr, reg_value])]) # SENSOR_IIC_BUS is selected
  i2c.close()

def ad7414_reg_read(dev_addr,reg_addr,nbits):
  i2c = I2C("/dev/i2c-1")
  read = I2C.Message([0x0]*nbits, read=True)
  i2c.transfer(dev_addr, [I2C.Message([reg_addr]), read]) # reg for read
  i2c.close()
  return bytes(bytearray(read.data)).encode('hex')

def ad7414_mon(dev_addr):
  ad7414_reg_write(dev_addr,0x1,0x48) #alert active low
  ad7414_reg_write(dev_addr,0x2,0x3F) #up limit is 63 Degree
  ad7414_reg_write(dev_addr,0x3,0x80) #low limit is 0 degree
  temperature=ad7414_reg_read(dev_addr,0x0,1)#read the temperature value
  return int(temperature,16)

def ltc2499_temp_mon(dev_addr,reg_addr0,reg_addr1):
  i2c = I2C("/dev/i2c-1")
  i2c.transfer(dev_addr, [I2C.Message([reg_addr1,reg_addr0])])# Reg for read
  sleep(0.5)

  read = I2C.Message([0x0]*4, read=True)
  i2c.transfer(dev_addr, [read])
  i2c.close()
  adc_code=int(bytes(bytearray(read.data)).encode('hex'), 16)

  resolution=2500./0x80000000
  amplitude=(adc_code-0x40000000)*resolution
  if(adc_code==0x3FFFFFFF): amplitude=-1

  temperature= 326-0.5*amplitude
  return temperature

#convert a LinearFloat5_11 formatted word into a floating point value
def lin5_11ToFloat(wordValue):
  binValue = int(wordValue,16)
  binValue=binValue>>8 | (binValue << 8 & 0xFF00)
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

def bmr458_mon(dev_addr,reg_addr):
  i2c = I2C("/dev/i2c-1")
  write = I2C.Message([reg_addr])
  read = I2C.Message([0x0]*2, read=True)
  i2c.transfer(dev_addr, [write, read])
  i2c.close()
  return bytes(bytearray(read.data)).encode('hex')

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

#12V power module BMR458 temperature
reg_value=bmr458_mon(BMR4582_U11_ADDR,0x8D)
temperature=lin5_11ToFloat(reg_value)
print('U11       BMR458      {0:d}                12V DC/DC Converter' .format(trunc(temperature)))

# LTM4630A power modules Temperature monitoring
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBC)
print('U66       LTM4630A    {0:d}                DDR4_VDDQ_1.2V/MGTAVTT_Z_1.2V' .format(trunc(temperature)))
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB5)
print('U73       LTM4650A    {0:d}                Power module of INT_Z_0.85V' .format(trunc(temperature)))
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBD)
print('U55       LTM4630A    {0:d}                Power module of 2.5V' .format(trunc(temperature)))
temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB6)
print('U59       LTM4630A    {0:d}                MGTAVCC_Z_0.9V/3.3V' .format(trunc(temperature)))

if board == 'v4b':
  # LTM4630A power modules Temperature monitoring
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB0)
  print('U122      LTM4630A    {0:d}                Power module of INT_A_0.85V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB8)
  print('U77       LTM4630A    {0:d}                Power module of MGTAVCC_A_0.9V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB1)
  print('U30       LTM4630A    {0:d}                Power module of MGTAVTT_A_1.2V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB9)
  print('U123      LTM4630A    {0:d}                Power module of INT_B_0.85V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB2)
  print('U124      LTM4630A    {0:d}                Power module of MGTAVCC_B_0.9V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBA)
  print('U40       LTM4630A    {0:d}                Power module of MGTAVTT_B_1.2V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB3)
  print('U126      LTM4630A    {0:d}                Power module of INT_C_0.85V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xBB)
  print('U125      LTM4630A    {0:d}                Power module of MGTAVCC_C_0.9V' .format(trunc(temperature)))
  temperature=ltc2499_temp_mon(LTC2499_U2_ADDR,0x90,0xB4)
  print('U44       LTM4630A    {0:d}                Power module of MGTAVTT_C_1.2V' .format(trunc(temperature)))

