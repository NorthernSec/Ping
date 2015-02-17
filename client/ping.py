#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Ping Client
# Connects to Ping server to reset the death counter. It also allows to
# set some specific settings.

# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import sys

import socket
import argparse

description='''Connects and interacts with the Ping server. '''

parser = argparse.ArgumentParser(description=description)
parser.add_argument('--set-server-address', metavar='address[:port]', type=str, help='Sets the Ping server address to connect to and writes it to the config file. Optionally you can specify a non-default port' )
parser.add_argument('--set-user-name', metavar='username', type=str, help='Sets your username and writes it to the config file' )
args = parser.parse_args()





if __name__ == '__main__':

  #if args.set-server-address: print(args.set-server-address)
  #elif args.set-user-name:    print(args.set-user-name)

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  addr = ('localhost', 10000)
  print ('connecting to %s port %s' % addr)
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
