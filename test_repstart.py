#!/usr/bin/env python
from smbus import SMBusWrapper, i2c_msg
from time import sleep
import sys
from collections import Counter
def test_repstart():
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

with SMBusWrapper(1) as bus:
  bus.write_byte_data(0x70,0x01, 0x01)

for delay in [0.0]:
  results = []
  for i in range(10000):
    if i % 1000 == 0: sys.stdout.write(str(i))
    results.append(test_repstart())
    if i % 10 == 0: sys.stdout.write('.')
    sys.stdout.flush()
    sleep(delay)
  print Counter(results)
