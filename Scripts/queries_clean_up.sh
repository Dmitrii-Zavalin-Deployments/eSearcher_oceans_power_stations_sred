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

# Navigate to the parent directory of the script
cd "$(dirname "$0")" || { echo "Failed to navigate to the script's directory."; exit 1; }

# Log message indicating the start of the cleanup process
echo "Starting cleanup process. Each query name should be on a new line in the file queries_to_clean_up.txt."

# Ensure the IFS (Internal Field Separator) is set to handle spaces properly
IFS=$'\n'

# Read each query name from queries_to_clean_up.txt and process them
while read -r QUERY_NAME || [[ -n "$QUERY_NAME" ]]; do
  # Log the query name being processed
  echo "Cleaning up query: $QUERY_NAME"
  
  # Use jq to update data.json for each query
  jq --arg query_name "$QUERY_NAME" --arg date_time "$(date)" '(.[$query_name] | select(. != null)) = ["This query was cleaned up at \($date_time)"]' ../data/data.json > temp.json && mv temp.json ../data/data.json
  
  # Check if the update was successful
  if [ $? -eq 0 ]; then
    echo "Successfully cleaned up query: $QUERY_NAME"
  else
    echo "Failed to clean up query: $QUERY_NAME. Please check if the query name exists in data.json and is correctly formatted."
  fi
done < queries_to_clean_up.txt

# Reset IFS to default
unset IFS

# Clear the queries_to_clean_up.txt file after processing all queries
> queries_to_clean_up.txt

# Add, commit, and push changes if there were any
if ! git diff --quiet ../data/data.json queries_to_clean_up.txt; then
  git add ../data/data.json queries_to_clean_up.txt
  git commit -m "Cleaned up queries"
  git push origin main
else
  echo "No changes to commit."
fi


