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

from lib.Action import Action
from lib.Communication import XMPPBot, MailBot
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
