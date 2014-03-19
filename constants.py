#!/usr/bin python 

ORIGINAL_SIZE = (1024, 700)

COLOR_BLUE = '0000ff'
COLOR_RED = 'ff0000'
COLOR_SILVER = 'cccccc'

PIANO_X = 150
PIANO_Y = 500
PIANO_WHITE_WIDTH = 20
PIANO_WHITE_HEIGHT = 150
PIANO_BLACK_WIDTH = 14
PIANO_BLACK_HEIGHT = 100
TICK_INTERVAL = 1000
KEYCODE_OFFSET = 36

PIANO_KEY_COUNT = 61

KEYBOARD_KEY_COLOR = ( True,True,True,True,True,True,True,True,True,True,
    True,True,True,True,True,True,True,True,True,True,True,
    True,False,True,
    True,False,True,False,True,True,False,True, False, True, False, True, # 24~35
    True,False,True,False,True,True,False,True, False, True, False, True, # 36~47
    True,False,True,False,True,True,False,True, False, True, False, True, # 48~59
    True,False,True,False,True,True,False,True, False, True, False, True, # 60~71
    True,False,True,False,True,True,False,True, False, True, False, True, # 72~83
    True,False,True,False,True,True,False,True, False, True, False, True, # 84~95
    True,False,True,False,True,True,False,True, False, True, False, True, # 96~107
    True
    )
