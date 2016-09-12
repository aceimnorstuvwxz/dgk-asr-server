#!/usr/bin/env python
#
# 

import sys
import logging
import json
import codecs
import os.path
import uuid
import time
import threading
import functools
from Queue import Queue

import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.gen
import tornado.concurrent
import settings
import common
import wave
import audioop
import subprocess
import json
import threading



import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def setup(self):
        print "called setup"
        self.data = ''

    def asr(self, oldfn):
        cmdd = "cd /home/dgk/kaldi/egs/thchs30/s5/ && ./sod-api.sh /home/dgk/dgk-asr-server/dgkserver/%s %s"  % (oldfn, oldfn[:-4])

        ret = subprocess.Popen(cmdd, stdout=subprocess.PIPE, shell=True).stdout.read()

        return ret 

    def handle(self):
            # self.request is the TCP socket connected to the client
        while True:
            newdata = self.request.recv(4096)  # is blocking ????
            print 'handle recv=', len(newdata)
            if len(newdata) <= 0:
                print "newdata null == 0"
                break
            
            if 'DGKASE' in newdata:
                pos = newdata.find('EOF')
                self.data = self.data + newdata[:pos]

                #ASR with self.data
                self.fnstr = str(uuid.uuid4())

                self.wav = wave.open(self.fnstr + '.wav', 'wb')
                self.wav.setparams((1,2,16000,0,'NONE','not compressed'))
                self.wav.writeframes(self.data)
                self.wav.close()
                ret = self.asr(self.fnstr + '.wav')
                # ret = 'asdfds'
                self.request.send(ret+'EOF')

                #ASR end

                self.data = newdata[pos:]
                break
            else:
                self.data = self.data + newdata
        

if __name__ == "__main__":
    
    print "SocketSimpleServer running"
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    
    server.serve_forever()
