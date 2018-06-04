# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Enter_Course.py
import Init, API_Calls as API

def enterCourse():
    while True:
        input_short_course_id = input('Enter Course ID:')
        input_full_course_id = '#Your token prefix/account number goes here' + input_short_course_id.zfill(13)
        try:
            course = API.testCourse(input_full_course_id)
            print(('Found Course: ({})\n').format(course['name']))
            Init.Course_ID = input_full_course_id
            Init.Short_Course_ID = input_short_course_id
            break
        except:
            print('Invalid Course ID. The requested course either does not exist, or you do not have access to it.')
