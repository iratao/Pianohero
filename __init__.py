import os

from libavg.utils import getMediaDir, createImagePreviewNode
from game import Pianohero

__all__ = ['apps']

apps = ({'class': Pianohero},
       )

if __name__ == '__main__':
    Pianohero.start()
