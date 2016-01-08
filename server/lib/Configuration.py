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
  default = {'defWarnTime': 5, 'defExtension': 7, 'dbPath': "db.sqlite",
             'maxAttempts': 5, 'maxActions':5,
             'saltLength': 10, 'hashRounds': 8000,
             'jid': "", 'jpass': "", 'jmessage':"./messages/xmpp.msg",
             'irc': "DeathClock",  'ircmessage':"./messages/irc.msg",
             'mail': "", 'mailpass': "", 'mailmessage': "./messages/mail.msg",
             'mailserver': "", 'mailport': 587,
             'pingHost':  "127.0.0.1",                 'pingPort':  10000,               'pingDebug':  True,
             'flaskHost': "127.0.0.1",                 'flaskPort': 5060,                'flaskDebug': True,
             'sslCertificate': "./ssl/cve-search.crt", 'sslKey': "./ssl/cve-search.crt", 'ssl': False}

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
    return cls.readSetting("User", "default warn time", cls.default['defWarnTime'])
  @classmethod
  def getDefaultExtension(cls):
    return cls.readSetting("User", "default extension", cls.default['defExtension'])
  @classmethod
  def getDatabase(cls):
    return os.path.join(runPath, "..", cls.readSetting("Database", "path", cls.default['dbPath']))
  @classmethod
  def getSaltLength(cls):
    return cls.readSetting("User", "salt length", cls.default['saltLength'])
  @classmethod
  def getHashRounds(cls):
    return cls.readSetting("User", "hashing rounds", cls.default['hashRounds'])

 
  # Actions
  @classmethod
  def getXMPPCredentials(cls):
    jid=cls.readSetting("XMPP", "id", cls.default['jid'])
    jpass=cls.readSetting("XMPP", "pass", cls.default['jpass'])
    return (jid, jpass) if jid and jpass else (None, None)
  @classmethod
  def getXMPPMessage(cls):
    path=os.path.join(runPath, "..", cls.readSetting("XMPP", "message path", cls.default['jmessage']))
    try:
      return open(path, 'r').read()
    except:
      return None
  @classmethod
  def getMailCredentials(cls):
    mail=cls.readSetting("Mail", "email", cls.default['mail'])
    mpass=cls.readSetting("Mail", "pass", cls.default['mailpass'])
    return (mail, mpass) if mail and mpass else (None, None)
  @classmethod
  def getMailServer(cls):
    server=cls.readSetting("Mail", "server", cls.default['mailserver'])
    port=cls.readSetting("Mail", "port", cls.default['mailport'])
    return (server, port) if server else (None, None)
  @classmethod
  def getMailMessage(cls):
    path=os.path.join(runPath, "..", cls.readSetting("Mail", "message path", cls.default['mailmessage']))
    try:
      return open(path, 'r').read()
    except:
      return None
  @classmethod
  def getIRCcredentials(cls):
    return cls.readSetting("IRC", "username", cls.default['irc'])
  @classmethod
  def getIRCMessage(cls):
    path=os.path.join(runPath, "..", cls.readSetting("IRC", "message path", cls.default['mailmessage']))
    try:
      return open(path, 'r').read()
    except:
      return None
  @classmethod
  def getMaxAttempts(cls):
    return cls.readSetting("Actions", "max attempts", cls.default['maxAttempts'])
  @classmethod
  def getMaxActions(cls):
    return cls.readSetting("Actions", "max actions", cls.default['maxActions'])
  # Ping server
  @classmethod
  def getPingAddress(cls):
    host = cls.readSetting("Pingserver", "Host", cls.default['pingHost'])
    port = cls.readSetting("Pingserver", "Port", cls.default['pingPort'])
    return (host, port)
  @classmethod
  def getPingDebug(cls):
    return cls.readSetting("Pingserver", "Debug", cls.default['pingDebug'])
  # Flask
  @classmethod
  def getWebAddress(cls):
    host = cls.readSetting("Webserver", "Host", cls.default['flaskHost'])
    port = cls.readSetting("Webserver", "Port", cls.default['flaskPort'])
    return (host, port)
  @classmethod
  def getWebDebug(cls):
    return cls.readSetting("Webserver", "Debug", cls.default['flaskDebug'])
  # SSL
  @classmethod
  def useSSL(cls):
    return cls.readSetting("Webserver", "SSL", cls.default['ssl'])
  @classmethod
  def getSSLCert(cls):
    return os.path.join(runPath, "..", cls.readSetting("Webserver", "Certificate", cls.default['sslCertificate']))
  @classmethod
  def getSSLKey(cls):
    return os.path.join(runPath, "..", cls.readSetting("Webserver", "Key", cls.default['sslKey']))
