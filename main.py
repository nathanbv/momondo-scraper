from selenium import webdriver
from time import sleep
from copy import deepcopy
from date_time import Date, Time
from flight import Flight
from pprint import pprint

# Parameters
departure = 'PAR'
arrival = 'TPE'
dep_date_min = '01-01-2018'
dep_date_max = '02-01-2018'
ret_date_min = '10-01-2018'
ret_date_max = '11-01-2018'
length_min = '9'
length_max = '20'
direct = 'false'

path_to_chromedriver = '/Users/Nathan/Nextcloud/Git_Dev/momondo-scraper/chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

# Initialize
TripType = '&TripType=2'
SegNo = '&SegNo=2'
SO0 = '&SO0='
SD0 = '&SD0='
SDP0 = '&SDP0='
SO1 = '&SO1='
SD1 = '&SD1='
SDP1 = '&SDP1='
AD = '&AD=1'
TK = '&TK=ECO'
DO = '&DO='
NA = '&NA=false'

# Update with parameters
SO0 += departure
SD0 += arrival
SO1 += arrival
SD1 += departure
DO += direct

def forEachDepartureDate():
    global results, everyReturnCombination
    dep_date = Date(str(dep_date_min))
    while not dep_date.exceeds(dep_date_max):
        forEachReturnDate(dep_date)
        results.append(deepcopy(everyReturnCombination))
        pprint(everyReturnCombination)
        dep_date.incDay()

def forEachReturnDate(dep_date):
    global everyReturnCombination, scrapedFlight
    everyReturnCombination = []
    ret_date = Date(str(ret_date_min))
    while not ret_date.exceeds(ret_date_max):
        createUrl(dep_date, ret_date)
        scrapedFlight.departure = dep_date
        scrapedFlight.arrival =ret_date
        print scrapedFlight
        everyReturnCombination.append(deepcopy(scrapedFlight))
        ret_date.incDay()

def createUrl(dep_date, ret_date):
    print str(dep_date), '>', str(ret_date)
    SDP0 = '&SDP0=' + str(dep_date)
    SDP1 = '&SDP1=' + str(ret_date)
    url = 'https://www.momondo.fr/flightsearch?Search=true'
    url += TripType + SegNo + SO0 + SD0 + SDP0 + SO1 + SD1 + SDP1 + AD + TK + DO + NA
    scrap(url)

def isSearchFinished():
    try:
        searchStatus = browser.find_element_by_xpath('//*[@id="searchProgressText"]')
        if 'Recherche termin' in searchStatus.text:
            return True
        else:
            return False
    except:
        return False

def scrap(url):
    global scrapedFlight
    browser.get(url)
    while not isSearchFinished():
        sleep(1)

    element = browser.find_element_by_xpath('//*[@id="flight-tickets-sortbar-cheapest"]/div/span[2]/span[1]')
    scrapedFlight.cheapest_price = int(element.text)
    element = browser.find_element_by_xpath('//*[@id="flight-tickets-sortbar-cheapest"]/div/span[3]')
    scrapedFlight.cheapest_duration = Time(element.text)
    element = browser.find_element_by_xpath('//*[@id="uiBestDealTab"]/span[2]/span[1]')
    scrapedFlight.bestdeal_price = int(element.text)
    element = browser.find_element_by_xpath('//*[@id="uiBestDealTab"]/span[3]')
    scrapedFlight.bestdeal_duration = Time(element.text)
    #print scrapedFlight.price
    #print scrapedFlight.duration

dep_date_min = Date(dep_date_min)
dep_date_max = Date(dep_date_max)
ret_date_min = Date(ret_date_min)
ret_date_max = Date(ret_date_max)
global results, everyReturnCombination, scrapedFlight
results = []
everyReturnCombination = []
scrapedFlight = Flight()
if "__main__" == __name__:
    forEachDepartureDate()
    print 'Done.'
    pprint(results)
    quit()
