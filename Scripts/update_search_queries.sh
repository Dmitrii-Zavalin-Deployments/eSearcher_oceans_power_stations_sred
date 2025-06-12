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

# Navigate to the root directory of the repository where the data directory is located
cd "$(dirname "$0")"/.. || { echo "Failed to navigate to the root directory of the repository."; exit 1; }

# Check if the data directory exists
if [ ! -d "data" ]; then
  echo "Data directory not found. Exiting."
  exit 1
fi

# Navigate to the data directory
cd data

# Loop through each subfolder in the data directory
for dir in */ ; do
  # Check if search_name.txt exists in the subfolder
  if [[ -f "$dir/search_name.txt" ]]; then
    # Read the first line of search_name.txt to use as the commit message
    commit_message=$(head -n 1 "$dir/search_name.txt")
    # Add only the modified files in the subfolder to the staging area
    git add "$dir"*
    # Commit the changes with the message from search_name.txt
    git commit -m "Updated query for $commit_message"
  else
    # If search_name.txt is not found, use a generic commit message
    git add "$dir"*
    git commit -m "Updated query in data/$dir"
  fi
done

# Push the changes to the remote repository
git push origin main


