from ConfigParser import ConfigParser

class URL():
    def __init__(self, path_config_file):

        # Get config
        config_file = ConfigParser()
        config_file.read(path_config_file)
        departure = config_file.get('Airports', 'AirportOfDeparture')
        arrival = config_file.get('Airports', 'AirportOfArrival')
        nearby = config_file.get('Airports', 'AlsoSearchNearbyAirports')
        direct = config_file.get('FlightOptions', 'OnlyDirect')

        # Fixed
        self.TripType = '&TripType=2'
        self.SegNo = '&SegNo=2'
        self.AD = '&AD=1'
        self.TK = '&TK=ECO'

        # Set config
        self.SO0 = '&SO0=' + departure
        self.SD0 = '&SD0=' + arrival
        self.SO1 = '&SO1=' + arrival
        self.SD1 = '&SD1=' + departure
        self.DO = '&DO=' + direct
        self.NA = '&NA=' + nearby

        # Will be set later
        self.SDP0 = '&SDP0=04-07-2017'
        self.SDP1 = '&SDP1=28-03-1994'

    def __repr__(self):
        return 'URL '+str(self)

    def __str__(self):
        return self.getFullUrl()

    def setDates(self, dep_date, ret_date):
        print str(dep_date), '>', str(ret_date)
        self.SDP0 = '&SDP0=' + str(dep_date)
        self.SDP1 = '&SDP1=' + str(ret_date)

    def getFullUrl(self):
        url = 'https://www.momondo.fr/flightsearch?Search=true'
        url += self.TripType + self.SegNo + self.SO0 + self.SD0 + self.SDP0 + self.SO1 + self.SD1 + self.SDP1 + self.AD + self.TK + self.DO + self.NA
        return url

#TODO: Add every search parameter (1 way, 2 ways, multi-destination with only 2 segments)
#TODO: Add custum number of segments