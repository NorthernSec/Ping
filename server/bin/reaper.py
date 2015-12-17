import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

import lib.DatabaseConnection as db
from lib.Actor import Actor

if __name__ == '__main__':
  actor = Actor()
  # Actions of dead users that failed before
  actor.queue(db.getActionsToDo())
  # New dead users
  for user in db.getNewDeaths():
    db.markDead(user)
    actions=db.getActions(user)
    actor.queue(actions)

  # Update actions
  close,failed = actor.actOnQueue() 
  for act in close: db.markCompleted(act)
  for act in failed: db.markFailed(act)
