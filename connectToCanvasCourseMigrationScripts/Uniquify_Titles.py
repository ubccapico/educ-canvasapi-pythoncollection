# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Uniquify_Titles.py
import Init, API_Calls as API, re

def getCoreNames(names, ugly_names):
    canvas_extension = re.compile('-[0-9]+')
    plain_ugly_names = []
    for uname in ugly_names:
        plain_ugly_names.append(canvas_extension.split(uname)[0])

    core_names = list(set(plain_ugly_names))
    if core_names != []:
        print('The following page titles are used for more than one page.')
        print(core_names)
        for core_name in core_names:
            if core_name not in names:
                core_names.remove(core_name)

    return core_names


def MasterUniquifyTitles():
    print('****Making all page titles unique****')
    names = []
    ugly_names = []
    pages = API.getAllPages()
    for page in pages:
        names.append(page['title'])

    reused_title_identifier = re.compile('.+?-[0-9]+')
    for name in names:
        if reused_title_identifier.match(name):
            ugly_names.append(name)

    core_names = getCoreNames(names, ugly_names)
    if core_names != []:
        canvas_extension = re.compile('-[0-9]+')
        module_identifier = re.compile('[^0-9]+[0-9]*')
        modules = API.getAllModules()
        for module in modules:
            module_items = API.getModuleItems(module['id'])
            for module_item in module_items:
                if module_item['type'] == 'Page':
                    stripped_title = canvas_extension.split(module_item['title'])[0]
                    if stripped_title in core_names:
                        module_partial_name = module_identifier.findall(module['name'])[0]
                        new_page_title = ('{} ({})').format(stripped_title, module_partial_name)
                        print(('({}) used to be ({})').format(new_page_title, module_item['title']))
                    page = API.updatePageTitle(module_item['page_url'], new_page_title)

    print('\n\n')