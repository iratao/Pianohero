#!/usr/bin python

from libavg import avg, Point2D, AVGApp, AVGNode, fadeOut, gameapp
from libavg.utils import getMediaDir

import logging

import math, random, os

import song as song
import piano as piano
import constants as consts
from widgets import *

g_Player = avg.Player.get()
g_Log = avg.Logger.get()

def create_node(parent_node, type, **props):
    node = avg.Player.get().createNode(type, props)
    parent_node.appendChild(node)
    return node

def set_timeout(millis, handler):
    return avg.Player.get().setTimeout(millis, handler)

def set_interval(millis, handler):
    return avg.Player.get().setInterval(millis, handler)

def clear_interval(id):
    avg.Player.get().clearInterval(id)


class PreGameState:
    def __init__(self, game):
        self.game = game
        self.node = create_node(game.game_node, 'div')
    
    def enter(self):
        self.buttonList = []
        path="midi/"
        dirList = os.listdir(path)
        listlength = len(dirList)
        songList = SongList(game=self.game, pos=(self.game.size.x/3, self.game.ynorm(40)), 
            interleave=10, width=self.game.size.x*1/3, parent=self.node)
        for fname in dirList:
            songList.addSong(text=fname, path=path)
    
    def leave(self):
        self.node.unlink()
    
    def createSongButton(self, text, pos):
        return SongButton(
            pos=pos, text=text, width=self.game.size.y/2, 
            clickHandler=lambda e: self.game.enterGameState('midi/'+text),
            parent=self.node)

class GameState:
    def __init__(self, game, filename, tracknumber=0):
        self.game = game
        self.width, self.height = self.game.size.x, self.game.size.y
        self.node = create_node(self.game.game_node, 'div')
        
        self.song = song.Song(self.game, filename, tracknumber)
        self.tick_interval = int(self.song.tickLength/100)
        self.trackLength = self.song.trackLength
        self.interval_id = None
        self.notenodes = []
        self.filename = filename
        
    
    def enter(self):
        self.run()
    
    def leave(self):
        self.pause()
        self.node.unlink()
    
    def run(self):
        self.paintPiano()
        self.pause()
        self.interval_id = set_interval(self.tick_interval, self.tick)
        
    
    def tick(self):
        if not self.song.isEnd:
            self.paintSong()
        else:
            self.game.enterEndState(self.filename)
    
    def paintPiano(self):
        # Piano coordinates are all decided and finally decided in Piano class
        piano49 = piano.Piano(self, consts.PIANO_KEY_COUNT, consts.PIANO_X, consts.PIANO_Y)
    
    def paintSong(self):
        if self.notenodes:
            for i in range(len(self.notenodes)):
                self.notenodes[i].unlink()
        notes = self.song.getCurrentNotes()
        for i in range(len(notes)):
            note = notes[i]
            # y is the length of the bottom of the block to the top
            y = (((note.keyDownTime- self.song.timeLeft) / self.song.timeWindow) * self.song.windowHeight)
            y = self.song.windowHeight - y
            self.paintNote(note, y)
    
    def paintNote(self, note, y):
        time = ((note.keyUpTime - note.keyDownTime) / self.song.timeWindow) * self.song.windowHeight - 5
        if y <= time and y < self.song.windowHeight:
            sizey = self.game.ynorm(y)
            y=0
        elif y <= time and y >= self.song.windowHeight:
            sizey = self.game.ynorm(self.song.windowHeight)
            y=0
        elif y > time and y < self.song.windowHeight:
            y = y - time
            sizey = self.game.ynorm(time)
        elif y > time and y >= self.song.windowHeight:
            y = y - time
            sizey = self.game.ynorm(self.song.windowHeight - y)
        
        # SongNote.x is finally decided in SongNote, SongNote.y is not
        p = (note.x, self.game.ynorm(y))
        
        if note.white:
            rect = avg.RectNode(pos=p, 
                size=(self.game.xnorm(consts.PIANO_WHITE_WIDTH/1.1), sizey), 
                fillopacity = 1, filltexhref="bar.png", fillcolor = "3399FF", color = "000000", parent=self.node)
        else:
            rect = avg.RectNode(pos=p, 
                size=(self.game.xnorm(consts.PIANO_BLACK_WIDTH/1.1), sizey), 
                fillopacity = 1, filltexhref="bar.png", fillcolor = "3399FF", color = "000000", parent=self.node)
        
        self.notenodes.append(rect)
    
    def pause(self):
        if self.interval_id:
            clear_interval(self.interval_id)
            self.interval_id = None
        
        
class EndState:
    def __init__(self, game, filename):
        self.game = game
        self.node = create_node(game.game_node, 'div')
        self.filename = filename
    
    def enter(self):
        self.createButtons()
        
    def leave(self):
        self.node.unlink()
    
    def createButtons(self):
        screenSize = self.game.size
        buttonSize = Point2D(400, 150)
        xPos = (screenSize.x-buttonSize.x)/2.0
        self.replayButton = Button(
            pos=(xPos, screenSize.y/4),
            upImage="replay_button.png",
            downImage="replay_button_pressed.png",
            clickHandler=lambda e: self.game.enterGameState(self.filename),
            parent=self.node)
        self.mainWindowButton = Button(
            pos=(xPos, 2*screenSize.y/4),
            upImage="mainwindow_button.png",
            downImage="mainwindow_button_pressed.png",
            clickHandler=lambda e: self.game.enterStartState(),
            parent=self.node)

class StartState:
    def __init__(self, game):
        self.game = game
        self.node = create_node(game.game_node, 'div')
    
    def createButtons(self):
        screenSize = self.game.size
        buttonSize = Point2D(400, 150)
        xPos = (screenSize.x-buttonSize.x)/2.0
        
        self.startButton = Button(
            pos=(xPos, screenSize.y/5),
            upImage="start_button.png",
            downImage="start_button_pressed.png",
            clickHandler=lambda e: self.game.enterPreGameState(),
            parent=self.node)
        
        self.exitButton = Button(
            pos=(xPos, 3*screenSize.y/5),
            upImage="exit_button.png",
            downImage="exit_button_pressed.png",
            clickHandler=lambda e: self.game.quit(),
            parent=self.node)
    
    def enter(self):
        self.createButtons()
    
    def leave(self):
        self.node.unlink()

class Pianohero(gameapp.GameApp):
    multitouch = True
    def __init__(self,parentNode):
        super(Pianohero, self).__init__(parentNode)
        self._parentNode.mediadir = getMediaDir(__file__)
        self.currentState = None
        self.size = self._parentNode.size
        self.margin = Point2D(0, 0) 
        
        self.background = create_node(self._parentNode, 'rect', 
            size=self.size, fillcolor='000000', fillopacity=1)
        
        self.game_node = create_node(self._parentNode, 'div', 
            pos=self.margin, size=self.size - self.margin*2)
        
        g_Player.showCursor(True)

    def _enter(self):
        avg.fadeIn(self.game_node, 400, 1.0)
        self.enterStartState()

    def _leave(self):
        if self.currentState:
            self.currentState.leave()
            self.currentState = None
    
    def enterGameState(self, filename):
        if self.currentState != None:
            self.currentState.leave()
        self.currentState = GameState(self, filename)
        self.currentState.enter()
    
    def enterPreGameState(self):
        if self.currentState != None:
            self.currentState.leave()
        self.currentState = PreGameState(self)
        self.currentState.enter()     

    def enterEndState(self, filename):
        if self.currentState != None:
            self.currentState.leave()
        self.currentState = EndState(self, filename)
        self.currentState.enter()
    
    def enterStartState(self):
        if self.currentState != None:
            self.currentState.leave()
        self.currentState = StartState(self)
        self.currentState.enter()

    def xnorm(self, value):
        return int(value * self.size.x / float(consts.ORIGINAL_SIZE[0]))
    
    def ynorm(self, value):
        return int(value * self.size.y / float(consts.ORIGINAL_SIZE[1]))
    
    def pnorm(self, p):
        if len(p) == 2:
            point = Point2D(p)
        elif type(p) == Point2D:
            point = p
        else:
            raise ValueError('Cannot convert %s to Point2D' % str(args))
        
        return Point2D(self.xnorm(point.x), self.ynorm(point.y))

if __name__ == '__main__':
    Pianohero.start()
