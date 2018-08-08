#!/usr/bin/env python
# expect to be running python3 in the future
from __future__ import print_function
# manufacturer requires a specific time-delay from preamble to setting registers
from time import sleep
# command-line configuration for user-friendliness
import sys
# http://python-periphery.readthedocs.io/en/latest/
# this interfaces with the virtual filesystem to send low-level HW commands to the HW
# for example GPIO, LED, SPI, I2C, etc.
from periphery import I2C
# import configurations for clock chip for v4
from configurations import Si5345, frequencies
# import global constants such as i2c bus locations
from constants import *

# this function batches iterables into iterables of batches
# a list of objects to a list of groups of objects of fixed size
# - it is used to batch a list of register commands into groups of triplets for sending along i2c
def batch(iterable, n=1):
  l = len(iterable)
  for ndx in range(0, l, n):
    yield iterable[ndx:min(ndx+n, l)]

# set page to group up commands as required by manufacturer instructions
# for the Si5345 clock chip
def set_page(i2c, page):
  print('  Writing page: {0:02x}'.format(page))
  i2c.transfer(SI5345_U137_ADDR, [I2C.Message([0x01, page])])

# write a block of commands over i2c
def do_i2c_block_write(i2c, block):
  page, register, value = block
  # change page if page changes
  if page != do_i2c_block_write.page:
    set_page(i2c, page)
    do_i2c_block_write.page = page
  print('  Writing     : {0:02x}{1:02x}'.format(register, value))
  i2c.transfer(SI5345_U137_ADDR, [I2C.Message([register, value])])
# initialize page to 0x0
do_i2c_block_write.page = 0x00

# write a command over i2c
# takes a list of commands, batches them into triplets, and executes block writes
def do_i2c_write(i2c, configurations):
  for block in batch(configurations, 3): do_i2c_block_write(i2c, block)

# entrypoint to script to set the frequency of the clock chip and lock it
# such as "set_frequency('MixMHz')" using the allowed frequencies specified in the configuration file
# this is necessary when first setting up the board or changing the frequency based on the firmware
# The engineers will need to write specifications for which frequencies to use
def set_frequency(frequency):
  if frequency not in frequencies:
    print('Invalid frequency, pick one of: {}'.format(frequencies.keys()))
    return False
  # select i2c device
  i2c = I2C("/dev/i2c-0")
  # preamble, postamble, and soft-reset defined in configurations on a per-clock-chip basis
  # send the manufacturer preamble for initializing the clock chip for being able to accept register modifications
  print('Handling preamble')
  do_i2c_write(i2c, Si5345['preamble'])
  sleep(0.3) # 300 ms delay required by manufacturer
  # write the frequency configuration defined by manufacturer
  print('Handling modifications for {0:s}'.format(frequency))
  do_i2c_write(i2c, frequencies[frequency])
  # required by manufacturer for finishing register modifications
  print('Handling soft reset')
  do_i2c_write(i2c, Si5345['soft reset'])
  # required by manufacturer to lock the clock
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
