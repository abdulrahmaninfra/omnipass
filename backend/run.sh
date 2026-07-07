#!/bin/bash
source ~/Documents/api/myenv/bin/activate.fish

uvicorn "$1":app --reload