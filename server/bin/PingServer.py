#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Ping server
#   Listens to incomming connections of registered users to reset their
#   Death Clock.
#   When a persons Death Clock reaches zero, respective actions will be
#   taken. Basic actions are IRC connect, Tweet, Mail.

# Copyright (c) 2015	NorthernSec
# Copyright (c)	2015	Pieter-Jan Moreels

# Imports
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

sys.path.append(runPath)

import socket

from lib.ClientThread import ClientThread
from lib.Configuration import Configuration as conf

if __name__ == '__main__':
  # Start server
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  addr = conf.getPingAddress()
  print('Starting Ping on %s port %s' % addr)
  try:
    sock.bind(addr)
    sock.listen(1)
    while True:
      (cl_sock, (cl_ip, cl_port)) = sock.accept()
      thread=ClientThread(cl_ip, cl_port, cl_sock)
      thread.start()
  finally:
    sock.close()
