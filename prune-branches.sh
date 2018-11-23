#!/bin/bash

# removes local branches that are no longer on remote

prune_branches() {
  git fetch -p && for branch in `git branch -vv --no-color | grep ': gone]' | awk '{print $1}'`; do git branch $deleteArg $branch; done
}

if [ $1 = "-d" ] || [ $1 = "-D" ]; then
  deleteArg=$1
  prune_branches $deleteArg
else
  echo "Command not recognised. Try -d for soft delete; -D for hard delete";
fi
