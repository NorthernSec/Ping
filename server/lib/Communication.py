#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# Contains all communication bots
#
# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports

#import irc.bot
#import irc.strings
import os
import sleekxmpp
import smtplib
import sys

runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from lib.Action import Action
from lib.Configuration import Configuration as conf
from lib.Exceptions import NoCredentials, InvalidVarType

# Classes
class XMPPBot(sleekxmpp.ClientXMPP):
  def __init__(self, jid, password):
    jid, password = conf.getXMPPCredentials()
    if not jid or not password: raise(NoCredentials)
    sleekxmpp.ClientXMPP.__init__(self, jid, password)
    self.use_ipv6 = True
    self.message=db.getXMPPMessage()
    self.add_event_handler("session_start", self.start)
    self.add_event_handler("ssl_invalid_cert", self.ssl_invalid_cert)
    self.register_plugin('xep_0030')  # Service Discovery
    self.register_plugin('xep_0004')  # Data Forms
    self.register_plugin('xep_0060')  # PubSub
    self.register_plugin('xep_0199')  # XMPP Ping

  def ssl_invalid_cert(self, cert):
    return

  def start(self, event):
    self.send_presence()
    self.get_roster()

  def act(self, action):
    if type(action) is not Action: raise(InvalidVarType)
    for target in action.target.split(","):
      user=action.username if action.username else action.user.email
      message=self.message.replace("%user%", user)
      if action.message: message=message+"\n\nPersonal message:\n"+action.message
      self.send_message(target.strip(), message)


#class IRCBot(irc.bot.SingleServerIRCBot):
#  def __init__(self, nickname, server, port, password=None, username=None):
#    irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
#    self.joined=[]

#  def on_nicknameinuse(self, c, e):
#    c.nick(c.get_nickname() + "_")

#  def act(self, action):
#    chans = action.target.split(",")
#    chans.pop(0) # pop off server
#    # Todo send messages (check syntax)


class MailBot():
  def __init__(self):
    self.serverCreds = conf.getMailServer()
    if not self.serverCreds[0]: raise(NoCredentials)
    self.email, self.pwd = conf.getMailCredentials()
    if not self.email: raise(NoCredentials)
    self.server=None
    self.message=conf.getMailMessage()
    if not self.message: raise(NoMessage)

  def login(self):
    self.server=smtplib.SMTP('%s:%s'%(self.serverCreds))
    self.server.starttls()
    self.server.login(self.email, self.pwd)

  def logout(self):
    self.server.quit()

  def sendMail(self, recipient, body, subject=None):
    if type(body) is not str or type(recipient) is not str: raise(InvalidVarType)
    if subject:
      if type(subject) is not str: raise(InvalidVarType)
      body="Subject: %s\n\n%s"%(subject, body)
    self.server.sendmail(self.email, recipient, body)

  def act(self, action):
    if type(action) is not Action: raise(InvalidVarType)
    for target in action.target.split(","):
      user=action.username if action.username else action.user.email
      message=self.message.replace("%user%", user)
      if action.message: message=message+"\n\nPersonal message:\n"+action.message
      self.sendMail(target.strip(), message)
