#!/bin/bash

# Create VENV & Install Modules
python3 -m venv $INSTALL_DIR/noshgrab_venv
source $INSTALL_DIR/noshgrab_venv/bin/activate && pip install -r $INSTALL_DIR/requirements.txt
deactivate