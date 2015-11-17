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

import lib.DatabaseConnection as db

class ClientThread(threading.Thread):
  def __init__(self,ip,port,clientsocket):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.csocket = clientsocket
    print("[+] New thread started for %s:%s"%(ip,str(port)))

  def reply(self, text):
    try:
      self.csocket.send(text.encode('utf-8'))
    except Exception as e:
      print("Could not reply: %s"%e)

  def handleData(self,data):
    try:
      data=data if type(data) is str else data.decode('utf-8')
      if data.startswith('ping'):
        parts = data.split(' ')
        if len(parts)>=3:
          parts.pop(0) #pop "ping"
          user=parts.pop(0)
          pwd=' '.join(parts)
          if self.ping(user, pwd):
            self.reply('accepted User updated')
          else:
            self.reply('rejected User does not exist')
        else:
          self.handleBadData(data)
      elif data.startswith('set'):
        print("TODO: Handle storing user settings")
    except Exception as e:
      print("Exception occured while handling data: %s"%e)
      print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data))
    #add "it's dangerous" package for signature

  def handleBadData(self, data):
    print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data.decode('utf-8')))

  def ping(self, user, pwd):
    user, valid =  self.verifyUser(user,pwd)
    if valid:
      db.updatePing(user)
      print("user %s is alive!"%user.email)
      return True
    return False

  def verifyUser(self,user,passwd):
    u=db.getUser(user)
    return (u, u.verifyPassword(passwd)) if u else (None, False)

  def run(self):
    try:
      print ("Connection from : %s on port %s"%(self.ip,str(self.port)))
      data='temp'
      while True and len(data)>0:
        data = self.csocket.recv(2048)
        self.handleData(data)
    finally:
      print("Client at %s disconnected..."%self.ip)
      self.csocket.close()


