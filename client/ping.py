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
from Config import Config

description='''Connects and interacts with the Ping server. '''

parser = argparse.ArgumentParser(description=description)
parser.add_argument('--set-server-address', metavar='address[:port]', type=str, help='Sets the Ping server address to connect to and writes it to the config file. Optionally you can specify a non-default port' )
parser.add_argument('--set-user-name', metavar='username', type=str, help='Sets your username and writes it to the config file' )
parser.add_argument('--set-user-pass', metavar='password', type=str, help='Sets your password and writes it to the config file' )
args = parser.parse_args()

def printResult(setting, outcome):
  if outcome:
    print(">> Set %s"%(setting))
  else:
    print("[!] Could not set %s"%(setting))

if __name__ == '__main__':
  # setting vars
  if args.set_server_address:
    a=args.set_server_address.split(':')
    printResult('server host', Config.setHost(a[0]))
    if len(a)>1:
      printResult('server port', Config.setPort(a[1]))
  elif args.set_user_name:
    printResult('user-name', Config.setHost(args.set_user_name))
  elif args.set_user_pass:
    # encryption to be added
    printResult('user-pass', Config.setPass(args.set_user_pass))
  # start client
  else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = Config.getHost() if Config.getHost() else sys.exit('[!] No hostname set!')
    addr = (host, Config.getPort())
    print ('Connecting to %s port %s' % addr)
    sock.connect(addr)
    try:
      message = 'Ping test message'.encode('utf-8')
      print ('Sending "%s"' % message)
      sock.sendall(message)
      while True:
        data = sock.recv(2048)
        print ('Received "%s"' % data.decode('utf-8'))
    finally:
      print('Closing socket')
      sock.close()
