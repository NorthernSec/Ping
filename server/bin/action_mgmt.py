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
from lib.User import User
from lib.Exceptions import ActionAlreadyExists
import lib.DatabaseConnection as db

# args
argParser = argparse.ArgumentParser(description='Management tool for the database')
argParser.add_argument('-a', help='Add action for user', default=False)
args = argParser.parse_args()

if __name__ == "__main__":
  if args.a:
    try:
      # verify user args.a
      # Ask action
      # if action.lower()=="irc":
        # Ask server
        # Ask Channel or user
      # elif action.lower()=="xmpp":
        # Ask user
      # elif action.lower()=="mail":
        # Ask user
      # Ask username of person to speak for (leave blank for email)
      # Ask for short personal message
      # Add user
    except ActionAlreadyExists:
      print("Action already exists in DB")
  elif args.c:
    print("To be implemented")
  elif args.r:
    print("To be implemented")
  else:
    sys.exit(0)

