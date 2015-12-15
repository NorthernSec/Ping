import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

import lib.DatabaseConnection as db

MESSAGE="Deathclock message: %s has probably passed away."

if __name__ == '__main__':
  # For x in db.getActionsToDo(): (== with attempts > 0)
    # Execute action
    # If success => set to -1
    # If fail, increment with 1

  for user in db.getNewDeaths():
    db.markDead(user)
    for a in db.getActions(user):
      uname=a.username if a.username else user.email
      message = MESSAGE%uname
      if a.message:
        message+="\nPersonal message: %s"%a.message

      if a.action=="irc":
        print("will connect to irc and send the following message:")
        print(message)
      elif a.action=="xmpp":
        print("will connect to xmpp and send the follwing message:")
        print(message)
      elif a.action=="mail":
        print("will send an email with the follwing message:")
        print(message)
    # Execute actions for user
      # If success, set to -1, else, increment with 1

	
