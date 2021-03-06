# #!/usr/bin/env python
# ##############################################
# # The MIT License (MIT)
# # Copyright (c) 2016 Kevin Walchko
# # see LICENSE for full details
# ##############################################
#
# from __future__ import print_function
# from __future__ import division
# import logging
# # from pyxl320 import Packet
# # from pyxl320.Packet import makeSyncAnglePacket
# # from pyxl320 import xl320
# # import pyservos
# from pyservos import Packet
# # from pyservos import AX12
# # from pyservos import XL320
# from pyservos import ServoSerial
#
# logger = logging.getLogger(__name__)
#
#
# # def makeBulkAnglePacket(info):
# # 	"""
# # 	Write bulk angle information to servos.
# #
# # 	info = [[ID, angle], [ID, angle], ...]
# # 	"""
# # 	addr = Packet.le(xl320.XL320_GOAL_POSITION)
# # 	data = []
# # 	for pkt in info:
# # 		data.append(pkt[0])  # ID
# # 		data.append(addr[0])  # LSB
# # 		data.append(addr[1])  # MSB
# # 		data.append(2)
# # 		data.append(0)
# # 		angle = Packet.le(int(pkt[1]/300*1023))
# # 		data.append(angle[0])  # LSB
# # 		data.append(angle[1])  # MSB
# #
# # 	ID = xl320.XL320_BROADCAST_ADDR
# # 	instr = xl320.XL320_BULK_WRITE
# # 	pkt = Packet.makePacket(ID, instr, None, data)  # create packet
# #
# # 	# print(pkt)
# # 	return pkt
#
#
# # I don't like global variables, but I don't know how else to have one array
# # shared by all servos and have one simple class method to push updates
# # gBulkData = []
# # gSyncData = []  # this is much less data than bulk
#
#
# class ServoBase(object):
# 	"""
# 	I might reverse these classes, so i can combine RC and Robotis servos
# 	ServoBase
# 	|  angle()
# 	|  limits()
# 	+- RCServo
# 		|  servo things
# 	+- RobotisServo
# 		|  bulkWrite
# 	"""
# 	ser = None
# 	bulkServoWrite = False
# 	syncServoWrite = False
# 	gSyncData = []  # info = [[ID, angle], [ID, angle], ...]
# 	gBulkData = []
# 	# bulkData = [0]
#
# 	def __init__(self, servo_type):
# 		# just put a dummy serial here, because testing needs it in the angle setter
# 		# if self.ser is None:
# 		# 	self.ser = ServoSerial('dummy')
# 		# 	# raise Exception('ServoBase::__init__() no serial port')
# 		# else:
# 		# 	self.ser = ServoSerial(port)
#
# 		self.packet = Packet(servo_type)
#
# 	def setNewSerial(self, port):
# 		self.ser = ServoSerial(port)
# 		self.ser.open()
#
# 	def setSerial(self, serial):
# 		self.ser = serial
# 		# check if open
#
# 	def bulkWrite(self):
# 		pass
# 	# 	if self.ser is None:
# 	# 		raise Exception('bulkWrite no serial port')
# 	# 	# print('Servo::bulkWrite()')
# 	# 	# global gBulkData
# 	# 	pkt = makeBulkAnglePacket(self.gBulkData)
# 	# 	self.ser.write(pkt)
# 	# 	gBulkData = []  # clear global
#
# 	def syncWrite(self):
# 		# sync write is less data than bulk write as long as all servos are
# 		# getting the same command
# 		if self.ser is None:
# 			raise Exception('syncWrite no serial port')
# 		# print('Servo::syncWrite()')
# 		# global gSyncData
# 		# print('gSyncData', gSyncData)
# 		pkt = self.packet.makeSyncMovePacket(self.gSyncData)
# 		# print('pkt', pkt)
# 		self.ser.write(pkt)
# 		# self.ser.write(pkt)
# 		self.gSyncData = []
#
# 	def write(self):
# 		if self.bulkServoWrite:
# 			self.bulkWrite()
# 		elif self.syncServoWrite:
# 			self.syncWrite()
# 		else:
# 			raise Exception('ServoBase::write() not bulk or sync')
#
#
# class Servo(ServoBase):
# 	"""
# 	Keeps info for servo and commands their movement.
# 	angles are in degrees
#
#                     0
# 	-150 ------ + ------- 150  kinematics (servo_k)
#                    150
#            0 ------ + ------- 300  real servo (servo_r)
#
# 	servo_k commands are between -150 and 150 degrees, with 0 deg being center
#
# 	servo to kinematics: servo_r = servo_k + 150
# 	kinematics to servo: servo_k = servo_r - 150
# 	"""
# 	_angle = 0.0  # current angle
# 	_offset = 150.0  # angle offset default, see above for explaination
# 	minAngle = -150.0
# 	maxAngle = 150.0
# 	ID = 0
#
# 	def __init__(self, ID, servo_type):
# 		"""
# 		limits [angle, angle] - [optional] set the angular limits of the servo
# 		to avoid collision
# 		"""
# 		ServoBase.__init__(self, servo_type)
# 		self.ID = ID
# 		self._offset = offset
# 		self.setServoLimits(150.0, -150.0, 150.0)  # defaults: offset, min, max
#
# 	@property
# 	def angle(self):
# 		"""
# 		Returns the current servo angle
# 		"""
# 		return self._angle
#
# 	@angle.setter
# 	def angle(self, angle):
# 		"""
# 		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
# 		It also commands the servo to move.
# 		"""
#
# 		# saturates the angle if it is outside of the limits
# 		if self.minAngle > angle or angle > self.maxAngle:
# 			# raise Exception('@angle.setter {} > {} > {}'.format(self.minAngle, angle, self.maxAngle))
# 			print('@angle.setter error {} > {} > {}'.format(self.minAngle, angle, self.maxAngle))
#
# 			if self.minAngle > angle:
# 				angle = self.minAngle
# 			elif self.maxAngle < angle:
# 				angle = self.maxAngle
#
# 			print('@angle.setter now {}'.format(angle))
#
# 		# print('servo[{}]: bulkWrite {}'.format(self.ID, self.bulkServoWrite))
#
# 		# only send a pkt if there is a change
# 		if self._angle != angle:
# 			self._angle = angle
# 			# servos are centered at 150 deg, but offset can change
# 			# print(self.ID, angle, angle + self._offset)
#
# 			if self.syncServoWrite:
# 				# global gBulkData
# 				# gBulkData.append([self.ID, angle + self._offset])
# 				self.gSyncData.append([self.ID, angle + self._offset])
# 				# self.bulkData.append([self.ID, angle + self._offset])
# 				# print('servo[{}]: bulkWrite {}'.format(self.ID, gBulkData))
# 			elif self.bulkServoWrite:
# 				# global gBulkData
# 				self.gBulkData.append([self.ID, angle + self._offset])
# 				# gSyncData.append([self.ID, angle + self._offset])
# 				# self.bulkData.append([self.ID, angle + self._offset])
# 				# print('servo[{}]: bulkWrite {}'.format(self.ID, gBulkData))
# 			else:
# 				pkt = self.packet.makeServoMovePacket(self.ID, angle + self._offset)
# 				self.ser.sendPkt(pkt)
# 				# print('sent angle {} [{}]'.format(angle, angle + self._offset))
#
# 	def setServoLimits(self, offset, minAngle, maxAngle):
# 		"""
# 		sets maximum and minimum achievable angles. Remeber, the limits have to
# 		be within the servo range of [0, 180] ... anything more of less won't
# 		work unless your change setServoRangleAngle() to something other than
# 		0 - 180.
#
# 		in:
# 			minAngle - degrees
# 			maxAngle - degrees
# 		"""
# 		if minAngle > maxAngle:
# 			raise Exception("Servo::setServoLimits: min angle > max angle")
#
# 		self._offset = offset
# 		self.minAngle = minAngle
# 		self.maxAngle = maxAngle
