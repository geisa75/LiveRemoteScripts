# http://lividinstruments.com

from __future__ import with_statement
import Live
import math

""" _Framework files """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
from _Framework.ChannelStripComponent import ChannelStripComponent # Class attaching to the mixer of a given track
#from _Framework.ClipSlotComponent import ClipSlotComponent # Class representing a ClipSlot within Live
from _Framework.CompoundComponent import CompoundComponent # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import ControlElement # Base class for all classes representing control elements on a controller 
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live
from _Framework.DeviceComponent import DeviceComponent # Class representing a device in Live
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
from VCM600.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.ModeSelectorComponent import ModeSelectorComponent # Class for switching between modes, handle several functions with few controls
from _Framework.NotifyingControlElement import NotifyingControlElement # Class representing control elements that can send values
from _Framework.SceneComponent import SceneComponent # Class representing a scene in Live
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent as SessionZoomingComponent# Class using a matrix of buttons to choose blocks of clips in the session
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
from VCM600.TrackEQComponent import TrackEQComponent # Class representing a track's EQ, it attaches to the last EQ device in the track
from VCM600.TrackFilterComponent import TrackFilterComponent # Class representing a track's filter, attaches to the last filter in the track
from _Framework.TransportComponent import TransportComponent # Class encapsulating all functions in Live's transport section


""" Here we define some global variables """
CHANNEL = 0	  #main channel (0 - 15)
ALIAS8_KNOBS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
ALIAS8_FADERS = [17,18,19,20,21,22,23,24]
ALIAS8_BUTTONS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
ALIAS8_MFADER = [25]
ALIAS8_LCDS = [16,17]
ALIAS8_ENCODER = [42]

class LividAlias8M4L(ControlSurface):
  __module__ = __name__
  __doc__ = " LividAlias8M4L controller script "

  def __init__(self, c_instance):
	super(LividAlias8M4L, self).__init__(c_instance)
	with self.component_guard():
	  self._host_name = 'LividAlias8M4L'
	  self._color_type = 'Base'
	  self.log_message("--------------= LividAlias8M4L log BEGIN SCRIPT =--------------")
	  self._setup_controls()
	  
  """script initialization methods"""
  
  def _setup_controls(self):
	is_momentary = True
	self._knob = [None for index in range(16)]
	self._fader = [None for index in range(8)]
	self._button = [None for index in range(16)]
	self._mfader = [None for index in range(1)]
	self._lcd = [None for index in range(2)]
	self._encoder = [None for index in range(1)]
	self._tfader = [None for index in range(16)]
	self._tfader_touch = [None for index in range(8)]
	self._tbutton = [None for index in range(1)]
	for index in range(16):
	  self._tfader[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, ALIAS8_KNOBS[index], Live.MidiMap.MapMode.absolute)
	  self._tfader[index].name = 'knob[' + str(index) + ']'
	for index in range(8):
	  self._tfader_touch[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, ALIAS8_FADERS[index], Live.MidiMap.MapMode.absolute)
	  self._tfader_touch[index].name = 'fader[' + str(index) + ']'
	for index in range(16):
	  self._pad[index] = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, ALIAS8_BUTTONS[index])
	  self._pad[index].name = 'btn[' + str(index) + ']'
	for index in range(1):
	  self._pad_cc[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, ALIAS8_MFADER[index], Live.MidiMap.MapMode.absolute)
	  self._pad_cc[index].name = 'mfader[' + str(index) + ']'
	for index in range(1):
	  self._tbutton[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, ALIAS8_ENCODER[index], Live.MidiMap.MapMode.absolute)
	  self._tbutton[index].name = 'enc[' + str(index) + ']'
	for index in range(2):
	  self._button[index] = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, ALIAS8_LCD[index])
	  self._button[index].name = 'lcd[' + str(index) + ']' 
	
  def receive_value(self, value):
	self._value = value

	
  """LividAlias8M4L script disconnection"""
  def disconnect(self):
	self.log_message("--------------= LividAlias8M4L log END =--------------")
	ControlSurface.disconnect(self)
	return None