#!/usr/bin/env python
from smbus import SMBusWrapper, i2c_msg
from time import sleep
import sys
from collections import Counter

from periphery import I2C

def test_repstart(smbus=True):

  if smbus:
    try:
      with SMBusWrapper(1) as bus:
        write = i2c_msg.write(0x7F, [0x88])
        read = i2c_msg.read(0x7F, 2)
        bus.i2c_rdwr(write, read)
      value = list(read)
      value = value[1]*256 + value[0]
      return  hex(value)
    except IOError:
      return False
  else:
    i2c = I2C("/dev/i2c-1")
    write = I2C.Message([0x88])
    read = I2C.Message([0x0]*2, read=True) # read 2 bytes

    msgs = [write, read]
    i2c.transfer(0x7F, msgs)

    value = msgs[1].data[1]*256 + msgs[1].data[0]
    return hex(value)

with SMBusWrapper(1) as bus:
  bus.write_byte_data(0x70,0x01, 0x01)

for smbusFlag in [True, False]:
  print 'SMBUS'*(smbusFlag == True)
  print 'PERIPHERY'*(smbusFlag == False)

  for delay in [0.0]:
    results = []
    for i in range(10000):
      #if i % 1000 == 0: sys.stdout.write(str(i))
      results.append(test_repstart(smbusFlag))
      #if i % 10 == 0: sys.stdout.write('.')
      sys.stdout.flush()
      sleep(delay)
    print Counter(results)
