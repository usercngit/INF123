from network import Listener, Handler, poll

handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)
        
def broadcastTo(targets, msg, ignore = ""):
    for t in targets:
        if t != ignore:
            t.do_send(msg)
        
def findOccurances(string, char):
    return [i for i, letter in enumerate(string) if letter == char]

def findWords(string, char):
    returnList = []
    for val in findOccurances(string, char):
        start = val+1
        end = string.find(" ", val)
        if end == -1:
            end = len(string)
        
        word = string[start : end]
        if word != "":
            returnList.append(word)
    return returnList

class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            finaltxt = txt
            targets = []
            
            if "+" in txt:
                #find sub names
                subwords = findWords(txt, "+")
                #add self to correct subs
                temptxt = txt + " "
                for word in subwords:
                    if subs.__contains__(word):
                        if self not in subs[word]:
                            subs[word].append(self)
                    else:
                        subs[word] = []
                        subs[word].append(self)
                    
                    word = "+" + word + " "
                    temptxt = temptxt.replace(word, "")
                    temptxt = temptxt.replace("  ", " ")
                    
                #determine if it sends to others
                if (temptxt.replace(" ", "") == ""):
                    self.do_send({'speak': name, 'txt': txt})
                    return
                
                if temptxt[0] == " ":
                    temptxt = temptxt[1:]
                
                #update finaltxt
                finaltxt = temptxt
                    
            if "-" in txt:
                #find unsub words
                unsubwords = findWords(txt, "-")
                
                temptxt = finaltxt + " "
                #unsub from the correct subs
                for word in unsubwords:
                    if subs.__contains__(word):
                        if self in subs[word]:
                            subs[word].remove(self)
                            print "removed"
                            
                    word = "-" + word + " "
                    temptxt = temptxt.replace(word, "")
                    temptxt = temptxt.replace("  ", " ")
                
                #determine if should send to others
                if (temptxt.replace(" ", "") == ""):
                    self.do_send({'speak': name, 'txt': txt})
                    return
                
            if "#" in txt:
                pubwords = findWords(txt, "#")
                for word in pubwords:
                    if word in subs:
                        for subber in subs[word]:
                            if subber not in targets:
                                targets.append(subber)
                
            if "@" in txt:
                whisperwords = findWords(txt, "@")
                for word in whisperwords:
                    for h in handlers:
                        if handlers[h] == word:
                            if h not in targets:
                                targets.append(h)
                
            #if neither pub or whisper is in txt
            if ("#" not in txt) and ("@" not in txt):
                #send to all handlers
                targets = handlers
                print "send to all"
            
            broadcastTo(targets, {'speak': name, 'txt': finaltxt}, self)
            self.do_send({'speak': name, 'txt': txt})


Listener(8888, MyHandler)
while 1:
    poll(0.05)
