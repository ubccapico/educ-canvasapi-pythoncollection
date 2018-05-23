# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Services.py
import API_Calls as API, Init

def setHomeToSyllabus():
    API.setHome()
    print('Home page has been successfully set to syllabus')


def openLinksInNewTabs():
    print('****Making all external links in modules open in new tabs****')
    modules = API.getAllModules()
    convertedCount = 0
    for module in modules:
        moduleItems = API.getModuleItems(module['id'])
        for moduleItem in moduleItems:
            if moduleItem['type'] == 'ExternalUrl':
                if not moduleItem['new_tab']:
                    API.newTab(module['id'], moduleItem['id'])
                    print(moduleItem['title'] + ' now opens in a new tab')
                    convertedCount += 1

    print(('{} link(s) were converted to open in new tabs').format(convertedCount))


def unduplicateModuleContents(moduleID):
    result = False
    module_items = API.getModuleItems(moduleID)
    checked_items = []
    for module_item in module_items:
        data_pair = (
         module_item['title'], module_item['type'])
        if data_pair not in checked_items:
            checked_items.append(data_pair)
        else:
            print(('----Duplicate item detected: [{}]').format(data_pair))
            API.deleteModuleItem(moduleID, module_item['id'])
            if not result:
                result = True

    return result


def MasterUMC():
    print('****Deleting Duplicate Module Contents****')
    modules = API.getAllModules()
    for module in modules:
        result = unduplicateModuleContents(module['id'])
        if not result:
            print(('The module ({}) does not contain any duplicate items').format(module['name']))
        else:
            print(('Done revising the module ({})').format(module['name']))

    print('\n')


def MasterRAP():
    print('****Restoring all pages to their first version****')
    pages = API.getAllPages()
    if pages == []:
        print('No Pages found in course')
    else:
        for page in pages:
            API.revertToPageRevision(page['url'], 1)
            print(('[restorePage] Restored - {}').format(page['title']))


def deleteUnpublishedPages():
    print('****Deleting all unpublished pages****')
    unpublished_pages = API.getAllUnpublishedPages()
    if unpublished_pages == []:
        print('No unpublished pages found')
    else:
        for unpublished_page in unpublished_pages:
            print(unpublished_page['title'])
            API.deletePage(unpublished_page['url'])