#!/bin/python3
import sys,mimetypes

print(mimetypes.guess_type(sys.argv[1])[0])