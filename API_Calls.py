# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: API_Calls.py
import requests, Init
baseURL = 'https://canvas.instructure.com/api/v1/courses/'

def testToken(token):
    accounts = requests.get('https://canvas.instructure.com/api/v1/course_accounts', params={'access_token': token})
    return accounts.json()


def testCourse(course_id):
    course = requests.get(baseURL + course_id, params={'access_token': Init.Access_Token})
    return course.json()


def getAccounts():
    accounts = requests.get('https://canvas.instructure.com/api/v1/course_accounts', params={'access_token': Init.Access_Token})
    return accounts.json()


def getCourse():
    course = requests.get(baseURL + Init.Course_ID, params={'access_token': Init.Access_Token})
    return course.json()


def getAllQuizzes():
    quizzes = requests.get(baseURL + ('{}/quizzes').format(Init.Course_ID), params={'access_token':Init.Access_Token,  'per_page':100})
    return quizzes.json()


def getAllFiles(file_type=''):
    file_set = []
    if file_type == '':
        parameters = {'access_token':Init.Access_Token, 
         'per_page':50}
    else:
        parameters = {'access_token':Init.Access_Token, 
         'per_page':50,  'content_types[]':file_type}
    buffer100 = requests.get(baseURL + ('{}/files/').format(str(Init.Course_ID)), params=parameters)
    raw = buffer100.json()
    for file in raw:
        file_set.append(file)

    while buffer100.links['current']['url'] != buffer100.links['last']['url']:
        buffer100 = requests.get(buffer100.links['next']['url'], params=parameters)
        raw = buffer100.json()
        for file in raw:
            file_set.append(file)

    return file_set


def getAllPages():
    page_set = []
    buffer100 = requests.get(baseURL + ('{}/pages/').format(str(Init.Course_ID)), params={'access_token':Init.Access_Token, 
     'per_page':50})
    raw = buffer100.json()
    for page in raw:
        page_set.append(page)

    while buffer100.links['current']['url'] != buffer100.links['last']['url']:
        buffer100 = requests.get(buffer100.links['next']['url'], params={'access_token':Init.Access_Token, 
         'per_page':50})
        raw = buffer100.json()
        for page in raw:
            page_set.append(page)

    return page_set


def getAllUnpublishedPages():
    page_set = []
    parameters = {'access_token':Init.Access_Token, 
     'per_page':50,  'published':False}
    buffer100 = requests.get(baseURL + ('{}/pages/').format(str(Init.Course_ID)), params=parameters)
    raw = buffer100.json()
    for page in raw:
        page_set.append(page)

    while buffer100.links['current']['url'] != buffer100.links['last']['url']:
        buffer100 = requests.get(buffer100.links['next']['url'], params=parameters)
        raw = buffer100.json()
        for page in raw:
            page_set.append(page)

    return page_set


def getAllModules():
    module_set = []
    buffer100 = requests.get(baseURL + ('{}/modules/').format(str(Init.Course_ID)), params={'access_token':Init.Access_Token, 
     'per_page':50})
    raw = buffer100.json()
    for module in raw:
        module_set.append(module)

    while buffer100.links['current']['url'] != buffer100.links['last']['url']:
        buffer100 = requests.get(buffer100.links['next']['url'], params={'access_token':Init.Access_Token, 
         'per_page':50})
        raw = buffer100.json()
        for module in raw:
            module_set.append(module)

    return module_set


def setHome():
    home = requests.put(baseURL + Init.Course_ID, params={'access_token':Init.Access_Token, 
     'course[default_view]':'syllabus'})
    return home.json()


def startLinkValidation():
    start = requests.post(baseURL + ('{}/link_validation').format(Init.Course_ID), params={'access_token':Init.Access_Token, 
     'course[default_view]':'syllabus'})
    return start.json()


def getModule(module_ID):
    module = requests.get(baseURL + ('{}/modules/{}').format(str(Init.Course_ID), str(module_ID)), params={'access_token': Init.Access_Token})
    return module.json()


def createModule(module_name, module_position):
    module = requests.post(baseURL + Init.Course_ID + '/modules', params={'access_token':Init.Access_Token, 
     'module[name]':module_name,  'module[position]':module_position})
    return module.json()


def publishModule(module_ID):
    module = requests.put(baseURL + ('{}/modules/{}').format(str(Init.Course_ID), str(module_ID)), params={'access_token':Init.Access_Token, 
     'module[published]':True})
    return module.json()


def deleteModule(module_ID):
    module = requests.delete(baseURL + ('{}/modules/{}').format(Init.Course_ID, module_ID), params={'access_token': Init.Access_Token})
    return module.json()


def getModuleItems(module_ID):
    item_set = []
    buffer100 = requests.get(baseURL + ('{}/modules/{}/items').format(str(Init.Course_ID), str(module_ID)), params={'access_token':Init.Access_Token, 
     'per_page':50})
    raw = buffer100.json()
    for item in raw:
        item_set.append(item)

    while buffer100.links['current']['url'] != buffer100.links['last']['url']:
        buffer100 = requests.get(buffer100.links['next']['url'], params={'access_token':Init.Access_Token, 
         'per_page':50})
        raw = buffer100.json()
        for item in raw:
            item_set.append(item)

    return item_set


def getModuleItem(module_ID, item_ID):
    moduleItem = requests.get(baseURL + ('{}/modules/{}/items/{}').format(str(Init.Course_ID), str(module_ID), str(item_ID)), params={'access_token': Init.Access_Token})
    return moduleItem.json()


def moveModuleItem(module_ID, item_ID, final_module_ID, indent, new_position):
    moduleItem = requests.put(baseURL + ('{}/modules/{}/items/{}').format(str(Init.Course_ID), str(module_ID), str(item_ID)), params={'access_token':Init.Access_Token, 
     'module_item[module_id]':str(final_module_ID),  'module_item[indent]':str(indent), 
     'module_item[position]':new_position})
    return moduleItem.json()


def createModuleItem(module_ID, item):
    parameters = {'access_token':Init.Access_Token, 
     'module_item[title]':item['title'],  'module_item[type]':item['type'], 
     'module_item[indent]':item['indent']}
    if item['type'] == 'SubHeader':
        pass
    else:
        if item['type'] == 'Page':
            parameters['module_item[page_url]'] = item['page_url']
        else:
            if item['type'] == 'ExternalUrl':
                parameters['module_item[external_url]'] = item['external_url']
                parameters['module_item[new_tab]'] = True
            else:
                parameters['module_item[content_id]'] = item['content_id']
            added_item = requests.post(baseURL + ('{}/modules/{}/items').format(Init.Course_ID, module_ID), params=parameters)
            return added_item.json()


def addPageToModule(module_ID, page_url, position, indent):
    added_page = requests.post(baseURL + ('{}/modules/{}/items').format(str(Init.Course_ID), str(module_ID)), params={'access_token': Init.Access_Token}, data={'module_item[type]':'Page',  'module_item[page_url]':page_url,  'module_item[position]':position,  'module_item[indent]':indent})
    return added_page.json()


def publishModuleItem(module_ID, item_ID):
    published_item = requests.put(baseURL + ('{}/modules/{}/items/{}').format(str(Init.Course_ID), str(module_ID), str(item_ID)), params={'access_token': Init.Access_Token},
      data={'module_item[published]': True})


def deleteModuleItem(module_ID, item_ID):
    deleted_item = requests.delete(baseURL + ('{}/modules/{}/items/{}').format(Init.Course_ID, module_ID, item_ID), params={'access_token': Init.Access_Token})


def getPage(page_URL):
    page = requests.get(baseURL + ('{}/pages/{}').format(str(Init.Course_ID), str(page_URL)), params={'access_token': Init.Access_Token})
    return page.json()


def createPage(page_title, page_body):
    page = requests.post(baseURL + ('{}/pages').format(Init.Course_ID), params={'access_token': Init.Access_Token},
      data={'wiki_page[published]':'true',  'wiki_page[title]':page_title,  'wiki_page[body]':page_body})
    return page.json()


def deletePage(page_url):
    page = requests.delete(baseURL + ('{}/pages/{}').format(Init.Course_ID, page_url), params={'access_token': Init.Access_Token})
    return page.json()


def updatePageTitle(page_URL, new_title):
    page = requests.put(baseURL + ('{}/pages/{}').format(str(Init.Course_ID), str(page_URL)), params={'access_token': Init.Access_Token},
      data={'wiki_page[title]': new_title})
    return page.json()


def updatePageBody(page_URL, new_body):
    page = requests.put(baseURL + ('{}/pages/{}').format(str(Init.Course_ID), str(page_URL)), params={'access_token': Init.Access_Token},
      data={'wiki_page[body]': new_body})
    return page.json()


def getPageRevisions(page_URL):
    revision = requests.get(baseURL + ('{}/pages/{}/revisions').format(Init.Course_ID, page_URL), params={'access_token': Init.Access_Token})
    return revision.json()


def revertToPageRevision(page_URL, revision_ID):
    revision = requests.post(baseURL + ('{}/pages/{}/revisions/{}').format(Init.Course_ID, page_URL, revision_ID), params={'access_token': Init.Access_Token})
    return revision.json()


def getFile(file_ID):
    file = requests.get(baseURL + ('{}/files/{}').format(str(Init.Course_ID), str(file_ID)), params={'access_token': Init.Access_Token})
    return file.json()


def deleteFile(file_ID):
    file = requests.delete('https://canvas.instructure.com/api/v1/' + ('files/{}').format(str(file_ID)), params={'access_token': Init.Access_Token})
    return file.json()


def resolvePath(dir):
    path = requests.get(baseURL + ('{}/folders/by_path/{}').format(Init.Course_ID, dir), params={'access_token': Init.Access_Token})
    return path.json()


def getAllFolders(dir=''):
    folders = requests.get(baseURL + ('{}/folders/{}/').format(Init.Course_ID, dir), params={'access_token': Init.Access_Token})
    return folders.json()


def getFolders(parentID):
    folders = requests.get(('https://canvas.instructure.com/api/v1/folders/{}/folders').format(parentID), params={'access_token': Init.Access_Token})
    return folders.json()


def getFolderImages(folderID):
    files = requests.get(('https://canvas.instructure.com/api/v1/folders/{}/files').format(folderID), params={'access_token':Init.Access_Token, 
     'content_types[]':'image'})
    return files.json()


def newTab(moduleID, itemID):
    result = requests.put(('https://canvas.instructure.com/api/v1/courses/{}/modules/{}/items/{}').format(Init.Course_ID, moduleID, itemID), params={'access_token':Init.Access_Token, 
     'module_item[new_tab]':True})
    return result.json()