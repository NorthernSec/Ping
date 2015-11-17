#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# Config reader to read the configuration file
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# imports
import sys
import os
runPath = os.path.dirname(os.path.realpath(__file__))

import configparser

class Configuration():
  ConfigParser = configparser.ConfigParser()
  ConfigParser.read(os.path.join(runPath, "../etc/configuration.ini"))
  default = {'defWarnTime': 5, 'defExtension': 7, 'dbPath': "db.sqlite"}

  @classmethod
  def readSetting(cls, section, item, default):
    result = default
    try:
      if type(default) == bool:
        result = cls.ConfigParser.getboolean(section, item)
      elif type(default) == int:
        result = cls.ConfigParser.getint(section, item)
      else:
        result = cls.ConfigParser.get(section, item)
    except:
      pass
    return result

  # Users
  @classmethod
  def getDefaultWarnTime(cls):
    return cls.readSetting("User", "defaultWarnTime", cls.default['defWarnTime'])
  @classmethod
  def getDefaultExtension(cls):
    return cls.readSetting("User", "defaultExtension", cls.default['defExtension'])
  @classmethod
  def getDatabase(cls):
    return os.path.join(runPath, "..", cls.readSetting("Database", "path", cls.default['dbPath']))

