#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# User Object

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import os
import sys
_runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_runPath, ".."))

import calendar
import time

from passlib.hash import pbkdf2_sha256

from lib.Exceptions import InvalidVarType
from lib.Configuration import Configuration as conf

# Constants
DAY_MULTIPLIER=60*60*24

class User():
  def __init__(self, email, pwd, joinTime=None, defaultExtension=None,
               defaultWarnTime= None, lastPing=None, warnDate=None,
               deathDate=None):
    self.validateVars(email, pwd, joinTime, defaultExtension,
                      defaultWarnTime,  lastPing, warnDate, deathDate)
    self.email=email
    self.password=pwd
    if not joinTime: self.newUser()
    else:
      self.joinTime=joinTime
      self.defaultExtension=defaultExtension
      self.defaultWarnTime=defaultWarnTime
      self.lastPing=lastPing
      self.warnDate=warnDate
      self.deathDate=deathDate

  def validateVars(self, e, p, jt, de, dw, lp, wd, dd):
    if( not all(isinstance(x,str) for x in [e, p]) or
    (type(jt) is not int and jt is not None) or
    (type(de) is not int and de is not None) or
    (type(dw) is not int and dw is not None) or
    (type(lp) is not int and lp is not None) or
    (type(wd) is not int and wd is not None) or
    (type(dd) is not int and dd is not None)):
      raise(InvalidVarType)

  def newUser(self):
    self.defaultExtension=conf.getDefaultExtension()
    self.defaultWarnTime=conf.getDefaultWarnTime()
    self.ping()
    self.joinTime=self.lastPing

  def ping(self):
    self.lastPing=calendar.timegm(time.gmtime())
    self.warnDate=self.lastPing+(self.defaultWarnTime*DAY_MULTIPLIER)
    self.deathDate=self.lastPing+(self.defaultExtension*DAY_MULTIPLIER)

  def verifyPassword(self, pwd):
    return pbkdf2_sha256.verify(pwd, self.password)

