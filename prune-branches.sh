#!/bin/bash

# removes local branches that are no longer on remote

# soft delete if arg is -d
prune_soft_delete() {
  git fetch -p && for branch in `git branch -vv --no-color | grep ': gone]' | awk '{print $1}'`; do git branch -d $branch; done
}

# hard delete if arg is -D
prune_hard_delete() {
  git fetch -p && for branch in `git branch -vv --no-color | grep ': gone]' | awk '{print $1}'`; do git branch -D $branch; done
}

if [ $1 = "-d" ]; then
  prune_soft_delete
elif [ $1 = "-D" ]; then
  prune_hard_delete
else
  echo "Command not recognised. Try -d for soft delete; -D for hard delete";
fi
