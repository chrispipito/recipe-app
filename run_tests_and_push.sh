#!/bin/bash

# Check the current branch
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [ "$current_branch" == "main" ]; then
    echo "You are on the main branch. Please switch to a feature branch for development."
    exit 1
fi

cd /Users/chris/PycharmProjects/Projects/Recipes/tests
# Run the tests
python -m unittest discover tests

# If the tests pass, prompt for a commit message and commit the changes
if [ $? -eq 0 ]; then
    echo "Tests passed. Please enter a commit message:"
    read commit_message

    git add .
    git commit -m "$commit_message"
    git push origin "$current_branch"

    # Checkout main and merge the feature branch
    git checkout main
    git pull origin main  # Ensure main is up-to-date
    git merge "$current_branch"
    git push origin main

    # Decide if more work is needed on the feature branch or if it should be closed
    echo "Do you need to return to the feature branch for more work? (yes/no)"
    read decision

    if [ "$decision" == "yes" ]; then
        git checkout "$current_branch"
        echo "Switched back to $current_branch for more work."
    else
        echo "Do you want to delete the local and remote feature branch? (yes/no)"
        read delete_branch_decision

        if [ "$delete_branch_decision" == "yes" ]; then
            # Delete the local branch
            git branch -d "$current_branch"

            # Delete the remote branch
            git push origin --delete "$current_branch"

            echo "Feature branch $current_branch has been deleted."
        else
            echo "Feature branch $current_branch has been kept."
        fi
        
        # Prompt for creating a new branch
        echo "Would you like to create a new branch? (yes/no)"
        read create_new_branch
        
        if [ "$create_new_branch" == "yes" ]; then
            echo "Enter the name for the new branch:"
            read new_branch_name
            git checkout -b "$new_branch_name"
            # Push the new branch to remote repository
            git push -u origin "$new_branch_name"
            echo "New branch $new_branch_name has been created, checked out, and pushed to the remote repository."
        fi
    fi
else
    echo "Tests failed. Fix the issues before committing."
fi





