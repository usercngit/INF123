from network import Handler, poll
from random import choice
from time import sleep

################### CONTROLLER #############################
class Controller():
    def __init__(self):
        self.dirs = ['up', 'down', 'left', 'right']
        self.cmd = 'down'
    
    def dumb_poll(self):
        return (choice(self.dirs))
    
    def plain_poll(self):
        l, t, w, h = mybox
        r = l + w
        b = t + h
        
        dl = dt = dw = dh = dr = db = 0
        
        for i, p in enumerate(pellets):
            if i == 0:
                dl, dt, dw, dh = p 
                dr = dl + dw
                db = dt + dh
                
        if l > dl:
            self.cmd = 'left'
        elif r < dr:
            self.cmd = 'right'
        else:
            if t > dt:
                self.cmd = 'up'
            elif b < db:
                self.cmd = 'down'
                
        return self.cmd
    
    def smart_poll(self):
        minxd = minyd = 9999
        closeL = closeT = closeR = closeB =0
        
        selfl, selft, selfw, selfh = mybox
        selfr = selfl + selfw
        selfb = selft + selfh
        
        pL, pT, pW, pH  = 0, 0, 0, 0

        for pellet in pellets:
            pL, pT, pW, pH = pellet
            
            xd = abs( (selfl + selfw/2) - (pL + pW/2 ) )
            yd = abs( (selft + selfh/2) - (pT + pH/2 ) )
            
            if(yd < minyd and xd < minxd):
                minyd = yd
                minxd = xd
                closeL = pL
                closeT = pT
                closeR = pL + pW
                closeB = pT + pH
        
        if selfl > closeL:
            self.cmd = 'left'
        elif selfr < closeR:
            self.cmd = 'right'
        else:
            if selft > closeT:
                self.cmd = 'up'
            elif selfb < closeB:
                self.cmd = 'down'
                
        return self.cmd

        
############ NETWORK CONTROLLER#######################
class Client(Handler):
    def on_open(self):
        global running
        running = True
        print "Connected to localhost:8888"
        
    def on_close(self):
        global running
        running = False
        print "Disconnected from server"
    
    def on_msg(self, data):
        global borders, pellets, players, myname, mybox
        
        tempbox = mybox
        temppellets = pellets
        
        borders = data['borders']
        pellets = data['pellets']
        players = {name: p for name, p in data['players'].items()}
        myname = data['myname']
        
        for name, p in players.items():
            if name == myname:
                mybox = p
                
        if(self.compareBox(tempbox, mybox) and self.comparePellets(temppellets, pellets, mybox)):
            print "Nom nom, delicious pellet"
    
    def compareBox(self, oldBox, newBox):
        x, y, w, h = oldBox
        x2, y2, w2, h2 = newBox
        if ( w2 > w ) and ( h2 > h ):
            return True
        return False
    
    def comparePellets(self, oldPellets, newPellets, box):
        if oldPellets == [] or newPellets == [] or box == []:
            return False
        for i, p in enumerate(newPellets):
            if oldPellets[i] != p:
                if self.collide_boxes(box, oldPellets[i]):
                    return True
        return False
    
    #I know this is kind of cheap, but it is the only way to be fairly certain of weather or not the bot actually ate a pellet
    def collide_boxes(self, box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
################### VIEW #############################
class View():
    def __init__(self):
        self.frame = 0
        
    def display(self):
        self.frame += 1
        if self.frame == 50:
            self.frame = 0
            print ("Position: %d, %d" %(mybox[0], mybox[1]))
    
################### LOOP #############################
running = False

borders = []
pellets = []
players = {}  # map player name to rectangle
myname = None
mybox = 0, 0, 0, 0

client = Client('localhost', 8888)

c = Controller()
v = View()

while not running:
    poll()

while running:
    poll()
    
    msg = {'input': c.smart_poll()}
    client.do_send(msg)
    
    sleep(1. / 20)