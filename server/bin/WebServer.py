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
from flask import Flask, render_template, request, redirect, jsonify, abort
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug import secure_filename
import calendar
import random
import signal
import time

from lib.Communication import MailBot
from lib.Configuration import Configuration as conf
from lib.Controls import isEmail
from lib.Exceptions import UserIsDead, UserAlreadyExists
from lib.Users import User
from lib.User  import User as UserObj
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
@app.route('/', methods=['get'])
def index():
  return render_template('index.html')

@app.route('/profile', methods=['get'])
def profile():
  if not current_user.is_authenticated():
    return render_template('login.html', status=["default", "none"])
  return render_template('profile.html', user=current_user)

@app.route('/login', methods=['get'])
def login():
  if not current_user.is_authenticated():
    return render_template('login.html', status=["default", "none"])
  else:
    return redirect("/profile")

@app.route('/signup', methods=['get'])
def signUp():
  if not current_user.is_authenticated():
    return render_template('signup.html', status=["default", "none"])
  else:
    return redirect("/profile")

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect("/")

# ajax
@app.route('/_login')
def validate_login():
  username = request.args.get('username')
  password = request.args.get('password')
  person = User.get(username)
  try:
    if person and person.user.verifyPassword(password):
      login_user(person)
      person.user.ping() #If a user can log in, he's alive
      db.updateUser(person.user)
      return jsonify({"status": "logged_in"})
    else:
      return jsonify({"status": "user_pass_mismatch"})
  except UserIsDead:
    return jsonify({"status": "user_is_dead"})

@app.route('/_change_pass')
@login_required
def change_pass():
  old = request.args.get('password',     type=str)
  new = request.args.get('new_password', type=str)
  person = current_user.user
  if not person.verifyPassword(old):
    return jsonify({"status": "wrong_pass"})
  else:
    try:
      person.setPassword(new)
      person.ping() #If a user can change his password, he's alive
      db.updateUser(person)
      return jsonify({"status": "pass_updated"})
    except:
      return jsonify({"status": "user_action_failed"})

@app.route('/_request_token')
def token_request():
  email = request.args.get('email', type=str)
  if not isMail(email):    return jsonify({"status": "invalid_mail"})
  if db.getUser(email)[0]: return jsonify({"status": "user_exists"})
  # Don't allow certain domains
  domain = email[email.index("@")+1:]
  if domain in conf.getBannedDomains():
    return jsonify({"status": "banned_domain"})
  token = str(random.SystemRandom().randint(0, 99999999))
  token = "0"*(8-len(token))+token
  token = "%s %s"%(token[:4], token[4:]) # user friendliness
  db.addToken(email, token)
  message=tokenMail.replace("%token%", token)
  try:
    mailer=MailBot()
    mailer.login()
    mailer.sendMail(email, message)
    mailer.logout()
    return jsonify({"status": "token_sent"})
  except:
    return jsonify({"status": "mail_failed"})

@app.route('/_create_account')
def create_account():
  email = request.args.get('email', type=str)
  pwd   = request.args.get('password', type=str)
  token = request.args.get('token', type=str)
  # 'if token and' to prevent bypassing with empty token
  if token and token == db.getToken(email):
    try:
      person = UserObj(email, pwd)
      db.removeToken(email) # remove token first, to prevent fake registration
      db.addUser(person)
      return jsonify({"status": "account_created"})
    except UserAlreadyExists:
      return jsonify({"status": "user_exists"})
  else:
    return jsonify({"status": "invalid_token"})

@app.route('/_get_action_details')
@login_required
def get_action_details():
  action = request.args.get('action', type=str)
  target = request.args.get('target', type=str)
  response = None
  if target and action:
    response = db.getAction(current_user.user, action, target).getDict()
  return jsonify(response)

@app.route('/_get_actions')
@login_required
def get_actions():
  ret = {'data': [x.getDict() for x in db.getActions(current_user.user)]}
  return jsonify(ret)

@app.route('/_add_action')
@login_required
def add_action():
  action   = request.args.get('action', type=str)
  target   = request.args.get('target', type=str)
  username = request.args.get('username', type=str)
  message  = request.args.get('message', type=str)
  try:
    act = Action(current_user.user, action, target, username, message)
    db.addAction(act)
    reply = {'status':  'action_added',
             'actions': db.getActions(current_user.user)}
  except (InvalidAction, InvalidVarType, UserDoesNotExist):
    print("[!] user is sending forged messages")
    abort(406)
  except InvalidTarget:       reply = {'status': 'invalid_target'}
  except TooManyActions:      reply = {'status': 'too_many_actions'}
  except ActionAlreadyExists: reply = {'status': 'action_exists'}
  except: reply = {'status': 'user_action_failed'}
  return jsonify(reply)

@app.route('/_remove_action')
@login_required
def remove_action():
  action = request.args.get('action', type=str)
  target = request.args.get('target', type=str)
  if target and action:
    try:
      act = db.getAction(current_user.user, action, target)
      db.removeAction(act)
      return jsonify({"status": "action_removed",
                      "actions": db.getActions(current_user.user)})
    except:
      abort(409)
  else:
    print("data manipulation attempt detected!")
    abort(406)

# filters
@app.template_filter('fromUTC')
def toDate_filter(x):
  return time.strftime('%b/%d/%Y, %H:%M:%S',time.gmtime(x))

# error handeling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(406)
def fraud_attempt(e):
  return jsonify({"status": "fraud_attempt"})

@app.errorhandler(409)
def edit_conflict(e):
  return jsonify({"status": "edit_conflict"})

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
  # check needed config settings:
  
  tokenMail = conf.getTokenMessage()
  if not tokenMail or not "%token%" in tokenMail:
    sys.exit("Please check the message for tokens")

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






