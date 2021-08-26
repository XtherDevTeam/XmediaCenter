#!/bin/python3
import core.XmediaCenterCore,core.xmcp,sys

print(sys.argv[2])

if sys.argv[1] == 'account':
    if sys.argv[2] == 'new':
        print(core.XmediaCenterCore.create_account(sys.argv[3],sys.argv[4]))
    elif sys.argv[2] == 'remove':
        print(core.XmediaCenterCore.remove_account(sys.argv[3],sys.argv[4]))
    elif sys.argv[2] == 'modify':
        if core.XmediaCenterCore.remove_account(sys.argv[3],sys.argv[4]):
            print(core.XmediaCenterCore.create_account(sys.argv[3],sys.argv[5]))
        else:
            print('False')
