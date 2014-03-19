#!/usr/bin python 

import constants as consts

from libavg import avg, Point2D
from mingus.midi import fluidsynth
from mingus.containers.Note import Note

SF2 = "GeneralUser.sf2"
if not fluidsynth.init(SF2, "alsa"):
	print "Couldn't load soundfont", SF2

class Key(avg.RectNode):
	def __init__(self, size, pos, pitch, isWhite, parent=None, **kwargs):
		super(Key, self).__init__(**kwargs)
		if parent:
			parent.appendChild(self)
		self.size = size
		self.pos = pos
		self.pitch = pitch
		self.isWhite = isWhite
		self.fillopacity = 1
		self.setNote()
		
		if self.isWhite:
			self.fillcolor = "FFFFFF"
			self.color = "000000"
			self.onDown = self.onWhiteDown
			self.onUp = self.onWhiteUp
			self.onOut = self.onWhiteOut
		else:
			self.fillcolor = "000000"
			self.color = "000000"
			self.onDown = self.onBlackDown
			self.onUp = self.onBlackUp
			self.onOut = self.onBlackOut
		
		self.setEventHandler(avg.CURSORDOWN, avg.MOUSE | avg.TOUCH, self.onDown)
		self.setEventHandler(avg.CURSORUP, avg.MOUSE | avg.TOUCH, self.onUp)
		self.setEventHandler(avg.CURSOROUT, avg.MOUSE | avg.TOUCH, self.onOut)
	
	def setNote(self):
		self.note = Note()
		self.note.from_int(self.pitch-12)
	
	def onDown(self, event):
		pass
	
	def onUp(self, event):
		pass
	
	def onOut(self, event):
		pass
	
	def onWhiteDown(self, event):
		self.fillcolor = "C0C0C0"
		fluidsynth.play_Note(self.note)
	
	def onWhiteUp(self, event):
		self.fillcolor = "FFFFFF"
		
	
	def onWhiteOut(self, event):
		self.fillcolor = "FFFFFF"
		
	
	def onBlackDown(self, event):
		self.fillcolor = "C0C0C0"
		fluidsynth.play_Note(self.note)
	
	def onBlackUp(self, event):
		self.fillcolor = "000000"
	
	def onBlackOut(self, event):
		self.fillcolor = "000000"

		
class Piano():
	# Assume x, y is not normalized
	def __init__(self, game, numOfKeys, x, y):
		self.game = game
		self.numOfKeys = numOfKeys
		self.px = x
		self.py = y
		self.keylist = []	
		self.blackKeyList = []
		self.paintKeys()
	
	def paintKeys(self):
		white = True
		whitePrev = True
		ix = self.px - consts.PIANO_WHITE_WIDTH - 1
		iy = self.py
		for i in range(self.numOfKeys):
			im12 = i % 12
			if(im12 == 0 or ((im12%10) != 0 and (im12 % 5) == 0)):
				whitePrev = white
				white = True
			else:
				whitePrev = white
				white = not white
			
			if (white):
				if (whitePrev):
					ix += consts.PIANO_WHITE_WIDTH+1
				else:
					ix += consts.PIANO_BLACK_WIDTH / 2+1
				
				self.keylist.append(self.createPianoKey(white, ix, iy, i+consts.KEYCODE_OFFSET))
			else:
				ix += consts.PIANO_WHITE_WIDTH - (consts.PIANO_BLACK_WIDTH / 2)
				self.blackKeyList.append({"isWhite":white, "ix":ix, "iy":iy, "pitch":i+consts.KEYCODE_OFFSET})
		
		for i in range(len(self.blackKeyList)):
			item = self.blackKeyList[i]
			self.keylist.append(self.createPianoKey(item["isWhite"], item["ix"], item["iy"], item["pitch"]))
	
	def createPianoKey(self, white, ix, iy, pitch):
		# Assume ix and iy are normalized
		if white:
			size = self.game.game.pnorm((consts.PIANO_WHITE_WIDTH, consts.PIANO_WHITE_HEIGHT))
		else:
			size = self.game.game.pnorm((consts.PIANO_BLACK_WIDTH, consts.PIANO_BLACK_HEIGHT))
		key = Key(size=size, pos=self.game.game.pnorm((ix, iy)), pitch=pitch, isWhite=white,  parent=self.game.node)
		return key


if __name__ == '__main__':
	
	
	player = avg.Player.get()
	canvas = player.createMainCanvas(size=(1024,700))
	rootNode = canvas.getRootNode()
	key1 = Key(pos=pnorm((consts.PIANO_X, consts.PIANO_Y)), pitch=60, parent=rootNode)
	key2 = Key(pos=pnorm((consts.PIANO_X+consts.PIANO_WHITE_WIDTH, consts.PIANO_Y)), pitch=62, parent=rootNode)
	key3 = Key(pos=pnorm((consts.PIANO_X+consts.PIANO_WHITE_WIDTH-consts.PIANO_BLACK_WIDTH/2.0, consts.PIANO_Y)), pitch=61, parent=rootNode)
	player.play()
	
		

		
