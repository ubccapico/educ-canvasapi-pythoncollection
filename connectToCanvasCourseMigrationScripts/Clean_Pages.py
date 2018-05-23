# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Clean_Pages.py
from Modulate import MasterModulate
from Uniquify_Titles import MasterUniquifyTitles
import API_Calls as API, Init
from bs4 import BeautifulSoup
import re
changes_flag = 0
page_log = {}
clean_pages_log = [
 '*********************', '*CLEAN PAGES RESULTS*', '*********************']

def encodingReplacements(body):
    newBody = body.replace('Ã©', 'é').replace('Ã', 'É').replace('â', "'").replace('Ã®', 'î').replace('Ã¨', 'è').replace('Ã ', 'à').replace('Ã§', 'ç').replace('Ãª', 'ê').replace('â', '–')
    return newBody


def stripBborderSpace(input_string):
    global changes_flag
    global page_log
    border_blacklist = [
     '<br/>', '<p></p>', '<div></div>', '<h1></h1>', '<h2></h2>', '<h3></h3>', '<p><a></a></p>',
     '<p><br/><br/></p>', '<p><br/></p>']
    from_top = []
    from_bot = []
    soup = BeautifulSoup(input_string, 'html.parser')
    if soup:
        while 1:
            try:
                first_element = soup.find()
                first_element_join = ('').join(str(first_element).split())
            except:
                break

            if first_element_join in border_blacklist:
                from_top.append(str(first_element))
                first_element.extract()
                if changes_flag != 1:
                    changes_flag = 1
                else:
                    break

        while 1:
            try:
                last_element = soup.find_all()[-1]
                last_element_join = ('').join(str(last_element).split())
            except:
                break

            if last_element_join in border_blacklist:
                from_bot.append(str(last_element))
                last_element.extract()
                changes_flag = changes_flag != 1 and 1
            else:
                break

    if from_top != [] or from_bot != []:
        result_string = [
         ('{} empty line(s) removed from top of html body.').format(len(from_top)), ('{} empty line(s) removed from bottom of html body.').format(len(from_bot))]
        page_log['stripBborderSpace'] = result_string
        body = str(soup)
    else:
        body = input_string
    return body


def removeHieroglyphs(input_string):
    global changes_flag
    undesirable_elements = [
     '�', '/*&lt;![CDATA[*/', '/*]]&gt;*/']
    found_undesirable_elements = []
    output_string = input_string
    for undesirable_element in undesirable_elements:
        if undesirable_element in output_string:
            output_string = output_string.replace(undesirable_element, '')
            found_undesirable_elements.append(undesirable_element)
            changes_flag = changes_flag != 1 and 1

    if found_undesirable_elements != []:
        result_string = [
         'The following undesirable elements were stripped:', str(found_undesirable_elements)]
        page_log['removeHieroglyphs'] = result_string
    return output_string


def textifyHeaders(input_string):
    global changes_flag
    textified_headers = []
    soup = BeautifulSoup(input_string, 'html.parser')
    imageTags = soup.find_all('img', src=True, alt=True)
    if imageTags:
        for img in imageTags:
            if 'https://connect.ubc.ca/bbcswebdav/xid' in img['src'] or 'Course_Templates/icons' in img['src']:
                if img['alt']:
                    img.replaceWith(BeautifulSoup('<h2>' + img['alt'] + '</h2>', 'html.parser'))
                    textified_headers.append(img['alt'])
                    changes_flag = changes_flag != 1 and 1

    if textified_headers != []:
        result_string = [
         'Headers with the following alt text(s) were converted:', str(textified_headers)]
        page_log['textifyHeaders'] = result_string
        body = str(soup)
    else:
        body = input_string
    return body


def divs2Heads(input_string):
    global changes_flag
    replacement_headings = []
    soup = BeautifulSoup(input_string, 'html.parser')
    divs = soup.find_all('div', id=True, class_=True)
    if divs:
        for div in divs:
            if div['id'] == 'imgheading':
                heading_text = str(div.text).strip()
                heading = BeautifulSoup(('<h2>{}</h2>').format(heading_text), 'html.parser')
                div.replaceWith(heading)
                replacement_headings.append(str(heading))
                changes_flag = changes_flag != 1 and 1

    if replacement_headings != []:
        result_string = [
         'The following headings were used to replace header-divs in the page:', str(replacement_headings)]
        page_log['divs2Heads'] = result_string
        body = str(soup)
    else:
        body = input_string
    return body


def stripRepeatedElements(input_string):
    global changes_flag
    extracted_elements = []
    soup = BeautifulSoup(input_string, 'html.parser')
    soup_element_parameters_list = [
     (
      'div', {'id': 'footer'}), ('a', {'name': 'top'}), ('div', {'class': 'print'}), ('a', {'href': '#top'})]
    for element_parameters in soup_element_parameters_list:
        found_elements = soup.find_all(*element_parameters)
        if found_elements:
            if changes_flag != 1:
                changes_flag = 1
            for found_element in found_elements:
                found_element.extract()
                extracted_elements.append(str(found_element))

    if extracted_elements != []:
        body = str(soup)
    else:
        body = input_string
    page_number_regex = re.compile('\\| Page .*? of .*?', re.I | re.M)
    page_number_matches = page_number_regex.findall(body)
    if page_number_matches != []:
        body = page_number_regex.sub('', body)
        extracted_elements.append(str(page_number_matches))
        if changes_flag != 1:
            changes_flag = 1
    if extracted_elements != []:
        result_string = [
         'The following repeated elements were extracted from this page:', str(extracted_elements)]
        page_log['stripRepeatedElements'] = result_string
    return body


def unrepeatTitles(input_string, page_title):
    global changes_flag
    removed_h1s = []
    specific_title_key = re.compile('\\s\\(.+\\)')
    specific_title_component = specific_title_key.search(page_title)
    if specific_title_component:
        general_title = page_title.replace(specific_title_component.group(0), '')
    else:
        general_title = page_title
    soup = BeautifulSoup(input_string, 'html.parser')
    h1s = soup.find_all('h1')
    for h1 in h1s:
        if str(h1.string).strip() == general_title.strip():
            h1.extract()
            if changes_flag != 1:
                changes_flag = 1
            removed_h1s.append(str(h1))

    if removed_h1s != []:
        result_string = [
         'The following h1 element(s) matched the page title and was removed:', str(removed_h1s)]
        page_log['unrepeatTitles'] = result_string
        body = str(soup)
    else:
        body = input_string
    return body


def printAndLog(page_title):
    global clean_pages_log
    clean_pages_log.append(('Adjusted ({}) with the following modifications:').format(page_title))
    print(('Adjusted ({}) with the following modifications:').format(page_title))
    for function in page_log:
        clean_pages_log.append('**' + function)
        print('**' + function)
        for line in page_log[function]:
            clean_pages_log.append('****' + line)
            print('****' + line)

    clean_pages_log.append('')
    print('')


def runCleaningSequence(page):
    global changes_flag
    global page_log
    changes_flag = 0
    page_log = {}
    clean_body = page['body']
    clean_body = removeHieroglyphs(clean_body)
    clean_body = textifyHeaders(clean_body)
    clean_body = stripRepeatedElements(clean_body)
    clean_body = unrepeatTitles(clean_body, page['title'])
    clean_body = divs2Heads(clean_body)
    clean_body = stripBborderSpace(clean_body)
    clean_body = encodingReplacements(clean_body)
    if changes_flag == 1:
        API.updatePageBody(page['url'], clean_body)
        printAndLog(page['title'])


def MasterCleanPages():
    print('****Cleaning page content of all pages in course****')
    pages_list = API.getAllPages()
    if pages_list != []:
        for page_from_list in pages_list:
            page = API.getPage(page_from_list['url'])
            if len(page['body']) != 0:
                runCleaningSequence(page)

    print('\n\n')


def MasterClean():
    MasterModulate()
    MasterUniquifyTitles()
    MasterCleanPages()