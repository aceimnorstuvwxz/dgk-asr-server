#!/usr/bin/env python
#
# Copyright 2013 Tanel Alumae
# 2016 chenbingfeng

"""
Reads speech data via websocket requests, sends it to Redis, waits for results from Redis and
forwards to client via websocket
"""


import socket
import wave
  
if "__main__" == __name__:  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9999))

    wavf = wave.open('speech/speech0.wav', 'r')
    data = wavf.readframes(wavf.getnframes())
    print 'data len=', len(data)
    sock.send(data + 'DGKASE')
    ret = sock.recv(1024)
    print "ret=", ret
    