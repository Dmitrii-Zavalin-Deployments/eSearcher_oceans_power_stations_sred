#!/bin/bash

# Function to cleanup before exiting
cleanup() {
  echo "Cleanup complete. Exiting."
  exit 0
}

# Trap SIGINT to call the cleanup function on script termination
trap cleanup SIGINT

# Stash any unstaged changes
git stash push --include-untracked -m "Auto-stashed by cleanup script"

# Pull the latest changes from the repository
git pull --rebase origin main

# Reapply the stashed changes
git stash pop

# Navigate to the directory above the current one, which should be the root of the repository
cd "$(dirname "$0")"/.. || { echo "Failed to navigate to the root directory of the repository."; exit 1; }

# Add only the reviewed_links.txt file to the staging area
if [ -f data/reviewed_links.txt ]; then
  git add data/reviewed_links.txt
else
  echo "The file data/reviewed_links.txt does not exist."
  exit 1
fi

# Check if there are any changes to commit
if git diff --staged --quiet; then
  echo "$(date): No changes to commit."
else
  # Commit the changes with the specified message
  git commit -m "Added reviewed links"

  # Push the changes to the remote repository
  git push origin main
  echo "$(date): Changes committed and pushed."
fi


