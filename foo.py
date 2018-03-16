import fcntl
from i2cdev import I2C
import ctypes
from smbus import SMBusWrapper, i2c_msg

i2c = I2C(0x70,1)
i2c.write(bytearray([0x01]))
print i2c.read(1)
i2c.close()

with SMBusWrapper(1) as bus:
  write = i2c_msg.write(0x7F, [0x8D])
  read = i2c_msg.read(0x7F, 2)
  bus.i2c_rdwr(write, read)

print list(read)
