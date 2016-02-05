#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Validations

# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import re

def isEmail(email):
  mailreg=re.compile("^[_.0-9a-z-]+@([0-9a-z][0-9a-z]+.)+[a-z]{2,4}$")
  return True if mailreg.match(mail.lower()) else False

def isXMPP(xmpp):
  xmppreg=re.compile("^[_.0-9a-z-]+@([0-9a-z][0-9a-z]+.)+[a-z]{2,4}$")
  return True if xmppreg.match(xmpp.lower()) else False

def getIRC(string):
  users=[x for x in string.split(",")[1:]]
  domain = string.split(",")[0]
  port = 6667
  if ":" in domain:
    try:
      port = int(domain.split(":")[0])
    except:
      pass
  ircreg=re.compile("^[_.0-9a-z-]+.([0-9a-z][0-9a-z]+.)+[a-z]{2,4}$")
  if ircreg.match(domain.lower()):
    return(domain, port, users)
  else:
    return (None, None, None)
