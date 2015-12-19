#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Ping Client
# Connects to Ping server to reset the death counter. It also allows to
# set some specific settings.

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import sys

from passlib.hash import pbkdf2_sha256

import socket
import argparse
from Config import Config as conf

description='''Connects and interacts with the Ping server. '''

parser = argparse.ArgumentParser(description=description)
parser.add_argument('--set-server-address', metavar='address[:port]', type=str, help='Sets the Ping server address to connect to and writes it to the config file. Optionally you can specify a non-default port' )
parser.add_argument('--set-user-name', metavar='username', type=str, help='Sets your username and writes it to the config file' )
parser.add_argument('--set-user-pass', metavar='password', type=str, help='Sets your password and writes it to the config file' )
parser.add_argument('--extend-ttl', metavar='days', type=int, help='Extends the death clock with set amount of days' )
parser.add_argument('--set-def-ttl', metavar='days', type=int, help='Sets the default life of a ping messageto the server' )
parser.add_argument('--add-action', action='store_true', help='Add an action to be taken on death')
parser.add_argument('-v', action='store_true', help='Verbose')
args = parser.parse_args()

MESSAGES={'100': "Invalid user or password",
          '200': "Successfully pinged",
          '210': "Successfully set setting",
          '220': "Successfully extended TTL",
          '230': "Successfully added action",
          '431': "You already have too many actions",
          '432': "This action already exists"}
UNKNOWN_SERVER_RESPONSE="Got an unknown server response"

def _log(line, force=False):
  if args.v or force:
    print(line)

def printResult(setting, outcome):
  if outcome:
    print(">> Set %s"%(setting))
  else:
    print("[!] Could not set %s"%(setting))

def addAction():
  action=(input("Channel for message (irc/xmpp/mail): ")).lower().strip()
  if action=="irc":
    server=(input("What server? '<server>[:<port>]': ")).lower().strip()
    chans=(input("#<channel> or <user>, separated by a space: ")).lower()
    chans=",".join(chans.split())
    target="%s,%s"%(server,chans)
  elif action=="xmpp":
    target=input("list of users, separated by a space: ").lower()
    target=",".join(target.split())
  elif action=="mail":
    target=input("list of emails, separated by a space: ").lower()
    target=",".join(target.split())
  else:
    sys.exit("unknown action")
  username=input("Name to display in message (blank for e-mail)").strip()
  message=input("Short personalized message (blank for none)").strip()
  sendMessage("\t".join(["add-action", conf.getUser(), conf.getPass(),
              action, target, username, message]))

def sendMessage(message):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = conf.getHost() if conf.getHost() else sys.exit('[!] No hostname set!')
  addr = (host, conf.getPort())
  _log('Connecting to %s port %s' % addr)
  sock.connect(addr)
  try:
    message = message.encode('utf-8')
    _log('Sending "%s"' % message)
    sock.sendall(message)
    while True:
      orig = sock.recv(2048)
      data=orig.decode('utf-8')
      data=data.strip()
      try:
        _log('Received "%s"' % orig.decode('utf-8'))
        message=MESSAGES[data.split()[0]]
        if len(data.split())>1:
          message+=" %s"%" ".join(data.split()[1:])
        show = True if data.startswith("2") else False
        _log(message, show)
      except Exception as e:
        print(e)
        print(UNKNOWN_SERVER_RESPONSE)
      break
  finally:
    sock.close()

if __name__ == '__main__':
  # setting vars
  if args.set_server_address:
    a=args.set_server_address.split(':')
    printResult('server host', conf.setHost(a[0]))
    if len(a)>1:
      printResult('server port', conf.setPort(a[1]))
  elif args.set_user_name:
    printResult('user-name', conf.setUser(args.set_user_name))
  elif args.set_user_pass:
    # encryption to be added
    printResult('user-pass', conf.setPass(args.set_user_pass))
  # message types
  elif args.set_def_ttl:
    sendMessage('set\t%s\t%s\tdet\t%s'%(conf.getUser(),conf.getPass(),
                                        args.set_ping_ttl))
  elif args.extend_ttl:
    sendMessage('extend\t%s\t%s\t%s'%(conf.getUser(),conf.getPass(),
                                        args.extend_ttl))
  elif args.add_action:
    addAction()
  else:
    sendMessage('ping\t%s\t%s'%(conf.getUser(),conf.getPass()))
