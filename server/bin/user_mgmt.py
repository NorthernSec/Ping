#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# User management tool

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

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
from lib.Exceptions import UserAlreadyExists
import lib.DatabaseConnection as db

# args
argParser = argparse.ArgumentParser(description='Management tool for the database')
argParser.add_argument('-a', help='<name> Add an account', default=False)
argParser.add_argument('-c', help='Change the password of an account', default=None)
argParser.add_argument('-r', help='Remove account', default=False)
args = argParser.parse_args()

# vars
col = "mgmt_users"
rounds = 8000
saltLength = 10
exits = {'userInDb': 'User already exists in database',
         'userNotInDb': 'User does not exist in database',
         'passwordMatch': "The passwords don't match!"}

# functions
def promptNewPass():
  password = getpass.getpass("New password:")
  verify = getpass.getpass("Verify password:")
  if (password != verify):
    sys.exit(exits['passwordMatch'])
  return pbkdf2_sha256.encrypt(password, rounds=rounds, salt_size=saltLength)

def addUser(email, password):
  return db.addUser(User(email, password))

if __name__ == "__main__":
  if args.a:
    try:
      pwd=promptNewPass()
      addUser(args.a, pwd)
    except UserAlreadyExists:
      print("User already exists in DB")
  elif args.c:
    print("To be implemented")
  elif args.r:
    print("To be implemented")
  else:
    sys.exit(0)
