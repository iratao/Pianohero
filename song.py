#!/usr/bin python 

import midi as midi
import logging
import binascii
import time
import constants as consts

from libavg import avg

def bytes_to_int(bytes):
		return int(binascii.b2a_hex(bytes), 16)

g_Log = avg.Logger.get()

class SongNote:
	def __init__(self, game, track_index, channel_index, pitch, velocity, keyDownTime, keyUpTime):
		self.game = game
		self.track_index = track_index
		self.channel_index = channel_index
		self.pitch = pitch
		self.velocity = velocity
		self.keyDownTime = keyDownTime
		self.keyUpTime = keyUpTime
		self.white = consts.KEYBOARD_KEY_COLOR[pitch]
		self.x = self.getXPos()
	
	def __repr__(self):
		r = "track_index = %s, channel_index = %s, pitch = %s, velocity = %s, keyDownTime = %s, keyUpTime = %s" \
		    %(self.track_index, self.channel_index, self.pitch, self.velocity, self.keyDownTime, self.keyUpTime)
		return r
		

	def getXPos(self):
		xPos = consts.PIANO_X
		for i in range(consts.KEYCODE_OFFSET, self.pitch):
			if(consts.KEYBOARD_KEY_COLOR[i]):
				xPos += consts.PIANO_WHITE_WIDTH + 1
		if not consts.KEYBOARD_KEY_COLOR[self.pitch]:
			xPos = xPos - consts.PIANO_BLACK_WIDTH / 2.0
					
		return self.game.xnorm(xPos)

class Song:
	trackNum = 0
	trackLength = 0.0 
	notelist = [ [] for i in range(16) ] # A list of note list for all notes of each channel
	
	tempo = 0 
	tpqn = 0 # ticksPerQuarterNote, milliseonds/tick = tempo/tpqn
	
	# Current time is a number between 0.0 and trackLength + timeWindow
	# stores the current time of the played song
	currTime = 0.0
	
	# prevTime stores the time of the last frame, 
	# so the passed time between frames can be calculated. 
	# Used to scale down time
	prevTime = -1.0
	
	# The length of a tick in milliseconds
	tickLength = 0
	
	# scale down the speed with which the notes are falling
	timeScale = 0.9
	
	# the value determines how long before a note has to be played(millis)
	timeWindow = 700.0
	
	windowHeight = 500 # Physical height of the timeWindow
	
	timeRight = 0
	timeLeft = 0
	isEnd = False
	
	m = midi.MidiFile()
	
	def __init__(self, game, filename, trackNumber=0):
		self.game = game
		midi.register_note = self.register_note 
		self.m.open(filename)
		self.m.read() 
		
		for e in self.m.tracks[trackNumber].events:
			if e.type == "SET_TEMPO":
				self.tempo = bytes_to_int(e.data)
				break
		
		self.tpqn = self.m.ticksPerQuarterNote
		self.tickLength = self.tempo/self.tpqn/1000.0
		
		for i in range(len(self.notelist)):
			for j in range(len(self.notelist[i])):
				self.notelist[i][j].keyDownTime = self.tickToMillis(self.notelist[i][j].keyDownTime)
				self.notelist[i][j].keyUpTime = self.tickToMillis(self.notelist[i][j].keyUpTime)
		self.trackLength = self.getTrackLength()
	
	def getTrackLength(self):
		length = 0
		
		for i in range(len(self.notelist)):
			if len(self.notelist[i]) > 0:
				upTime = self.notelist[i][len(self.notelist[i])-1].keyUpTime
				if upTime > length:
					length = upTime
		return length
		
	def __repr__(self):
		r = "tickLength = %s, trackLength = %s" %(self.tickLength, self.trackLength)
		return r
		
	#track_index, channel_index, pitch, velocity, keyDownTime, keyUpTime
	def register_note(self, t, c, p, v, t1, t2):
		self.notelist[c-1].append(self.toSongNote((t, c, p, v, t1, t2))) 
	
	def toSongNote(self, n):
		return SongNote(self.game, n[0], n[1], n[2], n[3], n[4], n[5])
	
	def tickToMillis(self, tick):
		return tick * self.tickLength
	
	def getCurrentNotes(self):
		retNotes = []
		
		if not self.isEnd:
			if(self.prevTime == -1.0):
				self.prevTime = self.getCurrentTimeMillis()
			self.currTime += (self.getCurrentTimeMillis() - self.prevTime) * self.timeScale
			if(self.currTime > (self.trackLength + self.timeWindow)):
				self.currTime = self.trackLength + self.timeWindow
			self.prevTime = self.getCurrentTimeMillis()
			
			self.timeRight = self.currTime
			self.timeLeft = (self.currTime - self.timeWindow)
			
			for i in range(len(self.notelist)):
				for j in range(len(self.notelist[i])):
					if self.notelist[i][j].keyDownTime > self.timeRight:
						continue
					elif self.notelist[i][j].keyUpTime >= self.timeLeft:
						retNotes.append(self.notelist[i][j])
			
			if self.timeLeft >= self.trackLength:
				self.isEnd = True
				self.notelist[:] = [ [] for i in range(16) ]
			
		return retNotes
		
	def getCurrentTimeMillis(self):
		millis = int(round(time.time() * 1000))
		return millis

if __name__ == "__main__": 
    song = Song("adele-someone_like_you.mid")
    print song.__repr__
    print song.getCurrentNotes()
    time.sleep(3)
    print song.getCurrentNotes()
    
	
	
