
"""
Pneumatic Classes.

This Module contains all the classes relating to Pneumatic Actuators 
"""

from ophyd import Component as Cpt
from ophyd import EpicsSignalRO, EpicsSignal
from ophyd.device import Device
from pcdsdevices.interface import LightpathMixin

class BeckhoffPneumatic(LightpathMixin):
	"""
	Class containing basic Beckhoff Pneumatic support
	"""
	lightpath_cpts = ['limit_switch_in', 'limit_switch_out']

	#readouts
	limit_switch_in = Cpt(EpicsSignalRO, ':PLC:bInLimitSwitch')
	limit_switch_out = Cpt(EpicsSignalRO, ':PLC:bOutLimitSwitch')
	
	retract_status = Cpt(EpicsSignalRO, ':bRetractDigitalOutput')
	insert_status = Cpt(EpicsSignalRO, ':bInsertDigitalOutput')
    
	#logic and supervisory
	interlock_ok = Cpt(EpicsSignalRO, 'bInterlockOK')
	insert_ok = Cpt(EpicsSignalRO, 'bInsertEnable')
	retract_ok = Cpt(EpicsSignalRO, 'bretractEnable')

	#commands
	insert_signal = Cpt(EpicsSignal, 'CMD:IN')
	retract_signal = Cpt(EpicsSignal, 'CMD:OUT')

	#returns
	busy = Cpt(EpicsSignalRO, ':bBusy')
	done = Cpt(EpicsSignalRO, ':bDone')
	reset = Cpt(EpicsSignal, ':bReset')
	error = Cpt(EpicsSignalRO, ':PLC:bError')
	error_id = Cpt(EpicsSignalRO, ':PLC:nErrorId')
	error_message = Cpt(EpicsSignalRO, ':PLC:sErrorMessage')
	position_state = Cpt(EpicsSignalRO, ':nPositionState')

	def insert(self):
		"""
		Method for inserting Beckhoff Pneumatic Actuator
		"""
		if self.insert_ok:
			self.insert_signal.put(1)
		else:
			pass
			#throw?
		
	def retract(self):
		if self.retract_ok:
			self.retract_signal.put(1)
		else:
			pass
			#throw?

	trans = 0.0 if limit_switch_in and not limit_switch_out else 1.0

	def calc_lightpath_state(self, limit_switch_in=None, limit_switch_out=None):
		status = LightpathState(
			inserted=limit_switch_in and not limit_switch_out,
			removed=limit_switch_out and not limit_switch_in,
			output={self.output_branches[0]: trans}
		)
		return status



	




