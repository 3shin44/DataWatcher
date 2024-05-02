# Shell Controller Note

## Note

This folder store shell script for Raspbian execute python functions with venv

All file is converted to UNIX format. Don't run on Windows!

## Preparation

adjust project absolute path in config.bat, all bat will take this variable to launch

## Installation

1. set permission for entire folder

`chmod -R +x /path/to/shellController`

2. set absolute path in config.bat

`PROJECT_DIR="/path/to/project"`

3. test run

`bash /path/to/project/shellController/test.sh`