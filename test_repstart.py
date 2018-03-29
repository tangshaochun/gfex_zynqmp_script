#!/usr/bin/env python
from time import sleep
import sys
from collections import Counter

from periphery import I2C

def test_repstart():
  i2c = I2C("/dev/i2c-1")
  write = I2C.Message([0x88])
  read = I2C.Message([0x0]*2, read=True) # read 2 bytes

  msgs = [write, read]
  i2c.transfer(0x7F, msgs)

  value = msgs[1].data[1]*256 + msgs[1].data[0]
  return hex(value)

i2c = I2C("/dev/i2c-1")
i2c.transfer(0x70, [I2C.Message([0x01, 0x01])])
i2c.close()

print 'PERIPHERY'

for delay in [0.0]:
  results = []
  for i in range(10000):
    if i % 1000 == 0: sys.stdout.write(str(i))
    results.append(test_repstart())
    if i % 10 == 0: sys.stdout.write('.')
    sys.stdout.flush()
    sleep(delay)
  print Counter(results)
