#!/bin/python3

import os,sys,json,importlib

sys.path.append('./core')

app = importlib.import_module('XmediaCenterCore')
app.run()