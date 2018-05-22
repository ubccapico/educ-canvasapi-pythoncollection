# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Files_To_Pages.py
import API_Calls as API, urllib.request as req
from bs4 import BeautifulSoup
from Fix_Internal_Links import fixInternalLinks, getImageNameDuplicates
import Init
pageUrlHtmlList = []
processed_item_count = 0
total_item_count = 0
processed_item_count = 0
total_item_count = 0
recreated_modules = []
created_pages = []

def deleteAllHTMLFiles():
    print('****Deleting all HTML files from course****')
    all_html_files = API.getAllFiles('text/html')
    print(('Found {} files to delete. This will take approximately {} minutes.').format(len(all_html_files), len(all_html_files) / 100))
    deleted_file_count = 0
    for file in all_html_files:
        API.deleteFile(file['id'])
        deleted_file_count += 1

    print(('[deleteAllHTMLFiles] {} files were deleted').format(deleted_file_count))


class pageUrlHtml(object):

    def __init__(self, url, html):
        self.url = url
        self.html = html

    def __repr__(self):
        return str(self.__dict__)


def getHtmlBody(file_url):
    response = req.urlopen(file_url)
    html_raw = response.read()
    response.close()
    soup = BeautifulSoup(html_raw, 'html.parser')
    head = soup.find('head')
    if head:
        head.extract()
    body = str(soup)
    return body


def createReversionedModule(module_name, module_position, module_items):
    new_module = API.createModule(module_name, module_position)
    API.publishModule(new_module['id'])
    recreated_modules.append(new_module['name'])
    for item in module_items:
        created_module_item = API.createModuleItem(new_module['id'], item)
        if (item['published'] is True) or (item['type'] == 'SubHeader'):
            API.publishModuleItem(new_module['id'], created_module_item['id'])
    return


def reversionModule(module_ID):
    global created_pages
    global processed_item_count
    old_module = API.getModule(module_ID)
    old_module_name = old_module['name']
    module_items = API.getModuleItems(old_module['id'])
    if module_items:
        new_module_flag = 0
        module_items_count = len(module_items)
        for n in range(module_items_count):
            processed_item_count += 1
            if module_items[n]['type'] == 'File':
                file = API.getFile(module_items[n]['content_id'])
                if file['content-type'] == 'text/html':
                    print(('Converted HTML File - Title: {}').format(module_items[n]['title']))
                    page_body = getHtmlBody(file['url'])
                    page = API.createPage(page_title=module_items[n]['title'], page_body=page_body)
                    created_pages.append([page['title'], old_module_name])
                    pageUrlHtmlList.append(pageUrlHtml(page['url'], file['display_name']))
                    page_changes = {'position':module_items[n]['position'],  'indent':module_items[n]['indent'], 
                     'page_url':page['url'], 
                     'type':'Page', 
                     'published':module_items[n]['published']}
                    page.update(page_changes)
                module_items[n] = page
                new_module_flag = 1

        if new_module_flag == 1:
            Init.pageUrlHtmlList = pageUrlHtmlList
            createReversionedModule(old_module['name'], old_module['position'], module_items)
            API.deleteModule(module_ID)
            print(('MODULE {} has been recreated').format(old_module['name']))
        else:
            print(('MODULE {} contains no HTML files => No modifications necessary').format(old_module['name']))
        return


def traverseCourseFTP():
    print('****Converting HTML Files in modules to Canvas content pages****')
    modules = API.getAllModules()
    for module in modules:
        reversionModule(module['id'])

    print('\n\n')


def MasterFTP():
    print('Checking for images with repeated names before commencing FTP... If no duplicates are found, the program will continue without prompting the user.')
    duplicate_data = getImageNameDuplicates()
    traverseCourseFTP()
    deleteAllHTMLFiles()
    fixInternalLinks(duplicate_data)