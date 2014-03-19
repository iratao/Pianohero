#!/usr/bin python 
from libavg.ui import button
from libavg import avg, Point2D

import constants as consts

g_Player = avg.Player.get()
g_Log = avg.Logger.get()

class GameWordsNode(avg.WordsNode):
    def __init__(self, *args, **kwargs):
        kwargs['font'] = 'EMPRetro'
        kwargs['sensitive'] = False
        if 'fontsize' in kwargs:
            kwargs['fontsize'] = max(kwargs['fontsize'], 7)
        super(GameWordsNode, self).__init__(*args, **kwargs)

class VLayout(avg.DivNode):
    def __init__(self, interleave, width, *args, **kwargs):
		# Assume interleave and width are all normalized
        super(VLayout, self).__init__(*args, **kwargs)
        self.interleave = interleave
        self.size = Point2D(width, 1)
        self.yoffs = 0
        self.objs = []
    
    def add(self, obj, offset=0):
        self.appendChild(obj)
        self.objs.append(obj)
        obj.y = self.yoffs + offset
        if obj.size != Point2D(0, 0):
            objSize = obj.size
        else:
            objSize = obj.getMediaSize()
            
        self.yoffs += objSize.y + self.interleave + offset
        self.height = self.yoffs
        g_Log.trace(g_Log.APP, 'obj.y=%s objSize=%s height=%s'%(obj.y,objSize,self.height))

class SongItem(avg.DivNode):
    def __init__(self, game, text, path, width, *args, **kwargs):
        super(SongItem, self).__init__(*args, **kwargs)
        self.game = game
        self.bg = avg.RectNode(opacity=0, fillopacity=1, 
            fillcolor="110C11", parent=self)

        self.wnode = GameWordsNode(text=text, fontsize=game.ynorm(20), alignment='center',
                color=consts.COLOR_SILVER, parent=self)
        border = self.wnode.getMediaSize().y / 6
        self.wnode.y = border
        self.size = (width, self.wnode.getMediaSize().y + border * 2)
#        posX = self.game.xnorm(consts.ORIGINAL_SIZE[0])-self.size.x
#        self.pos.x = posX
        self.bg.size = self.size
        self.wnode.x = width / 2

        self.setEventHandler(avg.CURSORDOWN, avg.MOUSE | avg.TOUCH,
                lambda e: self.executeCallback(path+text))
        
#        self.curContainer = avg.DivNode(sensitive=False, parent=self)
#        avg.LineNode(pos1=(0, 0), pos2=(0, self.height), color=consts.COLOR_RED,
#                strokewidth=3, parent=self.curContainer)
    
    def executeCallback(self, filename):
		self.bg.filltexhref="song_button_pressed.png"
		self.game.enterGameState(filename)
#        g_Log.trace(g_Log.APP, 'executeCallback:'+filename)

class SongList(avg.DivNode):
	def __init__(self, game, interleave, *args, **kwargs):
		# Assume interleave and width is normalized
		super(SongList, self).__init__(*args, **kwargs)
		self.game = game
		self.layout = VLayout(interleave=interleave, width=self.width, parent=self)
		
	def addSong(self, text, path):
		self.layout.add(SongItem(game=self.game, text=text, path=path, width=self.width))

class Button(button.Button):

    def __init__(self, upImage, downImage, **kwargs):
        upNode = avg.ImageNode(href=upImage)
        downNode = avg.ImageNode(href=downImage)
        button.Button.__init__(self, upNode=upNode, downNode=downNode, **kwargs)


		
		
