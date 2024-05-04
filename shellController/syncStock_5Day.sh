#!/bin/bash
# get current path
SCRIPT_DIR="$(dirname "$0")"
# get path variable from config.sh
source "$SCRIPT_DIR/config.sh"
# Python commands: startup, execute, deactivate
source $PROJECT_DIR/bin/activate
python $PROJECT_DIR/controller/syncStock_5Day.py
deactivate