#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# General purpose functions

# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
from lib.Action import Action
from lib.User import User

def userFromDict(u):
  try:
    return User(u["email"], u["password"], u["jointime"],
                u["defaultextension"], u["defaultwarntime"],
                u["lastping"],u["warndate"], u["deathdate"])
  except:
    return None 

def actionFromDict(user, a):
  try:
    return Action(user, a["action"], a["target"], a["username"],
                  a["message"], a['attempts'], a['id'])
  except:
    return None
