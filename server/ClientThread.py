#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Client thread
# Allows the server to handle the request of multiple clients at once

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import socket
import threading

class ClientThread(threading.Thread):
  def __init__(self,ip,port,clientsocket):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.csocket = clientsocket
    print("[+] New thread started for %s:%s"%(ip,str(port)))

  def handleConnection(conn, cl_addr):
    try:
      print('Connection from', client_address)
      while True:
        data = connection.recv(16)
        if data:
          handleData(data)
        else:
          break
    finally:
      connection.close()

  def handlePing(self,data):
    parts=data.split(' ') if len(data.split(' '))==3 else self.handleBadSyntax()
    if self.verifyUser(parts[1],parts[2]):
      self.csocket.send('accepted'.encode('utf-8'))
      self.updateAlive(parts[1])
    #add "it's dangerous" package for signature

  def updateAlive(self):
    print('updates user record in db')

  def verifyUser(self,user,passwd):
    print('verifies user %s with %s in db'%(user,passwd))
    return True
    # db struct: user name, hashed pass, join time, lastPing, default extension time, new death date, tresholds with actions
    # maybe document oriented db

  def run(self):
    try:
      print ("Connection from : %s on port %s"%(self.ip,str(self.port)))
      data='temp'
      while True and len(data)>0:
        data = self.csocket.recv(2048)
        if data.decode('utf-8').startswith('ping'):
          self.handlePing(data.decode('utf-8'))
        print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data.decode('utf-8')))
    finally:
      print("Client at %s disconnected..."%self.ip)
      self.csocket.close()


