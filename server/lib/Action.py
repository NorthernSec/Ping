#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Action Object

# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import os
import sys
_runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_runPath, ".."))

import calendar
import time

from passlib.hash import pbkdf2_sha256

from lib.User import User
from lib.Exceptions import InvalidVarType
from lib.Configuration import Configuration as conf

class Action():
  def __init__(self, user, action, target, username=None, message=None,
               attempts=0, id=None):
    self.validateVars(user, action, target, username, message,
                      attempts, id)
    self.user=user
    self.action=action.strip()
    self.target=target.strip()
    self.username=username.strip() if username else None
    self.message=message.strip()   if message  else None
    self.atttempts=attempts
    self.id=id

  def validateVars(self, u, a, t, un, m, at, id):
    if( not all(isinstance(x,str) for x in [a, t]) or
    (type(u)  is not User) or
    (type(un) is not str and un is not None) or
    (type(m)  is not str and m  is not None) or
    (type(at) is not int) or
    (type(id) is not int and id is not None)): raise(InvalidVarType)
    if a.strip() not in ['irc', 'xmpp', 'mail']:
      raise(InvalidAction)
    # check if target patterns are correct
    if a.strip()=='irc':
      print("xxx.xxx.xxx[:port],(#)user or chan separated by , but no trailing ,")
    elif a.strip()=='xmpp':
      print("xxx@xxx.xxx[,xxx@xxx.xxx]*")
    elif a.strip()=='mail':
      print("same as xmpp")
    # Throws InvalidTarget if fails

  def isSimilar(self, action):
    if (action.user.email == self.user.email and
        action.action     == self.action and
        action.target     == self.target): return True
    return False
