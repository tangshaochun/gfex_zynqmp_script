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
    #sleep(1)
  value = list(read)
  #print("[{0}]".format(', '.join(map(str, value))))
  value = value[1]*256 + value[0]
  #print('BMR458 value  is {0:d}' .format(value))
  return '{0:x}'.format(value)

def ina226_reg_write(dev_addr,reg_addr,reg_value0,reg_value1):
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([reg_addr,reg_value0,reg_value1]))# SENSOR_IIC_BUS is selected
  #print('write done')
  i2c.close()
def ina226_reg_read(dev_addr,reg_addr,nbits):
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([reg_addr]))# Reg for read
  reg_value=i2c.read(nbits)# Read N bits.
  i2c.close()
  #print('read done')
  return reg_value

def ltc2499_current_mon(dev_addr,reg_addr0,reg_addr1):
  i2c = I2C(dev_addr, 1) # device @ dev_addr, bus 1
  i2c.write(bytearray([reg_addr1,reg_addr0]))# Reg for read
  sleep(0.5)
  adc_code=i2c.read(4)# Read 4 bits.
  i2c.close()
  sleep(0.0)
  resolution=2500./0x80000000
  if(int(adc_code,16)<0x40000000):
    amplitude=0
  else:
    amplitude=(int(adc_code,16)-0x40000000)*resolution
  return amplitude/40

def adm1066_voltage_mon(dev_addr,reg_value_80,reg_value_81,reg_addr_vh,reg_addr_vl,average_on):
  #read the ADM1066 U52 with addr 0x34 and 0x35
  i2c = I2C(dev_addr, 1) # device 0x34/0x35
  i2c.write(bytearray([0x82,0x0+average_on*4]))# reset STOPWRITE BIT
  i2c.write(bytearray([0x80,reg_value_80]))# reg 0x80 select channel
  i2c.write(bytearray([0x81,reg_value_81]))# reg 0x81

  i2c.write(bytearray([0x82,0x01+average_on*4]))# reg 0x82 select go bit
  i2c.write(bytearray([0x82]))# reg 0x82
  status=i2c.read(1)# read the go bit status
  if int(status,16) != average_on*4:
    status=i2c.read(1) #keep checking the go bit, until it is equal average_on*4
    sleep(0.5)
  i2c.write(bytearray([0x82,0x08+average_on*4]))

  i2c.write(bytearray([reg_addr_vh]))# reg 0xA8 VH high 8bit voltage value
  vh=i2c.read(1)#
  i2c.write(bytearray([reg_addr_vl]))# reg 0xA9 VH low 8 bits voltag value
  vl=i2c.read(1)#
  i2c.close()
  voltage= ((int(vh,16)*256+int(vl,16))*2.048/4095)/(2**(average_on*4))
  return voltage
  #print('12V  measured by ADM1066 is {0:.3f} V'.format(voltage))


#set the i2c mux channel, since all the device is under SENSOR_IIC_BUS, just need to set once at the begining.
i2c = I2C(TCA9548_U93_ADDR, 1) # device @ 0x70, bus 1
i2c.write(bytearray([SENSOR_IIC_BUS]))# SENSOR_IIC_BUS is selected
i2c.close()
print('-------------Power monitoring of gFEX production board--------------------')
print('Power Rail       Monitoring Device    Voltage(V)    Current(A)    Power(W)')
#12V power module BMR458 Voltage
reg_value=bmr458_mon(BMR4582_U11_ADDR,0x88)
voltage=lin5_11ToFloat(reg_value)
print('48V/54V          BMR458 DC/DC U11     {0:.3f}        N/A           N/A' .format(voltage))

reg_value=bmr458_mon(BMR4582_U11_ADDR,0x8B)
voltage=2**(-11)*int(reg_value,16)
reg_value=bmr458_mon(BMR4582_U11_ADDR,0x8C)
current=lin5_11ToFloat(reg_value)
print('12V              BMR458 DC/DC U11     {0:.3f}        {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))

#INA226 Monitoring
ina226_reg_write(INA226_U81_ADDR,0x06,0x80,0x02)#set alert pin active low
ina226_reg_write(INA226_U81_ADDR,0x07,0x2E,0xE0)#set the alert to 30A
value=ina226_reg_read(INA226_U81_ADDR,0x02,2)#read the voltage
voltage=int(value,16)*1.25/1000
value=ina226_reg_read(INA226_U81_ADDR,0x01,2)
current=int(value,16)*2.5/1000
print('12V              INA226 U81           {0:.3f}        {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))

#ADM1066 Monitoring
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xEF,0x1F,0xA8,0xA9,1)# read ADM1066 U52 channel VH, 12V
#print('12V           ADM1066 U52          {} voltage measured by ADM1066 is {0:.3f} V'.format(voltage*10.472))
#print('12V           ADM1066 U52          {0:.3f}        {1:.3f}         {2:.3f}' .format(voltage*,current,voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0x7F,0x1B,0xB4,0xB5,1)# read ADM1066 U52 channel AUX1 5V IPMI
print('5V IPMI          ADM1066 U52          {0:.3f}         N/A           N/A' .format(voltage*5))

voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xFE,0x1F,0xA0,0xA1,1)# read ADM1066 U52 channel VP1 3.3V IPMI
print('3.3V IPMI        ADM1066 U52          {0:.3f}         N/A           N/A' .format(voltage*4.363))

#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xFD,0x1F,0xA2,0xA3,1)# read ADM1066 U52 channel VP2 INT_A_0.85V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB0)#read current of INT_A_0.85V from LTC2499
#print('INT_A_0.85V      ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xFB,0x1F,0xA4,0xA5,1)# read ADM1066 U52 channel VP3 MGTAVCC_A_0.9V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB8)##read current of MGTAVCC_A_0.9V from LTC2499
#print('MGTAVCC_A_0.9V   ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xF7,0x1F,0xA6,0xA7,1)# read ADM1066 U52 channel VP4 MGTAVCC_A_1.2V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB1)##read current of MGTATT_A_1.2V from LTC2499
#print('MGTAVTT_A_1.2V   ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xDF,0x1F,0xAA,0xAB,1)# read ADM1066 U52 channel VX1 INT_B_0.85V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB9)
#print('INT_B_0.85V      ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xBF,0x1F,0xAC,0xAD,1)# read ADM1066 U52 channel VX2 MGTAVCC_B_0.9V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB2)
#print('MGTAVCC_B_0.9V   ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0x7F,0x1F,0xAE,0xAF,1)# read ADM1066 U52 channel VX3 MGTAVTT_B_1.2V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xBA)
#print('MGTAVTT_B_1.2V   ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0xFF,0x1E,0xB0,0xB1,1)# read ADM1066 U52 channel VX4 INT_C_0.85V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB3)
#print('INT_C_0.85V      ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U52_ADDR,0x7F,0x1D,0xB2,0xB3,1)# read ADM1066 U52 channel VX5 MGTAVCC_C_0.9V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xBB)
#print('MGTAVCC_C_0.9V   ADM1066 U52/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))
#
#voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0xBF,0x1F,0xAC,0xAD,1)# read ADM1066 U51 channel VX2 MGTAVTT_C_1.2V
#current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB4)
#print('MGTAVTT_C_1.2V   ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0x7F,0x1F,0xAE,0xAF,1)# read ADM1066 U51 channel VX3 INT_Z_0.85V
current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xBC)
print('INT_Z_0.85V      ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0xFF,0x1E,0xB0,0xB1,1)# read ADM1066 U51 channel VX4 MGTAVCC_Z_0.9V
current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB5)
print('MGTAVCC_Z_0.9V   ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0x7F,0x1D,0xB2,0xB3,1)# read ADM1066 U51 channel VX5 MGTAVTT_Z_1.2V
current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xBD)
print('MGTAVTT_Z_1.2V   ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage,current,voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0xFE,0x1F,0xA0,0xA1,1)# read ADM1066 U51 channel VP1 2.5V
current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xBE)
print('2.5V             ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage*2.181,current,2.181*voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0xFD,0x1F,0xA2,0xA3,1)# read ADM1066 U51 channel VP2 3.3V
current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB7)/5
print('3.3V             ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage *4.363,current,4.363*voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0xFB,0x1F,0xA4,0xA5,1)# read ADM1066 U51 channel VP3 1.8V
current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xB6)/2
print('1.8V             ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage*2.181,current,2.181*voltage*current))

voltage=adm1066_voltage_mon(ADM1066_U51_ADDR,0xF7,0x1F,0xA6,0xA7,1)# read ADM1066 U51 channel VP4 DDR4_VDDQ_0.6V
current=ltc2499_current_mon(LTC2499_U1_ADDR,0x90,0xBF)/10
print('DDR4_VTT_0.6V    ADM1066 U51/LTC2499  {0:.3f}         N/A           N/A' .format(voltage))
print('DDR4_VDDQ_1.2V   ADM1066 U51/LTC2499  {0:.3f}         {1:.3f}         {2:.3f}' .format(voltage*2,current,2*voltage*current))

