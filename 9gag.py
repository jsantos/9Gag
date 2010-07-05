#!/usr/bin/env python
# encoding: utf-8
"""
9gag.py

Created by Jorge Santos on 2010-06-27.
Copyright (c) 2010 DEI-FCTUC. All rights reserved.
"""

import feedparser, os, sys, urllib, cStringIO
from PIL import Image as PilImage
from BeautifulSoup import BeautifulSoup
from pymt import *


class Gag(MTWidget):
    def __init__(self, **kargs):
        super(Gag, self).__init__()
            
        gag = feedparser.parse('http://9gag.com/rss/site/feed.rss')
        gagentries = gag.entries

        imgs = []
        numImgs = 0
        delay = 100

        for entry in gagentries:
            for content in entry.content:
                soup = BeautifulSoup(content.value)
                for s in soup.findAll('img'):
                    imgs.append(s['src'])
            
        k = MTKineticList(size=getWindow().size, friction=1, do_x=True,
                          h_limit=1, do_y=False, title='9GAG - New Definition of Fun', deletable=False,
                          searchable=False, w_limit=0, padding_x=10)

        for i in xrange(len(imgs)):
            f = urllib.urlopen(imgs[i])
            im = cStringIO.StringIO(f.read())
            img = PilImage.open(im)
            if img.size[1] > getWindow().size[1]-delay:
                newWidth = (img.size[0] * getWindow().size[1]-delay)/img.size[1]
                img = img.resize((newWidth,getWindow().size[1]-delay))
            img.save("img_%s.png" %numImgs)
            numImgs+=1

    
        for i in xrange(numImgs):
            image = MTKineticImage(filename="img_%s.png" %i)
            k.add_widget(image)
    
        self.add_widget(k)    
        
        exitButton = MTButton(label='X', pos = ((getWindow().size[0]-50),0), size=(50,50))   
        @exitButton.event
        def on_release(touch):
        	exit()
    
        self.add_widget(exitButton)
        

if __name__ == '__main__':
    runTouchApp(Gag())