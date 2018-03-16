#!/usr/bin/env python
from smbus import SMBusWrapper
with SMBusWrapper(0) as bus:
  bus.write_byte_data(0x68,0x01, 0x0)
  #bus.write_byte_data(0x68,0x03)
  value = bus.read_byte_data(0x68, 0x02)
  value |= bus.read_byte_data(0x68, 0x03) << 8
print value == 0x5345
