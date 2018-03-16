from i2cdev import I2C

def ps_i2c_bus_read(device, bus, register, N):
  i2c = I2C(device, bus)
  i2c.write(bytearray(register))
  data = i2c.read(N)
  i2c.close()
  return data

def ps_i2c_bus_write(device, bus, register, data):
  i2c = I2C(device, bus)
  i2c.write(bytearray([register, data]))
  i2c.close()
  return True

def ps_i2c_bus_action(device, bus, register, **kwargs):
  if 'read' in kwargs:
    if 'N' not in kwargs: raise KeyError('Specify N bytes with "N=#"')
    return ps_i2c_bus_read(device, bus, register, kwargs['N'])

  if 'write' in kwargs:
    if 'data' not in kwargs: raise KeyError('Specify data to write with "data=0x..."')
    return ps_i2c_bus_write(device, bus, register, data)

# read call
#ps_i2c_bus_action(0x68, 0, 0x0001, read=True, N=1)
# write call
#ps_i2c_bus_action(0x68, 0, 0x0001, write=True, data=0x00)

print ps_i2c_bus_action(0x68, 0, 0x0003, read=True, N=2)
