#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Action management tool

# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

import argparse
import getpass
from passlib.hash import pbkdf2_sha256

from lib.Configuration import Configuration as conf
from lib.Action import Action
from lib.Exceptions import ActionAlreadyExists
import lib.DatabaseConnection as db

# args
argParser = argparse.ArgumentParser(description='Management tool for the database')
argParser.add_argument('-a', help='Add action for user', default=False)
args = argParser.parse_args()

if __name__ == "__main__":
  if args.a:
    try:
      id, user = db.getUser(args.a)
      if not id: sys.exit("User does not exist in db")
      action=input("Channel for message (irc/xmpp/mail): ")
      if action.lower()=="irc":
        server=input("What server? <server>[:[+]<port>]: (+ for ssl): ")
        chan=input("#<channel> or <user>, separated by ',': ")
        target="%s,%s"%(server,chan)
      elif action.lower()=="xmpp":
        target=input("list of users, separated by ',': ")
      elif action.lower()=="mail":
        target=input("list of emails, separated by ',': ")
      else:
        sys.exit("unknown action")
      username=input("Name to display in message (blank for e-mail)")
      username=username if username else None
      message=input("Short personalized message (blank for none)")
      message=message if message else None
      db.addAction(Action(user, action, target, username, message))
    except ActionAlreadyExists:
      print("Action already exists in DB")
  #elif args.c:
  #  print("To be implemented")
  #elif args.r:
  #  print("To be implemented")
  else:
    sys.exit(0)

