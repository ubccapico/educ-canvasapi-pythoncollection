########################################################################################################################
# Script Name: Connect Migrated Files Cleaner For Canvas
#
# Developed by: Scott Beaulieu
#
# Contact Information: nicholassjbeaulieu@protonmail.com
#
# Description: Cleans all log files in a course and then systemactially deletes any empty folders. It achieves this by
# deleting only folders containing no folders or files and then deleting any new folders that now contain no folders or
# files. It does this until there are no longer any new folders that contain no files or folders.
########################################################################################################################


import requests
import json


def testToken(token):  # Tests the provided token
    # Returns a paginated list of accounts that the current user can view
    accounts = requests.get(url + '/api/v1/course_accounts', params={'access_token': token})
    return accounts.json()


def tokenLogin():
    while True:
        # Takes an input of an access token
        accessToken = input('Please enter your Canvas API Access Token: ')
        # Assigns a test variable as the return of testToken given an access token
        test = testToken(accessToken)
        # Tests to see if there are any errors in the returned token. If there aren't any, it returns the token
        if 'errors' not in test:
            return accessToken
        # If there are errors, it prints the below statement and continues to loop
        else:
            print('Error: Invalid entry, try again. This may be due to an incorrect URL.\n')


def urlSelection():  # Takes a URL in the form of website.domainsuffix and returns the full URL
    urlChoice = ("https://" + input("Please enter a URL for your Canvas instance. "
                                    "The format required is 'website.domainsuffix'. 'https://' will be"
                                    " appended to your input: "))
    return urlChoice


def courseSelection():
    while True:
        targetID = input("Please enter the target Course ID: ")
        print('\n')
        courseRequest = requests.get(url + "/api/v1/courses/{}".format(targetID), params={'access_token': token})
        course = courseRequest.json()
        if 'errors' not in course:
            print("You have selected the course \'{}\' \n".format(course['name']))
            courseChoice = input("Is this the correct course? Enter \'y\' for yes or \'n\' for no: ")
            print('\n')
            if courseChoice == "y":
                return targetID
            else:
                print("Restarting course selection. \n")
        else:
            print("Error: Course does not exist, or entered Course ID is invalid")


def pullListOfFileCounts(listOfDictionaries):
    valueList = [d['files_count'] for d in listOfDictionaries if 'files_count' in d]
    return valueList


def pullListOfFolderCounts(listOfDictionaries):
    valueList = [d['folders_count'] for d in listOfDictionaries if 'folders_count' in d]
    return valueList


def pullListOfFolderIDs(listOfDictionaries):
    valueList = [d['id'] for d in listOfDictionaries if 'id' in d]
    return valueList


# *** Extraneous Function, but it might be useful in the future. Reorders folders in ascending order of the number of
# folders contained in the folders. ***
#
# def reorderAscNumFolderIn(listOfDictionaries):
#    reorderedList = []
#    while True:
#        if listOfDictionaries == []:
#            return reorderedList
#        initIndex = 0
#        position = 0
#        lowest = listOfDictionaries[initIndex]
#        while initIndex < (len(listOfDictionaries) - 1):
#            nextDict = listOfDictionaries[initIndex + 1]
#            if lowest['folders_count'] == 0:
#                break
#            elif nextDict['folders_count'] < lowest['folders_count']:
#                lowest = nextDict
#                initIndex += 1
#                position = initIndex
#            else:
#                initIndex += 1
#        reorderedList.append(lowest)
#        del listOfDictionaries[position]


def getFullListOfFiles():
    fullList = []
    filesRequest = requests.get(url + '/api/v1/courses/{}/files'.format(courseID), params={'sort': 'size',
                                                                                           'per_page': 100,
                                                                                           'order': 'asc',
                                                                                           'access_token': token})
    files = filesRequest.json()
    for file in files:
        fullList.append(file)
    while filesRequest.links['current']['url'] != filesRequest.links['last']['url']:
        filesRequest = requests.get(filesRequest.links['next']['url'], params={'sort': 'size',
                                                                        'per_page': 100,
                                                                        'order': 'asc',
                                                                        'access_token': token})
        files = filesRequest.json()
        for file in files:
            fullList.append(file)
    return fullList


def getFullListOfFolders():
    fullList = []
    foldersRequest = requests.get(url + '/api/v1/courses/{}/folders'.format(courseID), params={'per_page': 100,
                                                                                               'access_token': token})
    folders = foldersRequest.json()
    for folder in folders:
        fullList.append(folder)
    while foldersRequest.links['current']['url'] != foldersRequest.links['last']['url']:
        foldersRequest = requests.get(foldersRequest.links['next']['url'], params={'per_page': 100,
                                                                                   'access_token': token})
        folders = foldersRequest.json()
        for folder in folders:
            fullList.append(folder)
    return fullList


def connectMigratedFilesCleaner():
    courseFiles = getFullListOfFiles()
    courseFolders = getFullListOfFolders()
    fileCounts = pullListOfFileCounts(courseFolders)
    folderCounts = pullListOfFolderCounts(courseFolders)
    folderIDs = pullListOfFolderIDs(courseFolders)
    folderIndex = 0
    if startFlag == 'b':
        for value in fileCounts:
            if value >= 1 or folderCounts[folderIndex] >= 1:
                dictIndex = 0
                while dictIndex != len(courseFiles):
                    dictionary = courseFiles[dictIndex]
                    if dictionary['folder_id'] == folderIDs[folderIndex] and dictionary['content-type'] == 'text/x-log':
                        deleteFileRequest = requests.delete(url + '/api/v1/files/{}'.format(dictionary['id']),
                                                            params={'access_token': token})
                        print("Deleted file: {}".format(dictionary['display_name']))
                    dictIndex += 1
            folderIndex += 1
    cleanedCourseFolders = getFullListOfFolders()
    fileCounts = pullListOfFileCounts(cleanedCourseFolders)
    folderCounts = pullListOfFolderCounts(cleanedCourseFolders)
    folderIDs = pullListOfFolderIDs(cleanedCourseFolders)
    noFoldersCount = 1
    while noFoldersCount != 0:
        index = 0
        noFoldersCount = 0
        for value in fileCounts:
            if value == 0 and folderCounts[index] == 0:
                deleteFolderRequest = requests.delete(url + '/api/v1/folders/{}'.format(folderIDs[index]),
                                                      params={'force': 'true', 'access_token': token})
                noFoldersCount = 1
                print("Deleted folder: {}".format((cleanedCourseFolders[index])['full_name']))
            index += 1
        cleanedCourseFolders = getFullListOfFolders()
        fileCounts = pullListOfFileCounts(cleanedCourseFolders)
        folderCounts = pullListOfFolderCounts(cleanedCourseFolders)


print("***This scripts deletes any leftover log files and then force deletes any empty folders. To recover any files "
      "append \'undelete\' after the course number in your URL. If they were contained in a deleted folder Canvas "
      "will create a folder titled \'unfiled\' which will contain the recovered items***\n")
url = urlSelection()
token = tokenLogin()
courseID = courseSelection()
while True:
    startFlag = input("Would you like to delete any log files and empty folders, or just empty folders? "
                      "Enter \'b\' for both log files and folders or \'f\' for just folders: ")
    if startFlag != 'b' and startFlag != 'f':
        print("Error: Invalid input")
    else:
        break
print("\n")
connectMigratedFilesCleaner()
if startFlag == 'b':
    print("Log file and folder cleanup complete!")
else:
    print("Folder cleanup complete!")