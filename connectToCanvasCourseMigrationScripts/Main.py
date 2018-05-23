# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Main.py
from Login import tokenLogin
from Enter_Course import enterCourse
from Files_To_Pages import MasterFTP
from Clean_Pages import MasterClean
from Services import *

def mainLoop():
    optionFlag = True
    while True:
        if optionFlag == True:
            print('Select from the following by entering the number/key associated with your desired action(s):')
            print('Migrations*')
            print('    1. Convert HTML files to pages -> Delete residual HTML files -> Fix broken internal links')
            print('    2. Break up a module (can be skipped) -> Make all page titles unique -> Clean all content pages')
            print('Services*')
            print('    a. Restore all content pages to first version')
            print('    b. Make all external links in modules open in new tabs')
            print('    c. Delete all unpublished Content Pages')
            print('    d. Delete duplicate module-items')
            print('    e. Set course homepage to syllabus')
            print('    q. Quit')
            optionFlag = False
        selection = input('YOUR INPUT:')
        print('\n')
        if selection.lower() == 'q':
            return
        if selection.lower() not in ('1', '2', 'a', 'b', 'c', 'd', 'e'):
            print('Invalid entry. \n')
        else:
            methodRouter = {'1':MasterFTP, 
             '2':MasterClean, 
             'a':MasterRAP, 
             'b':openLinksInNewTabs, 
             'c':deleteUnpublishedPages, 
             'd':MasterUMC, 
             'e':setHomeToSyllabus}
            methodRouter[selection.lower()]()
            print('****Process Complete****')
            input('PRESS ENTER TO RETURN TO THE MENU...')
            print('\n')
            optionFlag = True


tokenLogin()
enterCourse()
mainLoop()
