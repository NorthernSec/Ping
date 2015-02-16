#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Ping server
# Listens to incomming connections of registered users to reset their Death Clock.
# When a persons Death Clock reaches zero, respective actions will be taken. Basic actions are IRC connect, Tweet, Mail.

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports

import socket
import sys

def handleConnection(conn, cl_addr):
  try:
    print('Connection from', client_address)
    while True:
      data = connection.recv(16)
      if data:
        handleData(data)
      else:
        break
  finally:
      connection.close()

def handleData(data):
  print('handles incomming data')

def ping(user,passwd,chk):
  print('handles ping')
  #add "it's dangerous" package for signature

def verifyUser(user,passwd):
  print('verifies user in db')
  # db struct: user name, hashed pass, join time, lastPing, default extension time, new death date, tresholds with actions
  # maybe document oriented db

if __name__ == '__main__':
  # Start server
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  addr = ('localhost', 10000)
  print('Starting Ping on %s port %s' % server_address)
  sock.bind(addr)
  sock.listen(1)
  while True:
    conn, cl_add = sock.accept()
    handleConnection(conn, cl_addr)
