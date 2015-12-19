#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# Actor that takes a list of actions and executes them
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

#import irc.bot
#import irc.strings
import sleekxmpp

from lib.Action import Action
from lib.Configuration import Configuration as conf
from lib.Exceptions import InvalidVarType

class Actor():
  def __init__(self):
    self._queue={'xmpp':[],
                 'irc': {},
                 'mail':[]}

  def queue(self, actions):
    if type(actions) is not list: actions=[actions]
    if not all(isinstance(x,Action) for x in actions): raise(InvalidVarType)
    for act in actions:
      if   act.action == "xmpp":
        self._queue['xmpp'].append(act)
      elif act.action == "irc":
        server=act.target.split(",")[0]
        if server in self._queue['irc'].keys():
          self._queue['irc'][server].append(act)
        else:
          self._queue['irc'][server] = [act]
      elif act.action == "mail":
        self._queue['mail'].append(act)

  def actOnQueue(self):
    closureQueue = []
    failedQueue = []
    # empty XMPP queue
    if len(self._queue['xmpp']) != 0:
      jid, jpass = conf.getXMPPCredentials()
      if jid:
        xmpp = XMPPBot(jid, jpass)
        if xmpp.connect():
          xmpp.process()
          for act in self._queue['xmpp']:
            if xmpp.act(act):
              closureQueue.append(act)
            else:
              failedQueue.append(act)
            self._queue['xmpp'].pop(act)
    # empty IRC queue
    nick=conf.getIRCcredentials()
    for server in self._queue['irc'].keys():
      split=server.split(":")
      if len(split) == 2: server, port = split
      else:               server, port = [server, 6667]
      bot=IRCBot(nick, server, port)
      bot.start()
      for act in self._queue['irc'][server]:
        if bot.act(act):
          closureQueue.append(act)
        else:
          failedQueue.append(act)
      bot.die()
      self._queue['irc'].pop(server)
    # empty mail queue
    # TODO
    return (closureQueue, failedQueue)

class XMPPBot(sleekxmpp.ClientXMPP):
  def __init__(self, jid, password):
    sleekxmpp.ClientXMPP.__init__(self, jid, password)
    self.use_ipv6 = True
    self.message=db.getXMPPDefaultMessage()
    self.add_event_handler("session_start", self.start)
    self.add_event_handler("ssl_invalid_cert", self.ssl_invalid_cert)
    self.register_plugin('xep_0030')  # Service Discovery
    self.register_plugin('xep_0004')  # Data Forms
    self.register_plugin('xep_0060')  # PubSub
    self.register_plugin('xep_0199')  # XMPP Ping

  def ssl_invalid_cert(self, cert):
    return

  def start(self, event):
    self.send_presence()
    self.get_roster()

  def act(action):
    if type(action) is not Action: raise(InvalidVarType)
    for target in action.target.split(","):
      user=action.username if action.username else action.user.email
      message=self.message
      message.replace("%user%", user)
      if action.message: message=message+"\n"+action.message
      self.send_message(target.strip(), message)

#class IRCBot(irc.bot.SingleServerIRCBot):
#  def __init__(self, nickname, server, port, password=None, username=None):
#    irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
#    self.joined=[]

#  def on_nicknameinuse(self, c, e):
#    c.nick(c.get_nickname() + "_")

#  def act(self, action):
#    chans = action.target.split(",")
#    chans.pop(0) # pop off server
#    # Todo send messages (check syntax)
