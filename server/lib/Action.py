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
    self.action=action
    self.target=target
    self.username=username
    self.message=message
    self.atttempts=attempts

  def validateVars(self, u, a, t, un, m, at, id):
    if( not all(isinstance(x,str) for x in [a, t]) or
    (type(u)  is not User) or
    (type(un) is not str and un is not None) or
    (type(m)  is not str and m  is not None) or
    (type(at) is not int) or
    (type(id) is not int and id is not None)): raise(InvalidVarType)

