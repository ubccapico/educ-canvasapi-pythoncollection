# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Fix_Internal_Links.py
import API_Calls as API
from bs4 import BeautifulSoup
import Init, unidecode

def getImageNameDuplicates():
    images = API.getAllFiles('image')
    image_names = []
    unique_image_names = []
    duplicate_image_names = []
    duplicate_image_inclusion = '0'
    for image in images:
        image_names.append(image['display_name'])

    for image_name in image_names:
        if image_name not in unique_image_names:
            unique_image_names.append(image_name)
        else:
            unique_image_names.remove(image_name)
            duplicate_image_names.append(image_name)
            break

    if duplicate_image_names != []:
        while True:
            duplicate_image_inclusion = input(("The following duplicate image names were found in your course:\n{}\nThe link fixer cannot distinguish between different images with the same name.\nSelect one:\n1. Remove listed images\n2. Include listed imagees - ONLY IF: They are identical and don't need to be distinguished\n3. Don't fix any image links\n").format(duplicate_image_names))
            if duplicate_image_inclusion == '1':
                print('Images with duplicate names will not be automatically fixed. You can manually fix them using the course link validator.\n')
                break
            elif duplicate_image_inclusion == '2':
                print('Images with duplicate names will be included in the link fixer.\n')
                break
            elif duplicate_image_inclusion == '3':
                print('The link fixer will not attempt to fix any images.\n')
                break
            else:
                print('Invalid Input. Please enter one of the specified digit choices.\n')

    return (duplicate_image_inclusion, duplicate_image_names)


def fixInternalLinks(duplicate_data=None):
    print('****FIXING INTERNAL LINKS****')
    pages = API.getAllPages()
    files = API.getAllFiles('')
    images = API.getAllFiles('image')
    if duplicate_data == None:
        buffer = getImageNameDuplicates()
        duplicate_image_inclusion = buffer[0]
        duplicate_image_names = buffer[1]
    else:
        duplicate_image_inclusion = duplicate_data[0]
        duplicate_image_names = duplicate_data[1]
    if duplicate_image_inclusion == '1':
        print('Removing images with repeated names from the fixing list.')
        for image in images:
            if image['display_name'] in duplicate_image_names:
                images.remove(image)

    else:
        if duplicate_image_inclusion == '2':
            print('Continuing without removing duplicate images.')
        else:
            if duplicate_image_inclusion == '3':
                print('Link fixer will not attempt to fix any images.')
                images = []
        previewable_types = ['doc', 'odt', 'sxi', 'docx', 'pdf', 'sxw', 'odf', 'ppt', 'xlsx', 'odg', 'pptx', 'xls', 'odp',
         'rtf', 'txt', 'ods', 'sxc']
        processed_item_count = 0
        for page in pages:
            processed_item_count += 1
            body = API.getPage(page['url'])['body']
            image_flag, file_flag, page_flag = (False, False, False)
            if body is not None:
                soup = BeautifulSoup(body, 'html.parser')
                aTags = soup.findAll('a', href=True)
                if aTags:
                    for aTag in aTags:
                        decoded_href = aTag['href'].replace('%20', ' ')
                        for pageUrlHtml in Init.pageUrlHtmlList:
                            aTagtextToUrl = unidecode.unidecode(aTag.get_text().replace(' ', '-').lower())
                            if pageUrlHtml.html in decoded_href or aTagtextToUrl == pageUrlHtml.url:
                                page_flag = True

                        for file in files:
                            if file['display_name'] in decoded_href:
                                print(('Match(file) - {}').format(file['display_name']))
                                file_flag = True
                                for type in previewable_types:
                                    if type in file['content-type']:
                                        aTag['class'] = 'instructure_file_link instructure_scribd_file'

                                aTag['href'] = ('https://canvas.ubc.ca/courses/{}/files/{}/download').format(Init.Short_Course_ID, file['id'])
                                aTag['title'] = file['display_name']

                imageTags = soup.findAll('img', src=True)
                if imageTags:
                    for img in imageTags:
                        decoded_image = img['src'].replace('%20', ' ')
                        for image in images:
                            if image['display_name'] in decoded_image:
                                print(('Match(Image) - {}').format(image['display_name']))
                                image_flag = True
                                img['src'] = ('https://canvas.ubc.ca/courses/{}/files/{}/preview').format(Init.Short_Course_ID, image['id'])

                body = str(soup)
                if file_flag == True or image_flag == True or page_flag == True:
                    API.updatePageBody(page['url'], body)

        print('\n\n')