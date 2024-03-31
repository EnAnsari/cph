#!/bin/bash

# Check if db.txt exists
if [ ! -f "db.txt" ]; then
  # Create an empty file named db.txt
  touch "db.txt"
  echo "Created db.txt"
fi