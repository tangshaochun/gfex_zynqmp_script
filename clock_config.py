#!/usr/bin/env python
from __future__ import print_function
from time import sleep
import sys

from periphery import I2C
from configurations import Si5345, frequencies
from constants import *

def batch(iterable, n=1):
  l = len(iterable)
  for ndx in range(0, l, n):
    yield iterable[ndx:min(ndx+n, l)]

def set_page(i2c, page):
  print('  Writing page: {0:02x}'.format(page))
  i2c.transfer(SI5345_U137_ADDR, [I2C.Message([0x01, page])])

def do_i2c_block_write(i2c, block):
  page, register, value = block
  if page != do_i2c_block_write.page:
    set_page(i2c, page)
    do_i2c_block_write.page = page
  print('  Writing     : {0:02x}{1:02x}'.format(register, value))
  i2c.transfer(SI5345_U137_ADDR, [I2C.Message([register, value])])

do_i2c_block_write.page = 0x00

def do_i2c_write(i2c, configurations):
  for block in batch(configurations, 3): do_i2c_block_write(i2c, block)

def set_frequency(frequency):
  if frequency not in frequencies:
    print('Invalid frequency, pick one of: {}'.format(frequencies.keys()))
    return False
  i2c = I2C("/dev/i2c-0")
  print('Handling preamble')
  do_i2c_write(i2c, Si5345['preamble'])
  sleep(0.3) # 300 ms delay
  print('Handling modifications for {0:s}'.format(frequency))
  do_i2c_write(i2c, frequencies[frequency])
  print('Handling soft reset')
  do_i2c_write(i2c, Si5345['soft reset'])
  print('Handling postamble')
  do_i2c_write(i2c, Si5345['postamble'])
  print('{0:s} frequency was configured.'.format(frequency))
  i2c.close()
  return True

if __name__ == "__main__":
  frequency = None
  if len(sys.argv) >= 2 and sys.argv[1] in frequencies.keys():
    frequency = sys.argv[1]

  while frequency not in frequencies:
    frequency = raw_input(' or '.join(sorted(frequencies.keys())) + ': ')

  set_frequency(frequency)
