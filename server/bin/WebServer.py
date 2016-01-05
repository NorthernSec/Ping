#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
#
# Ping Webserver
#   Web interface to the Death Clock.
#   Needed for registring and more complex tasks

# Copyright (c) 2015    NorthernSec
# Copyright (c) 2015    Pieter-Jan Moreels

# Imports
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask import Flask, render_template, request, redirect, jsonify
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug import secure_filename
import calendar
import random
import signal
import time

from lib.Configuration import Configuration as conf
from lib.Users import User

import lib.DatabaseConnection as db

# variables
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = str(random.getrandbits(256))

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.get(id)

# pages
@app.route('/')
def index():
  return render_template('index.html')


@app.route('/login', methods=['get'])
def login():
  if not current_user.is_authenticated():
    return render_template('login.html', status=["default", "none"])
  else:
    return redirect("/")

@app.route('/profile', methods=['get'])
@login_required
def profile():
  return render_template('profile.html', user=current_user)

@app.route('/login', methods=['post'])
def validate_login():
  # validate username and password
  username = request.form.get('username')
  password = request.form.get('password')
  person = User.get(username)
  if person and person.user.verifyPassword(password):
    login_user(person)
    return redirect('/profile')
  else:
    return render_template('login.html', status=["wrong_combination", "warning"])

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect("/")

# ajax
@app.route('/_change_pass')
def change_pass():
  old=items=request.args.get('password',        type=str)
  new=items=request.args.get('new_password',    type=str)
  person=current_user.user
  if not person.verifyPassword(old):
    return jsonify({"status": "no match"})
  else:
    try:
      person.setPassword(new)
      person.ping() #If a user can change his password, he's alive
      db.updateUser(person)
      return jsonify({"status": "success"})
    except:
      return jsonify({"status": "failed"})

# filters
@app.template_filter('fromUTC')
def toDate_filter(x):
  return time.strftime('%b/%d/%Y, %H:%M:%S',time.gmtime(x))

# error handeling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# signal handlers
def sig_handler(sig, frame):
  IOLoop.instance().add_callback(shutdown)

def shutdown():
  MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3
  print('Stopping http server')
  http_server.stop()

  io_loop = IOLoop.instance()
  deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

  def stop_loop():
    now = time.time()
    if now < deadline and (io_loop._callbacks or io_loop._timeouts):
      io_loop.add_timeout(now + 1, stop_loop)
    else:
      io_loop.stop()
      print('Shutdown')
  stop_loop()

if __name__ == '__main__':
  # get properties
  host, port = conf.getWebAddress()
  debug = conf.getWebDebug()
  if debug:
    app.run(host=host, port=port, debug=debug)
  else:
    print("Server starting...")
    if conf.useSSL():
      ssl_options = {"certfile": conf.getSSLCert(), 
                     "keyfile":  conf.getSSLKey() }
    else:
      ssl_options = None
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    global http_server
    http_server = HTTPServer(WSGIContainer(app), ssl_options=ssl_options)
    http_server.bind(port, address=host)
    http_server.start(0)  # Forks multiple sub-processes
    IOLoop.instance().start()






