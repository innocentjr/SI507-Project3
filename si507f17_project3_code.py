from bs4 import BeautifulSoup
import unittest
import requests
import json
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!

###############################################
#Global variable definitions
###############################################

stateList = ['Arkansas', 'California', 'Michigan']
diction = {}
arkansas_natl_sites = []
california_natl_sites = []
michigan_natl_sites = []
NationalSites = {}
masterlist = {}
FILENAME = ['arkansas.csv', 'california.csv', 'michigan.csv']

###############################################
#Function definitions
###############################################
def collectObjects(masterlist):
    headers = ["Name", "Location", "Type", "Address", "Description"]
    for item in stateList:
        print('Now running through {}.'.format(item))
        poly=[]
        poly.append(headers)
        for park in NationalSites[item]:
            mono = []
            mono.append(park.name)
            mono.append(park.location)
            mono.append(park.type)
            mono.append(park.address)
            mono.append(park.description)
            poly.append(mono)
        masterlist[item] = poly

def writeLists(filelist, entry):
    with open(entry, "w", encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(filelist)

def valid(one, two):
    count = 0
    if two == '':
        count = 1
    if count == 1:
        three = " "
    else:
        three = two + ' ' + one
    if two == one:
        three = two
    else:
        three = two + ' ' + one
    return three

def validate(string):
    if string == None:
        return "None"
    else:
        return string

###############################################
#End of Function definitions
###############################################

######### PART 0 #########

# Write your code for Part 0 here.
try:
    with open("cats.html", "r") as f:
        cats = f.read()
except:
    cats = requests.get("http://newmantaylor.com/gallery.html").text

    with open("cats.html",'w') as f:
        f.write(cats) # more in the chapter on Files in textbook
        f.close()

cats_parse = BeautifulSoup(cats, 'html.parser')

for img in cats_parse.find_all('img'):
    print(img.get('alt', "No alternative text provided!"))

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.
home_page = "https://www.nps.gov/index.htm"

try:
    with open("nps_gov_data.html",'r') as f:
        main_page = f.read()
except:
    main_page = requests.get(home_page).text
    with open("nps_gov_data.html", 'w') as f:
        f.write(main_page)
        f.close

###############################################
#Create a dictionary with State Name and Link as Key-Value pair
###############################################

soup = BeautifulSoup(main_page, 'html5lib')
states = soup.find("ul", {"class":"dropdown-menu SearchBar-keywordSearch"}).find_all("a")
for x in states:
    diction[x.text] = x.get("href", "None")
    #print(diction)

# Get individual states' data...
base_url = "https://www.nps.gov/"
for item in stateList:
    try:
        with open(item.lower() + "_data.html", 'r') as f:
            state_page = f.read()
    except:
        complete_URL = base_url + diction[item]
        state_page = requests.get(complete_URL).text
        with open(item.lower() + "_data.html", 'w') as f:
            f.write(state_page)
            f.close()

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.

######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?
with open(stateList[0].lower() + "_data.html", 'r') as f:
    arkansas_soup = BeautifulSoup(f.read(), 'html5lib')
    f.close()

with open(stateList[1].lower() + "_data.html", 'r') as f:
    california_soup = BeautifulSoup(f.read(), 'html5lib')
    f.close()

with open(stateList[2].lower() + "_data.html", 'r') as f:
    michigan_soup = BeautifulSoup(f.read(), 'html5lib')
    f.close()

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...


## Define your class NationalSite here:
class NationalSite(object):

    def __init__(self, soup):
            self.location = validate(soup.find('h4').string)
            self.name = validate(soup.find('h3').find('a').string)
            self.type = validate(soup.find('h2').string)
            if self.type != None:
                self.type = str(self.type)
            self.description = soup.find('p').string
            if self.description == None:
                self.description = ""
            for bit in soup.select('a[href*="basicinfo"]'):
                self.information = bit.get('href', "None")

    def __str__(self):
            return "{} | {}".format(self.name, self.location)

    def get_mailing_address(self):
            state_info_page = requests.get(self.information).text
            information_soup = BeautifulSoup(state_info_page, 'html5lib')
            mailing_address_soup = information_soup.find('p', {"class":"adr"})
            streetAddress = mailing_address_soup.find('span', {"class":"street-address"})

            try:
                one = mailing_address_soup.find('span', itemprop=False).get_text().strip().replace('\n', ' ')
            except:
                one = mailing_address_soup.get_text().strip().replace('\n', ' ')
            try:
                two = streetAddress.get_text().strip().replace('\n', '/ ')
            except:
                two = mailing_address_soup.get_text().strip().replace('\n', ' ')

            #Validating the mailing list
            validation = valid(one, two)
            self.address = validation

            return self.address

    def __contains__(self, name):
        if name in self.name:
            return True
        else:
            return False




## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)

arkansas_natl_soup = arkansas_soup.find("ul", id="list_parks").find_all('li', {"class":"clearfix"})
california_natl_soup = california_soup.find("ul", id="list_parks").find_all('li', {"class":"clearfix"})
michigan_natl_soup = michigan_soup.find("ul", id="list_parks").find_all('li', {"class":"clearfix"})

arkansas = ['Arkansas', arkansas_natl_sites, arkansas_natl_soup]
california = ['California', california_natl_sites, california_natl_soup]
michigan = ['Michigan', michigan_natl_sites, michigan_natl_soup]

States = [arkansas, california, michigan]

for state in States:
    #print('Now running through {}.'.format(state[0]))
    for park in state[2]:
        park_Instance = NationalSite(park)
        park_Instance.get_mailing_address()
        state[1].append(park_Instance)
    #print('Finished with {}.'.format(state[0]))
    NationalSites[state[0]] = state[1]

collectObjects(masterlist)

writeLists(masterlist[stateList[0]], FILENAME[0])
writeLists(masterlist[stateList[1]], FILENAME[1])
writeLists(masterlist[stateList[2]], FILENAME[2])



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
