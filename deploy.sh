#!/bin/bash

# Add all changes
git add .

# Get commit message
echo "Enter commit message:"
read message

# Commit and push
git commit -m "$message"
git push origin main

echo "Changes pushed to GitHub. Streamlit Cloud will auto-deploy."