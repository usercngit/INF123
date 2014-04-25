from network import Listener, Handler, poll #@UnresolvedImport

 
handlers = {}  # map client handler to user name
 
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        for client in handlers:
            client.do_close()
     
    def on_msg(self, msg):
        if 'join' in msg:
            #add player name msg['join']
            #self is 'h', aka client handler connection (IP, etc)
            handlers[self] = msg['join']
            
            for client in handlers:
                client.do_send(handlers[self] + " has joined the chat room.")
                
        elif 'txt' in msg:
            if msg['txt'].lower() == 'quit':
                self.do_send("~~You are disconnecting~~")
                self.do_close()
                del handlers[self]
                
                for client in handlers:
                    client.do_send("~~" + msg['speak'] + " has disconnected~~")
                    
            elif msg['txt'].lower() == 'who\'s here?':
                self.do_send("    SERVER SAYS:\n" + self.clientString() + "\n    ARE HERE")
                
            else:
                for client in handlers:
                    
                    if client != self:
                        client.do_send(handlers[self] + "says: " + msg['txt']) 
            
        print msg
        
    def clientString(self):
        clientstring = []
        for client in handlers:
            clientstring.append(str(handlers[client]))
        rstring = '\n'.join([str(item) for item in clientstring])
        return rstring
 
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds
