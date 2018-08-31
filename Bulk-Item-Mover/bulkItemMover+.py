########################################################################################################################
# Script Name: Bulk Item Mover For Canvas Modules
#
# Developed by: Scott Beaulieu
#
# Contact Information: nicholassjbeaulieu@protonmail.com
#
# WARNING: Canvas will cause this script to break if there are too many items in a module. The API will not send item 
# information if there are around 400-500 items in a single module.
# 
# Description: This script has two functions that are designed to achieve similar results, but for different scenarios.
# As a brief prelude to the functions, be aware that a table is printed in terminal that shows all module and item
# positions. Always refer to the table whenever possible. If a module is removed, but no others are rearranged, Canvas
# will skip numbers. i.e. the order was 1, 2, 3, 4 but you remove module 2 and don't rearrange, then the order will
# be 1, 3, 4. Both functions allow for a header to be created with the same name as the source module in the destination
# module where the items will be placed. Only function two allows for deletion of the source module(s).
#
# The first function allows the use to move a range of items from a source module to a destination module. The items are
# placed in the given position in the given destination module. If there is an item in that position, its position will
# be taken up by the new items and it and everything below it will be moved down.
#
# The second function allows you to move all the items from source module(s) into a destination module. This way
# "folder in folder" structure can be replicated quickly. It follows the same protocol as the first function. The moved
# items move to the specified position and take the place of item, if one is present in that position, and then moves
# that item down and all other items in below it.
########################################################################################################################


import requests
import logging
from datetime import datetime
import json


def testToken(token):
    accounts = requests.get(url + '/api/v1/course_accounts', params={'access_token': token})
    return accounts.json()


def tokenLogin():
    while True:
        accessToken = input('Please enter your Canvas API Access Token: ')
        test = testToken(accessToken)
        if 'errors' not in test:
            return accessToken
        else:
            print('Error: Invalid input, this may be due to an incorrect URL.\n')


def urlSelection():
    urlChoice = (("https://" + input("Please enter a URL for your Canvas instance. "
                                     "The format required is 'website.domainsuffix'. 'https://' will be "
                                     "appended to your input: "))).lower().strip(" ")
    return urlChoice


def courseSelection():
    while True:
        targetID = input("Please enter the target Course ID: ")
        print('\n')
        courseRequest = requests.get(url + "/api/v1/courses/{}".format(targetID), params={'access_token': token})
        course = courseRequest.json()
        if 'errors' not in course:
            print("You have selected the course \"{}\" \n".format(course['name']))
            while True:
                courseChoice = input("Is this the correct course? Enter \'y\' for yes or \'n\' for no: ")
                print('\n')
                if courseChoice == "y":
                    logging.info("Chosen Course Name: {}, Course ID: {}".format(course['name'], targetID))
                    return targetID
                elif courseChoice == "n":
                    print("Restarting course selection. \n")
                else:
                    print("Error: Invalid input. \n")
        else:
            print("Error: Course does not exist, or entered Course ID is invalid")


def getModuleID(listOfModules, modulePosition):
    index = 0
    while index != len(listOfModules):
        dictionary = listOfModules[index]
        if dictionary['position'] == modulePosition:
            return dictionary['id']
        else:
            index += 1
    logging.error("Could not find module with position {} (Function: getModuleID)".format(modulePosition))
    return 1


def getModuleName(listOfModules, moduleID):
    index = 0
    while index != len(listOfModules):
        dictionary = listOfModules[index]
        if dictionary['id'] == moduleID:
            return dictionary['name']
        else:
            index += 1
    logging.error("Could not find a module with ID {} (Function: getModuleName)".format(moduleID))
    return


def pullListOfIDValues(listOfDictionaries):
    valueList = [d['id'] for d in listOfDictionaries if 'id' in d]
    return valueList


def pullListOfIndentValues(listOfDictionaries):
    valueList = [d['indent'] for d in listOfDictionaries if 'indent' in d]
    return valueList


def returnListOfItems(list, modulePosition):
    index = 0
    while index != len(list):
        dictionary = list[index]
        if dictionary['position'] == modulePosition:
            return dictionary['items']
        else:
            index += 1
    logging.error("Could not find any items in module with position {} (Function: "
                  "returnListOfItems)".format(modulePosition))
    return 1


def getFullListOfModules():
    fullList = []
    modulesRequest = requests.get(url + "/api/v1/courses/{}/modules".format(courseID), params={'include[]': 'items',
                                                                                               'per_page': 100,
                                                                                               'access_token': token})
    modules = modulesRequest.json()
    for module in modules:
        fullList.append(module)
    while modulesRequest.links['current']['url'] != modulesRequest.links['last']['url']:
        modulesRequest = requests.get(modulesRequest.links['next']['url'], params={'include[]': 'items',
                                                                                   'per_page': 100,
                                                                                   'access_token': token})
        modules = modulesRequest.json()
        for module in modules:
            fullList.append(module)
    return fullList


def listModulePositionsAndItemPositions():
    allCourseModules = getFullListOfModules()
    print("START----------------------------------------------------------------------------Table---------------------"
          "------------------------------------------------------START")
    print("\n")
    for module in allCourseModules:
        print("Name: \"{}\", Position: {}".format(module['name'], module['position']))
        itemsList = module['items']
        for item in itemsList:
            print(" | --{}> Name: \"{}\", Position: {}".format(("--"*item['indent']), item['title'], item['position']))
        print("\n")
    print("END------------------------------------------------------------------------------Table---------------------"
          "--------------------------------------------------------END")
    print("Refer to the above table for module and item positions. (Canvas considers positions to still be occupied by "
          "deleted modules and items. The above table guarantees the correct position.) \n")


def bulkItemMoverModeOne(sourceModule, destinationModule, positionToBeMovedTo, createHeader, startingPosition, endingPosition):
    allModules = getFullListOfModules()
    sourceDictionaryList = returnListOfItems(allModules, sourceModule)
    if sourceDictionaryList == 1:
        return 1
    destinationDictionaryList = returnListOfItems(allModules, destinationModule)
    if destinationDictionaryList == 1:
        return 1
    sourceModuleID = getModuleID(allModules, sourceModule)
    sourceModuleName = getModuleName(allModules, sourceModuleID)
    logging.info("Source Module Name: {}".format(sourceModuleName))
    destinationModuleID = getModuleID(allModules, destinationModule)
    destinationModuleName = getModuleName(allModules, destinationModuleID)
    logging.info("Destination Module Name: {}".format(destinationModuleName))
    sourceItemIDs = pullListOfIDValues(sourceDictionaryList)
    itemToBeMovedIDs = sourceItemIDs[(startingPosition - 1):(endingPosition)]
    sourceItemIndentLevels = pullListOfIndentValues(sourceDictionaryList)
    itemToBeMovedIndentLevels = sourceItemIndentLevels[(startingPosition - 1):(endingPosition)]
    if createHeader == 1:
        putHeader = requests.post(url + "/api/v1/courses/{}/modules/{}/items".format(courseID, destinationModuleID),
                                  params={'module_item[title]': sourceModuleName, 'module_item[type]': 'SubHeader',
                                          'module_item[position]': positionToBeMovedTo,
                                          'module_item[published': 'true', 'access_token': token})
        positionToBeMovedTo += 1
        logging.info("Header created with name {}".format(sourceModuleName))
    percentPerItem = float(100/len(itemToBeMovedIDs))
    percentComplete = 0
    index = 0
    print("0.00% Complete")
    for value in itemToBeMovedIDs:
        if createHeader == 1:
            itemToBeMovedIndentLevels[index] += 1
        updateItem = requests.put(url + '/api/v1/courses/{}/modules/{}/items/{}'.format(courseID, sourceModuleID,
                                                                                        value),
                                  params={'module_item[position]': positionToBeMovedTo, 'module_item[indent]':
                                          itemToBeMovedIndentLevels[index],
                                          'module_item[module_id]': destinationModuleID,
                                          'access_token': token})
        index += 1
        positionToBeMovedTo += 1
        percentComplete += percentPerItem
        logging.info("Item with ID {} has been updated".format(value))
        print('{:3.2f}'.format(percentComplete) + '% Complete')
    logging.info("All items have been updated")
    return


def bulkItemMoverModeTwo(listOfModulePositions, destinationModule, positionToBeMovedTo, createHeader):
    while True:
        deleteFlag = input("Would you like to delete the source modules after they are moved? "
                           "Enter \'y\' for yes or \'n\' for no: ")
        if deleteFlag != ("y" or "n"):
            print("Error: Invalid input.")
        else:
            if deleteFlag == "n":
                print("Source module deletion will be skipped.")
            logging.info("deleteFlag: {}".format(deleteFlag))
            break
    for positionFromList in listOfModulePositions:
        if positionFromList == destinationModule:
            logging.info("A source module and the destination module are the same")
            return 1
    allModules = getFullListOfModules()
    while listOfModulePositions != []:
        sourceModule = listOfModulePositions[0]
        sourceDictionaryList = returnListOfItems(allModules, sourceModule)
        if sourceDictionaryList == 1:
            return 1
        destinationDictionaryList = returnListOfItems(allModules, destinationModule)
        if destinationDictionaryList == 1:
            return 1
        sourceModuleID = getModuleID(allModules, sourceModule)
        sourceModuleName = getModuleName(allModules, sourceModuleID)
        logging.info("Source Module Name: {}".format(sourceModuleName))
        destinationModuleID = getModuleID(allModules, destinationModule)
        destinationModuleName = getModuleName(allModules, destinationModuleID)
        logging.info("Destination Module Name: {}".format(destinationModuleName))
        sourceItemIDs = pullListOfIDValues(sourceDictionaryList)
        sourceItemIndentLevels = pullListOfIndentValues(sourceDictionaryList)
        if createHeader == 1:
            putHeader = requests.post(url + "/api/v1/courses/{}/modules/{}/items".format(courseID, destinationModuleID),
                                      params={'module_item[title]': sourceModuleName, 'module_item[type]': 'SubHeader',
                                              'module_item[position]': positionToBeMovedTo,
                                              'module_item[published': 'true', 'access_token': token})
            positionToBeMovedTo += 1
            logging.info("Header created with name {}".format(sourceModuleName))
        percentPerItem = float(100/len(sourceItemIDs))
        percentComplete = 0
        index = 0
        print("0.00% Complete")
        for value in sourceItemIDs:
            if createHeader == 1:
                sourceItemIndentLevels[index] += 1
            updateItem = requests.put(url + '/api/v1/courses/{}/modules/{}/items/{}'.format(courseID, sourceModuleID,
                                                                                            value),
                                      params={'module_item[position]': positionToBeMovedTo, 'module_item[indent]':
                                              sourceItemIndentLevels[index],
                                              'module_item[module_id]': destinationModuleID,
                                              'access_token': token})
            index += 1
            positionToBeMovedTo += 1
            percentComplete += percentPerItem
            logging.info("Item with ID {} has been updated".format(value))
            print('{:3.2f}'.format(percentComplete) + '% Complete')
        logging.info("All items have been updated")
        if deleteFlag == 'y':
            deleteSource = requests.delete(url + '/api/v1/courses/{}/modules/{}'.format(courseID, sourceModuleID),
                                           params={'access_token': token})
            logging.info("The source module, {}, has been deleted. deleteFlag = {}".format(sourceModuleName,
                                                                                           deleteFlag))
            print("Module \"{}\" deleted.".format(sourceModuleName))
        positionToBeMovedTo += len(sourceItemIDs)
        del listOfModulePositions[0]
    return


logFileName = "Bulk_Mover_Operation_{}-{}-{}_{}h{}m{}s.log".format(str((datetime.now()).year),
                                                                   str((datetime.now()).month),
                                                                   str((datetime.now()).day),
                                                                   str((datetime.now()).hour),
                                                                   str((datetime.now()).minute),
                                                                   str((datetime.now()).second))
logging.basicConfig(filename=logFileName, level=logging.INFO)
logging.info("Time: {}".format(datetime.now()))
url = urlSelection()
token = tokenLogin()
courseID = courseSelection()
while True:
    while True:
        print("---------------------------------------------------------------------------------Modes-----------------"
              "---------------------------------------------------------------")
        print("Mode 1: Allows the user to move a range of items (inclusive of the start and end positions) from a "
              "source module to a destination module where the items take the place of, and move down, "
              "a specified item and all items under it. \n")
        print("Mode 2: Allows the user to move all of the items from one or multiple source modules to a destination "
              "module where the items take the place of, and move down, a specified item and all the items under it. "
              "\n")
        print("*******************************************************************************************************"
              "***************************************************************")
        print("Both modes support the optional creation of a text header, but only mode 2 supports deletion of "
              "the source module(s).")
        print("*******************************************************************************************************"
              "***************************************************************")
        print("---------------------------------------------------------------------------------Modes-----------------"
              "---------------------------------------------------------------")
        mode = int(input("Please enter the number for a mode: "))
        if mode != 1 and mode != 2:
            print("Error: Invalid input. \n")
        else:
            print("\n")
            break
    logging.info("Chosen Mode: {}".format(mode))
    while True:
        newHeader = input("Would you like a new header created with the same name as the source module? Enter \'y\' "
                          "for yes or \'n\' for no: ")
        if newHeader == 'y':
            headerFlag = 1
            break
        elif newHeader == 'n':
            headerFlag = 0
            break
        else:
            print("Error: Invalid input. \n")
    print("\n")
    listModulePositionsAndItemPositions()
    if mode == 1:
        while True:
            source = input("Please enter the position of the source module (1, 2, 3 ...): ")
            if source.isdigit() and source != '0':
                source = int(source)
                break
            else:
                print("Error: Invalid input. Input has to be greater than 0 and a number. \n")
        while True:
            destination = input("Please enter the position of the destination module (1, 2, 3 ...): ")
            if destination.isdigit() and destination != '0':
                destination = int(destination)
                break
            else:
                print("Error: Invalid input. Input has to be greater than 0 and a number. \n")
        while True:
            position = input("Please enter the position you would like the items moved to (The item occupying the "
                             "position will be moved down, as will any items under it): ")
            if position.isdigit() and position != '0':
                position = int(position)
                if mode == 2:
                    print("\n")
                break
            else:
                print("Error: Invalid input. Input has to be greater than 0 and a number. \n")
        while True:
            firstPosition = input("Please enter the position of the first item you would like to move: ")
            if firstPosition.isdigit() and firstPosition != '0':
                firstPosition = int(firstPosition)
                break
            else:
                print("Error: Invalid input. Input has to be greater than 0 and a number. \n")
        while True:
            lastPosition = input("Please enter the position of the last item you would like to move: ")
            if lastPosition.isdigit() and lastPosition != '0' and lastPosition > str(firstPosition):
                lastPosition = int(lastPosition)
                print("\n")
                break
            else:
                print("Error: Invalid input. Input has to be greater than 0, a number, and greater than"
                      "the first position. \n")
        logging.info("Source Destination Module Position: {}, Destination Module Position: {}, Position in Module: {}, "
                     "Create Header Flag: {}, Range of Items Being Moved: {}, {}".format(source, destination, position,
                                                                                         headerFlag, firstPosition,
                                                                                         lastPosition))
        status = bulkItemMoverModeOne(source, destination, position, headerFlag, firstPosition, lastPosition)
    elif mode == 2:
        while True:
            sourceString = input("Please enter the source module(s) position(s) (The module(s) will be moved in the "
                                 "order entered and if there is more than one module, each position must be separated "
                                 "by a space): ")
            zeroFlag = 0
            source = list(map(int, sourceString.split()))
            for value in source:
                if value == 0:
                    zeroFlag = 1
            if zeroFlag == 0:
                break
            else:
                print("Error: No position can contain 0.")
        while True:
            destination = input("Please enter the position of the destination module (1, 2, 3 ...): ")
            if destination.isdigit() and destination != '0':
                destination = int(destination)
                break
            else:
                print("Error: Invalid input. Input has to be greater than 0 and a number. \n")
        while True:
            position = input("Please enter the position you would like the items moved to (The item occupying the "
                             "position will be moved down, as will any items under it): ")
            if position.isdigit() and position != '0':
                position = int(position)
                if mode == 2:
                    print("\n")
                break
            else:
                print("Error: Invalid input. Input has to be greater than 0 and a number. \n")
        logging.info("Source Destination Module Position: {}, Destination Module Position: {}, Position in Module: {}, "
                     "Create Header Flag: {}".format(source, destination, position, headerFlag))
        status = bulkItemMoverModeTwo(source, destination, position, headerFlag)
    else:
        break
    if status == 1:
        print("The process stopped abruptly, please look at the created log file for the error")
    else:
        print("Process complete!")
    while True:
        continueFlag = input("Would you like to move another module or range of items? Enter \'y\' for yes, or \'n\' "
                             "for no: ")
        if continueFlag == 'y':
            logging.info("Moving another module or range of items")
            print('Restarting. URL, Token, and Course ID will be retained. \n')
            break
        elif continueFlag == 'n':
            logging.info("Program has terminated")
            logging.info("End: {}".format(datetime.now()))
            print("Stopping program. Have a great day!")
            break
        else:
            print("Invalid input. \n")
    if continueFlag == 'n':
        break
