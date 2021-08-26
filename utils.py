#!/bin/python3
import core.XmediaCenterCore as Core,core.xmcp,sys

if sys.argv[1] == 'account':
    if sys.argv[2] == 'new':
        print(Core.create_account(sys.argv[3],sys.argv[4]))
    elif sys.argv[2] == 'remove':
        print(Core.remove_account(sys.argv[3],sys.argv[4]))
    elif sys.argv[2] == 'modify':
        if Core.remove_account(sys.argv[3],sys.argv[4]):
            print(Core.create_account(sys.argv[3],sys.argv[5]))
        else:
            print('False')
