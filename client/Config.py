#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# Read configuration file or return default values

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import os
import sys
runpath=os.path.dirname(os.path.realpath(__file__))

import pymongo

import configparser

class Config():
  cp=configparser.ConfigParser()
  filePath='./conf.ini'
  cp.read(os.path.join(runpath, filePath))

  @classmethod
  def read(cls, section, item, type):
    result=None
    try:
      if type == bool:
        result=cls.cp.getboolean(section, item)
      elif type == int:
        result=cls.cp.getint(section, item)
      else:
        result=cls.cp.get(section,item)
    except:
      pass
    return result

  @classmethod
  def write(cls, section, item, value):
    try:
      if not os.path.exists(cls.filePath):
        open(cls.filePath, 'a').close()
      conf=open(cls.filePath,'w')
      if not cls.cp.has_section(section):
        cls.cp.add_section(section)
      cls.cp.set(section, item, value)
      cls.cp.write(conf)
      conf.close()
      return True
    except Exception as e:
      print(e)
      return False
    
  ### GETTERS ###

  # User
  @classmethod
  def getUser(cls):
    return cls.read('Default','User',str)
  @classmethod
  def getPass(cls):
    return cls.read('Default','Pass',str)

  # Connection
  @classmethod
  def getHost(cls):
    return cls.read('Default','Host',str)
  @classmethod
  def getPort(cls):
    p=cls.read('Default','Port',int)
    return 10000 if not p else p

  ### SETTERS ###

  # User
  @classmethod
  def setUser(cls, user):
    return cls.write('Default','User',user)
  @classmethod
  def setPass(cls, passwd):
    return cls.write('Default','Pass',passwd)

  # Connection
  @classmethod
  def setHost(cls, host):
    return cls.write('Default','Host',host)
  @classmethod
  def setPort(cls, port):
    return cls.write('Default','Port',port)
