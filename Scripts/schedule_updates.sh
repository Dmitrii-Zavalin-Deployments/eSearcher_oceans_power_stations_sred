#!/bin/bash

# Function to check for jq and install it if necessary
install_jq() {
  if ! command -v jq &> /dev/null; then
    echo "jq could not be found, attempting to install..."
    case "$OSTYPE" in
      linux-gnu*)
        if [ -f /etc/debian_version ]; then
          sudo apt-get update && sudo apt-get install -y jq
        elif [ -f /etc/redhat-release ]; then
          sudo yum install -y jq
        else
          echo "Unsupported Linux distribution. Please install jq manually."
          exit 1
        fi
        ;;
      darwin*)
        if command -v brew &> /dev/null; then
          brew install jq
        else
          echo "Homebrew not found. Please install Homebrew and jq manually."
          exit 1
        fi
        ;;
      *)
        echo "Unsupported operating system. Please install jq manually."
        exit 1
        ;;
    esac
  else
    echo "jq is already installed."
  fi
}

# Check for jq and install if necessary
install_jq

# Function to run a script and echo its name and the current date
run_script() {
  echo "Running $1: $(date)"
  bash "$1" | while IFS= read -r line; do
    echo "[$(date)] $1: $line"
  done
}

# Function to handle interrupts and run specific code before exiting
cleanup() {
  echo "Interrupt received, running cleanup scripts..."
  # Run the reviewed_links_update.sh script
  run_script "./reviewed_links_update.sh"

  # Run the update_search_queries.sh script
  run_script "./update_search_queries.sh"

  # Run the queries_clean_up.sh script
  run_script "./queries_clean_up.sh"

  echo "Cleanup complete. Exiting now."
  exit 0
}

# Trap Ctrl+C (SIGINT) and Ctrl+D (EOF/SIGTERM) to run the cleanup function
trap cleanup SIGINT SIGTERM

# Main loop
while true; do
  # Run the reviewed_links_update.sh script
  run_script "./reviewed_links_update.sh"

  # Run the update_search_queries.sh script
  run_script "./update_search_queries.sh"

  # Run the queries_clean_up.sh script
  run_script "./queries_clean_up.sh"

  # Wait for 15 minutes before the next update
  echo "Waiting for 15 minutes before the next update..."
  sleep 900 # Sleep for 15 minutes
done


