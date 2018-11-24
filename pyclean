#!/bin/bash

# Removes all `.pyc` and `.pyo` files, and `__pycache__` directories
pyclean () {
  find . -type f -name "*.py[co]" -delete
  find . -type d -name "__pycache__" -delete
  echo "dir cleaned of .py[co] and __pycache__"
}

pyclean
