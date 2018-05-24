# connect-canvas-migration-scripts

Language: Python and CanvasAPI

Developer: Ghazi Alchammat - alchammatg@gmail.com

### Introduction:

This repository contains a collection of Python scripts that leverage the Canvas API to automate multiple elements of the Connect to Canvas course migration process. The main way to operate the scripts is by editing and launching the file Main.py. All API calls are made through the API_Calls file which is imported to other files and used by the name API. For example, when you call tokenLogin() from Main.py, tokenLogin() calls API.testToken() which it has access to by importing the API_Calls module with the overwritten name API.


### Main.py:

This file contains a collection of imports from the rest of the files in this repository. Here, you can queue up various functions to be performed on a course in sequence. You can even modify the code to queue up many courses for modification.

### Init.py:

Before you can interact with the Canvas API, your access token needs to be stored in Init.Access_Token Variable. *You can store your token by calling the tokenLogin() function through Main.py*. To interact with a course, its short course ID needs to be store in Init.Short_Course_ID. *You can store a course ID by calling enterCourse() through Main.py*.

### API_Calls.py:

Using the library *requests*, API calls are made to the Canvas API through a collection of small functions in this file.

****************************************************************************************************************************
***All the remaining files except Services.py contain one Master function which I have imported directly into Main.py. Services.py contains four Master functions, which you can call in Main by entering Services.{FunctionName}***

### Login.py

Prompts the user to enter their Canvas API Access Token and performs a basic varification by testing an API call with the token for errors, then stores the token in the variable Init.Access_Token.

### Enter_Course.py

Prompts the user to enter a Course ID and performs a basic varification by testing an API call with the Course ID for errors, then stores the Course ID in the variable Init.Course_ID.

### Files_To_Pages.py

Scans all course modules for HTML file attatchments. If atleast one HTML attatchment is found in the module, all HTML files in the module get converted to Canvas Wiki Pages, and the module gets recreated to include the Wiki Pages. The old modules get deleted as well as all HTML files that were detected.

### Clean_Pages.py

Strips all pages from certain undesirable elements that carry over from Connect.

### Fix_Internal_Links.py

Fixes internal links that follow the Connect convention and don't work in Canvas. This is possible because the old convention includes the file name in the URL. Through the API, this file searches Canvas for file names identified in these URLs, and replaces the broken links to ones with the identified file IDs.

### Modulate.py

Prompts the user to enter the name of a module to be broken up, or enter "NONE" to skip. Next, it either exits or prompts the user with 2 possible ways to breakup a module. 1: Indiscriminate - makes a new module for each module item detected. 2: By SubHeader - Creates a new module for every identified subheader to contain all items found between that subheader and the next subheader. Subheaders must have the indent level 0 to work.

### Uniquify_Titles.py

Looks through the entire modules page for instances where Canvas has automatically renamed a duplicate-title page such as (Readings, Readings-1, Readings-2..). For each instance found, looks for "Module/Week" information in the module name to rename the pages with the following convention (Readings (Week 1), Readings (Week 2)...).

### Services.py

Contains four master functions.

**MasterUMC()** - Searches all modules for items with duplicate names. If any duplicates are detected, only the first instance is kept and the following ones are deleted from the module.

**MasterRAP()** - Restores all wiki pages to their 1st version.

**MasterDeleteUnpublishedPages()** - Deletes all unpublished wiki pages.

**MasterOpenLinksInNewTabs()** - Makes all external link attatchment module items open in new tabs.
