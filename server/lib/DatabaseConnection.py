#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Database layer

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import calendar
import platform
import sqlite3
import time

from lib.Action import Action
from lib.User import User
from lib.Exceptions import *
from lib.Configuration import Configuration as conf
from lib.Toolkit import userFromDict, actionFromDict

# Decorators
def dbOperand(func):
  def func_wrapper(*args, **kwargs):
    conn, cur=getConnection()
    result = func(conn, cur, *args, **kwargs)
    conn.close()
    return result
  return func_wrapper
def tmpdbOperand(func):
  def func_wrapper(*args, **kwargs):
    conn, cur=getConnection()
    result = func(conn, cur, *args, **kwargs)
    conn.close()
    return result
  return func_wrapper

# Functions
def getConnection():
  conn=sqlite3.connect(conf.getDatabase())
  conn.execute('''CREATE TABLE IF NOT EXISTS Users
                 (ID                INTEGER  PRIMARY KEY AUTOINCREMENT,
                  email             TEXT     NOT NULL    UNIQUE,
                  password          TEXT     NOT NULL,
                  joinTime          INTEGER  NOT NULL,
                  defaultExtension  INTEGER  NOT NULL,
                  defaultWarnTime   INTEGER  NOT NULL,
                  lastPing          INTEGER  NOT NULL,
                  warnDate          INTEGER  NOT NULL,
                  deathDate         INTEGER  NOT NULL );''')
  conn.execute('''CREATE TABLE IF NOT EXISTS Actions
                 (ID        INTEGER  PRIMARY KEY AUTOINCREMENT,
                  userID    INTEGER  NOT NULL,
                  action    TEXT     NOT NULL,
                  target    TEXT     NOT NULL,
                  username  TEXT             ,
                  message   TEXT             ,
                  attempts  INTEGER  DEFAULT 0 );''')

  return (conn, conn.cursor())

def getConnectionTemp():
  conn=sqlite3.connect(conf.getTempDatabase())
  conn.execute('''CREATE TABLE IF NOT EXISTS Tokens
                  (email  TEXT     PRIMARY KEY,
                   token  TEXT     NOT NULL,
                   time   INTEGER  NOT NULL);'''
  return conn

################
# Long term DB #
################

# Adding data
@dbOperand
def addUser(conn, curs, user):
  if type(user)!=User: raise(InvalidVarType)
  if getUser(user.email): raise(UserAlreadyExists)
  curs.execute('''INSERT INTO Users
                  (email, password, joinTime, defaultExtension, defaultWarnTime,
                   lastPing, warnDate, deathDate)
                  VALUES(:e,:p,:jt,:de,:dw,:lp,:wd,:dd)''',
                  {'e':user.email, 'p':user.password, 'jt':user.joinTime,
                   'de':user.defaultExtension, 'dw':user.defaultWarnTime,
                   'lp':user.lastPing, 'wd':user.warnDate, 'dd':user.deathDate})
  conn.commit()
  return True

@dbOperand
def addAction(conn, curs, action):
  if type(action)!=Action: raise(InvalidVarType)
  current=getActions(action.user)
  if len(current)>=conf.getMaxActions(): raise(TooManyActions)
  if True in [action.isSimilar(x) for x in current]:
   raise(ActionAlreadyExists)
  u = getUser(action.user.email)
  if not u[0]: raise(UserDoesNotExist())
  a = action # purely to shorten the code below
  curs.execute('''INSERT INTO Actions
                  (userID, action, target, username, message)
                  VALUES(:uid, :act, :targ, :uname, :mes)''',
                  {'uid': u[0], 'act': a.action, 'targ':a.target,
                   'uname': a.username, 'mes':a.message})
  conn.commit()
  return True

# Modifying data
def updatePing(user):
  if type(user)!=User: raise(InvalidVarType)
  user.ping()
  extendTTL(user)

@dbOperand
def extendTTL(conn, curs, user):
  if type(user)!=User: raise(InvalidVarType)
  curs.execute("""UPDATE Users SET lastPing=?, warnDate=?, deathDate=?
                  WHERE email=?""", (user.lastPing, user.warnDate, user.deathDate,
                                     user.email))
  conn.commit()
  return True

@dbOperand
def updateUser(conn, curs, user):
  curs.execute("""UPDATE Users SET password=?, defaultExtension=?,
                    defaultWarnTime=?
                  WHERE email=?""", (user.password, user.defaultExtension,
                                     user.defaultWarnTime, user.email))
  conn.commit()
  return True

@dbOperand
def markDead(conn, curs, user):
  if type(user)!=User: raise(InvalidVarType)
  curs.execute("""UPDATE Users SET deathDate=-1
                  WHERE email=?""", (user.email,))
  conn.commit()
  return True

@dbOperand
def markFailed(conn, curs, action):
  if type(actions)!=Action: raise(InvalidVarType)
  if not action.id: return False
  curs.execute("""UPDATE ACTIONS SET attempts=?
                  WHERE id=?""", (action.attempts+1, actions.id))
  conn.commit()
  return True

@dbOperand
def markCompleted(conn, curs, action):
  if type(actions)!=Action: raise(InvalidVarType)
  if not action.id: return False
  curs.execute("""UPDATE ACTIONS SET attempts=-1
                  WHERE id=?""", (actions.id,))
  conn.commit()
  return True

# Querying data
def getUsers():
  users=[]
  for user in selectAllFromDB("Users"):
    users.append(userFromDict(user))
  return users

def getUser(email):
  u=selectAllFromDB("Users", "email='%s'"%email)
  if len(u)!=0:
    u=u[0]
    return (u['id'], userFromDict(u))
  else:
    return (None, None)

def getActions(user):
  if type(user)!=User: raise(InvalidVarType)
  id, user=getUser(user.email)
  if not id: return None
  actions=[]
  for a in selectAllFromDB("Actions", where="userID = %s"%id):
    actions.append(actionFromDict(user, a))
  return actions

def getActionsToDo():
  actions=[]
  wh=["attempts > 0", "attempts < %s"%conf.getMaxAttempts()]
  for a in selectAllFromDB("Actions", where=wh):
    actions.append(actionFromDict(a))
  return actions

def getDeaths():
  users=[]
  for u in selectAllFromDB("Users", where="deathDate = -1"):
    users.append(userFromDict(u))
  return users

def getNewDeaths():
  users=[]
  now=calendar.timegm(time.gmtime())
  wh=["deathDate < %s"%now, "deathDate != -1"]
  for u in selectAllFromDB("Users", where = wh):
    users.append(userFromDict(u))
  return users

###########
# Temp DB #
###########

# Adding data
@tmpOperand
def addToken(conn, curs, email, token):
  now=calendar.timegm(time.gmtime())
  curs.execute('''INSERT INTO Tokens(email, token, time)
                  VALUES(:e,:t,:n)''',{'e':email, 't':token, 'n': now})
  conn.commit()

@tmpOperand
def getToken(conn, curs, email):
  t=selectAllFromDB("Users", "email='%s'"%email)
  return t[0] if len(t)!=0 else None

@tmpOperand
def removeToken(conn, curs, email):
  print("to-do")

@dbOperand
def selectAllFromDB(conn, curs, table, where=None):
  return selectAllFrom(conn, curs, table, where)

@tmpdbOperand
def selectAllFromTMPDB(conn, curs, table, where=None):
  return selectAllFrom(conn, curs, table, where)

def selectAllFrom(conn, curs, table, where=None):
  if type(where) is str: where = [where]
  wh="where "+" and ".join(where) if where else ""
  data=list(curs.execute("SELECT * FROM %s %s;"%(table,wh)))
  dataArray=[]
  names = list(map(lambda x: x[0], curs.description))
  for d in data:
    j={}
    for i in range(0,len(names)):
      j[names[i].lower()]=d[i]
    dataArray.append(j)
  return dataArray

