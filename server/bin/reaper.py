import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

import lib.DatabaseConnection as db


if __name__ == '__main__':
  # For x in db.getActionsToDo(): (== with attempts > 0)
    # Execute action
    # If success => set to -1
    # If fail, increment with 1

  for x in db.getNewDeaths():
    # Fetch actions
    # Act
    # Set time for user to -1
    # Execute actions for user
      # If success, set to -1, else, increment with 1

	
