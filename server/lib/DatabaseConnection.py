#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Database layer

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import platform
import sqlite3

from lib.User import User
from lib.Exceptions import InvalidVarType, UserAlreadyExists
from lib.Configuration import Configuration as conf

# Functions
def getConnection():
  conn=sqlite3.connect(conf.getDatabase())
  conn.execute('''CREATE TABLE IF NOT EXISTS Users
                 (ID                INTEGER  PRIMARY KEY AUTOINCREMENT,
                  email             TEXT     NOT NULL,
                  password          TEXT     NOT NULL,
                  joinTime          INTEGER  NOT NULL,
                  defaultExtension  INTEGER  NOT NULL,
                  defaultWarnTime   INTEGER  NOT NULL,
                  lastPing          INTEGER  NOT NULL,
                  warnDate          INTEGER  NOT NULL,
                  deathDate         INTEGER  NOT NULL );''')
  return conn

def addUser(user):
  if type(user)!=User: raise(InvalidVarType)
  if getUser(user.email): raise(UserAlreadyExists)
  conn=getConnection()
  curs=conn.cursor()
  curs.execute('''INSERT INTO Users
                  (email, password, joinTime, defaultExtension, defaultWarnTime,
                   lastPing, warnDate, deathDate)
                  VALUES(:e,:p,:jt,:de,:dw,:lp,:wd,:dd)''',
                  {'e':user.email, 'p':user.password, 'jt':user.joinTime,
                   'de':user.defaultExtension, 'dw':user.defaultWarnTime,
                   'lp':user.lastPing, 'wd':user.warnDate, 'dd':user.deathDate})
  conn.commit()
  conn.close()
  return True

def getUser(email):
  u=selectAllFrom("Users", ["email='%s'"%email])
  if len(u)!=0:
    u=u[0]
    return User(u["email"], u["password"], u["jointime"], u["defaultextension"],
                u["defaultwarntime"], u["lastping"], u["warndate"], u["deathdate"])
  else:
    return None

def selectAllFrom(table, where=None):
  conn=getConnection()
  curs=conn.cursor()
  wh="where "+" and ".join(where) if where else ""
  data=list(curs.execute("SELECT * FROM %s %s;"%(table,wh)))
  dataArray=[]
  names = list(map(lambda x: x[0], curs.description))
  for d in data:
    j={}
    for i in range(0,len(names)):
      j[names[i].lower()]=d[i]
    dataArray.append(j)
  conn.close()
  return dataArray

