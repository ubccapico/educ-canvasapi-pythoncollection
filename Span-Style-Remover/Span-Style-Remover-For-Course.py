########################################################################################################################
# Script Name: Span and Style Attribute Remover For Canvas Pages - Whole Course Version
#
# Developed by: Scott Beaulieu
#
# Contact Information: nicholassjbeaulieu@protonmail.com
#
# Description: Unwraps all span tags and removes all style attributes (in that order) for all pages in a Canvas course
########################################################################################################################


import requests
from bs4 import BeautifulSoup


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

def getFullListOfPages():
    fullList = []
    pagesRequest = requests.get(url + '/api/v1/courses/{}/pages'.format(courseID), params={'per_page': 100,
                                                                                           'order': 'asc',
                                                                                           'access_token': token})
    pages = pagesRequest.json()
    for page in pages:
        fullList.append(page)
    while pagesRequest.links['current']['url'] != pagesRequest.links['last']['url']:
        pagesRequest = requests.get(pagesRequest.links['next']['url'], params={'per_page': 100,
                                                                               'order': 'asc',
                                                                               'access_token': token})
        pages = pagesRequest.json()
        for page in pages:
            fullList.append(page)
    return fullList


def htmlStyleExterminator(pageObject):
    print("Removing span tags and inline styling.\n")
    htmlChangeFlag = 0
    page_html = pageObject['body']
    soup = BeautifulSoup(page_html, 'html.parser')
    while len(soup.find_all('span')) > 0:
        htmlChangeFlag = 1
        soup.span.unwrap()
    for tag in soup():
        if 'style' in tag.attrs:
            htmlChangeFlag = 1
            del tag.attrs['style']
    if htmlChangeFlag == 1:
        pageUpdate = requests.put(url + '/api/v1/courses/{}/pages/{}'.format(courseID, pageObject['url']),
                                  params={'access_token': token},
                                  data={'wiki_page[body]': str(soup)})
        print("!!!!!!!!!!!!Changes were made to the page \"{}\"!!!!!!!!!!!!\n\n".format(pageObject['title']))
    else:
        print("------------No changes made to page \"{}\"------------\n\n".format(pageObject['title']))
    return


url = urlSelection()
token = tokenLogin()
courseID = courseSelection()
pagesList = getFullListOfPages()
if pagesList != []:
    for page in pagesList:
        retrievedPage = (requests.get(url + '/api/v1/courses/{}/pages/{}'.format(courseID, page['url']),
                                      params={'access_token': token})).json()
        if retrievedPage['body'] and len(retrievedPage['body']) != 0:
            htmlStyleExterminator(retrievedPage)
print("\nInline styling and span tags have been successfully removed!")