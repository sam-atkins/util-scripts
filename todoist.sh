#!/bin/bash
# entrypoint to Python script.
# Suggestion: set an alias `td` to invoke this shell script

source /Users/samatkins/code/util-scripts/env/bin/activate;
python /Users/samatkins/code/util-scripts/src/todoist_api.py "$@";
