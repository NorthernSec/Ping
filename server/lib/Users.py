#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Admin creator script
#
# Creates an admin account in the database
# Only master accounts are allowed to add and remove users
# First account registered is the master account
#
# Software is free software released under the "Modified BSD license"
#
# Copyright (c) 2015 		Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Imports
import os
runPath = os.path.dirname(os.path.realpath(__file__))

from flask.ext.login import UserMixin

import lib.DatabaseConnection as db

# Exception
class UserNotFoundError(Exception):
    pass

# Class
class User(UserMixin):
  '''Simple User class'''
  USERS = {}
  for user in db.getUsers():
    USERS[user.email] = user

  def __init__(self, id):
    if not id in self.USERS:
      raise UserNotFoundError()
    self.id = id
    self.user = self.USERS[id]

  @classmethod
  def get(self_class, id):
    '''Return user instance of id, return None if not exist'''
    try:
      return self_class(id)
    except UserNotFoundError:
      return None
