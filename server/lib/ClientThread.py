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

  def verifyVars(self, split, length):
    if len(split)==length+1:
      split.pop(0) # pop off the command
      return split
    else:
      self.handleBadData('\t'.join(split))
      return False

  def handleData(self,data):
    try:
      data=data if type(data) is str else data.decode('utf-8')
      parts = data.split('\t')
      if parts[0] == 'ping': #Format: ping <user> <pass>
        if self.verifyVars(parts, 2):
          self.ping(parts[0], parts[1])
      elif parts[0] == 'set': #Format set <user> <pass> <setting> <value>
        if self.verifyVars(parts, 4):
          self.setSettings(parts[0], parts[1], parts[2], parts[3])
    except Exception as e:
      print("Exception occured while handling data: %s"%e)
      print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data))
    #add "it's dangerous" package for signature

  def handleBadData(self, data):
    print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data.decode('utf-8')))

  def ping(self, user, pwd):
    user, valid = self.verifyUser(user,pwd)
    if valid:
      db.updatePing(user)
      print("user %s is alive!"%user.email)
      self.reply('accepted User updated')
    else:
      self.reply('rejected User does not exist')

  def setSettings(self, user, pwd, setting, value):
    user, valid = self.verifyUser(user,pwd)
    if valid:
      if setting   == 'pwd':user.password = value
      elif setting == 'det':user.defaultExtension = value
      elif setting == 'dwt':user.defaultWarnTime = value
      else: self.handleBadData('\t'.join(['set', user, pwd, setting,
                                value]))
      db.updateUser(user)
      self.reply('accepted Setting has been set')
    else:
      self.reply('rejected User does not exist')

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


