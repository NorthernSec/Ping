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
from lib.Action import Action
from lib.Exceptions import *

class ClientThread(threading.Thread):
  def __init__(self,ip,port,clientsocket):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.csocket = clientsocket
    self.statusCode = {
      # 100 range: failed user commands
      'invalidUser':         '100',
      'markedDead':          '110',
      # 200 range: success
      'pingOK':              '200',
      'settingSet':          '210',
      'extensionSet':        '220',
      'actionAdded':         '230',
      # 300 range: bad input
      'unknownSetting':      '310',
      'invalidAction':       '321',
      'invalidTarget':       '322',
      # 400 range: action refused
      'tooManyActions':      '431',
      'actionAlreadyExists': '432'}

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
      if not data: return
      data=data if type(data) is str else data.decode('utf-8')
      p=data.split('\t')
      if p[0] == 'ping': #Format: ping <user> <pass>
        if self.verifyVars(p, 2):
          self.ping(p[0], p[1])
      elif p[0] == 'set': #Format set <user> <pass> <setting> <value>
        if self.verifyVars(p, 4):
          self.setSettings(p[0], p[1], p[2], p[3])
      elif p[0] == "extend": #Format extend <user> <pass> <days>
        if self.verrifyVars(p, 3):
          self.extendTTL(p[0], p[1], p[2])
      elif p[0] == "add-action": #Format add-action <user> <pass> <action> <target> <username> <message>
        if self.verifyVars(p, 6):
          self.addAction(p[0], p[1], p[2], p[3], p[4], p[5])
      else:
        self.handleBadData('\t'.join(p))
    except Exception as e:
      print("Exception occured while handling data: %s"%e)
      self.handleBadData(data)
    #add "it's dangerous" package for signature

  def handleBadData(self, data):
    print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data))

  def ping(self, user, pwd):
    valid, user = self.isValidUser(user, pwd)
    if valid:
      db.updatePing(user)
      self.reply(self.statusCode['pingOK'])

  def setSettings(self, user, pwd, setting, value):
    user, valid = self.isValidUser(user,pwd)
    if valid:
      if setting   == 'pwd':user.password = value
      elif setting == 'det':user.defaultExtension = value
      elif setting == 'dwt':user.defaultWarnTime = value
      else: 
        self.handleBadData('\t'.join(['set', user, pwd, setting, value]))
        self.reply(self.statusCode['unknownSetting'])
      db.updateUser(user)
      self.reply(self.statusCode['settingSet'])

  def extendTTL(self, user, pwd, days):
    user, valid = self.isValidUser(user,pwd)
    if valid:
      user.extend(days)
      db.extendTTL(user)
      self.reply(self.statusCode['extensionSet'])

  def addAction(self, user, pwd, act, target, name, message):
    user, valid = self.isValidUser(user,pwd)
    if valid:
      name   =name    if name    else None
      message=message if message else None
      try:
        action=Action(user, act, target, name, message)
        db.addAction(action)
        self.reply(self.statusCode['actionAdded'])
      except TooManyActions:
        self.reply(self.statusCode['tooManyActions'])
      except ActionAlreadyExists:
        self.reply(self.statusCode['actionAlreadyExists'])
      except InvalidAction:
        self.reply(self.statusCode['invalidAction'])
      except InvalidTarget:
        self.reply(self.statusCode['invalidTarget'])

  def verifyUser(self,user,passwd):
    u=db.getUser(user)
    return (u[1], u[1].verifyPassword(passwd)) if u[0] else (None, False)

  def isValidUser(self, user, passwd):
    u, valid = self.verifyUser(user, passwd)
    if not valid:
      self.reply(self.statusCode['invalidUser']); return (False, u)
    if not u or u.deathDate == -1  :
      self.reply(self.statusCode['markedDead']);  return (False, u)
    return (True, u)

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


