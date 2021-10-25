import smbus
import time
import numpy
import math 

#  IMU Magnetometer address  0x1e
m_add = 0x1e

# IMU Acc and Gyro address 0x6b 
ag_add =0x6b

# Initialize I2C (SMBus)
bus = smbus.SMBus(1)

# Verify comunication Magnetometer
if bus.read_byte_data(m_add , 0x0F) == 0x3D:
	print "Mag ready"
else:
	print "Mag not ready"

# Verify comunication Acc and Gyro
if bus.read_byte_data(ag_add , 0x0F) == 0x68:
        print "Acc and Gyro ready"
else:
        print "Acc and Gyro not ready"

#Init Gyro
#CTRL_REG1_G
#settings.gyro.sampleRate = 6
bus.write_byte_data(ag_add, 0x10, 0xC8)
#CTRL_REG2_G
bus.write_byte_data(ag_add, 0x11, 0x00)
#CTRL_REG3_G
bus.write_byte_data(ag_add, 0x12, 0x00)
#CTRL_REG4
bus.write_byte_data(ag_add, 0x1E, 0x38)
#ORIENT_CFG_G
bus.write_byte_data(ag_add, 0x13, 0x00)

stat = 0
while stat:
	#Check if Gyro is available
	byte = bus.read_byte_data(ag_add , 0x17)
	if byte == 7:
		"""
		xgyro = (bus.read_byte_data(ag_add , 0x19) << 8) | bus.read_byte_data(ag_add , 0x18)
		ygyro = (bus.read_byte_data(ag_add , 0x1B) << 8) | bus.read_byte_data(ag_add , 0x1A)
		zgyro = (bus.read_byte_data(ag_add , 0x1D) << 8) | bus.read_byte_data(ag_add , 0x1C)
		print "Gyro x:" + str(float(numpy.int16(xgyro))*0.00875) + " y:" + str(float(numpy.int16(ygyro))*0.00875) + " z: " + str(float(numpy.int16(zgyro))*0.00875)
		print """
		gyro = bus.read_i2c_block_data(ag_add,0x18,6)
                if len(gyro) == 6:
                        xgyro = (gyro[1] << 8) | gyro[0]
                        ygyro = (gyro[3] << 8) | gyro[2]
                        zgyro = (gyro[5] << 8) | gyro[4]
                        print "Gyro x:" + str(float(numpy.int16(xgyro))*0.00875) + " y:" + str(float(numpy.int16(ygyro))*0.00875) + " z: " + str(float(numpy.int16(zgyro))*0.00875)
	else:
		print "No entre"

	time.sleep(1)
	stat = 1


#Init Accel
#CTRL_REG5_XL
bus.write_byte_data(ag_add, 0x1F, 0x38)
#CTRL_REG6_XL
bus.write_byte_data(ag_add, 0x20, 0xC8)
#CTRL_REG7_XL
bus.write_byte_data(ag_add, 0x21, 0x00)

stat = 0
while stat:
	#Check if Acc is available
        byte = bus.read_byte_data(ag_add , 0x27)
        if (byte & (1<<0)):
                acc = bus.read_i2c_block_data(ag_add,0x28,6)
		if len(acc) == 6:
			xacc = (acc[1] << 8) | acc[0]
			yacc = (acc[3] << 8) | acc[2] 
			zacc = (acc[5] << 8) | acc[4]
			print "Acc x:" + str(float(numpy.int16(xacc))*0.000732) + " y:" + str(float(numpy.int16(yacc))*0.000732) + " z: " + str(float(numpy.int16(zacc))*0.000732)
	time.sleep(1)


#Init MAG
#CTRL_REG1_M
bus.write_byte_data(m_add, 0x20, 0x7C)
#CTRL_REG2_M
bus.write_byte_data(m_add, 0x21, 0x00)
#CTRL_REG3_M
bus.write_byte_data(m_add, 0x22, 0x00)
#CTRL_REG4_M
bus.write_byte_data(m_add, 0x23, 0x0C)
#CTRL_REG5_M
bus.write_byte_data(m_add, 0x24, 0x00)

stat = 1
while stat:
        #Check if Acc is available
        byte = bus.read_byte_data(ag_add , 0x27)
        if (byte & (1<<0)):
                mag = bus.read_i2c_block_data(ag_add,0x28,6)
                if len(mag) == 6:
                        xmag = (mag[1] << 8) | mag[0]
                        ymag = (mag[3] << 8) | mag[2]
                        zmag = (mag[5] << 8) | mag[4]
                        print "Mag x:" + str(float(numpy.int16(xmag))*0.00014) + " y:" + str(float(numpy.int16(ymag))*0.00014) + " z: " + str(float(numpy.int16(zmag))*0.00014)
        heading = 0.0
	if (ymag == 0):
    		#heading = (xmag < 0) ? math.pi : 0
		heading = 0.0
  	else:
    		heading = math.atan2(xmag, ymag)

  	heading -= -8.85 * math.pi / 180

  	if (heading > math.pi): 
		heading -= (2 * math.pi)
  	elif (heading < -math.pi):
		 heading += (2 * math.pi)

  	#Convert everything from radians to degrees:
  	heading *= 180.0 / math.pi
	print heading
	time.sleep(1)
