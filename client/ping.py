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
args = parser.parse_args()

def printResult(setting, outcome):
  if outcome:
    print(">> Set %s"%(setting))
  else:
    print("[!] Could not set %s"%(setting))

def sendMessage(message):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = conf.getHost() if conf.getHost() else sys.exit('[!] No hostname set!')
  addr = (host, conf.getPort())
  print ('Connecting to %s port %s' % addr)
  sock.connect(addr)
  try:
    message = message.encode('utf-8')
    print ('Sending "%s"' % message)
    sock.sendall(message)
    while True:
      data = sock.recv(2048)
      print ('Received "%s"' % data.decode('utf-8'))
      if data.decode('utf-8').startswith('accepted'):
        print('Request accepted')
      if data.decode('utf-8').startswith('rejected'):
        print('Request rejected')
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
  else:
    sendMessage('ping\t%s\t%s'%(conf.getUser(),conf.getPass()))
