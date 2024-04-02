#!/bin/bash

# Create a Python 3.10 virtual environment named "autodiarize"
python3.10 -m venv autodiarize

# Activate the virtual environment
source autodiarize/bin/activate

# Install the packages from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

echo "Virtual environment 'autodiarize' created and packages installed successfully."
