# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Login.py
import API_Calls as API, Init

def tokenLogin():
    while True:
        token = input('Please enter your Canvas API Access Token:')
        test = API.testToken(token)
        if 'errors' not in test:
            Init.Access_Token = token
            break
        else:
            print('Invalid entry, try again.')