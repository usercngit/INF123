from random import randint
from time import sleep
from common import Model
from math import floor

################### CONTROLLER #############################
class Controller():
    def __init__(self, m):
        self.m = m
    
    def poll(self):
        cmd = None
        chance = randint(1,4)
        
        if chance == 1:
            cmd = 'up'
        if chance == 2:
            cmd = 'right'
        if chance == 3:
            cmd = 'left'
        if chance == 4:
            cmd = 'down'
            
        if cmd:
            self.m.do_cmd(cmd)
    
    def smart_poll(self):
        cmd = None
        
        minxd = minyd = 9999
        closeX = closeY = 0
        
        selfx, selfy, selfw, selfh = self.m.mybox[0], self.m.mybox[1], self.m.mybox[2], self.m.mybox[3]
        selfx = selfx + selfw/2
        selfy = selfy + selfh/2

        
        for index, pellet in enumerate(self.m.pellets):
            xloc, yloc, xdim, ydim = pellet
            xloc = xloc + xdim/2
            yloc = yloc + ydim/2
            
            xd = abs(selfx-xloc)
            yd = abs(selfy-yloc)
            
            if(yd < minyd and xd < minxd):
                minyd = yd
                minxd = xd
                closeX = xloc
                closeY = yloc
            
        if floor(closeX) > floor(selfx):
            cmd = 'right'
        elif floor(closeX) < floor(selfx):
            cmd = 'left'
        if floor(closeY) > floor(selfy):
            cmd = 'down'
        elif floor(closeY) < floor(selfy):
            cmd = 'up'
            
        if cmd:
            self.m.do_cmd(cmd)

################### VIEW #############################
class View():
    def __init__(self, m):
        self.m = m
        self.frame = 0
        
    def display(self):
        self.frame += 1
        if self.frame == 50:
            self.frame = 0
            print ("Position: %d, %d" %(self.m.mybox[0], self.m.mybox[1]))
    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.smart_poll()
    model.update()
    v.display()