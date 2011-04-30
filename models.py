from google.appengine.ext import db
import urllib

class Office(db.Model):
    name = db.StringProperty(required=True)
    address = db.StringProperty(required=True)
    city = db.StringProperty(required=True)
    state = db.StringProperty(required=True)
    zipcode = db.StringProperty(required=True)
    phone = db.StringProperty(required=True)
    location = db.GeoPtProperty(required=True)


    @staticmethod
    def getByName(name):
        correctedName = name.replace('@', 'at')
        return db.GqlQuery(
                    "SELECT * FROM Office WHERE name = :1",
                    correctedName).get()

    @staticmethod
    def getByAddress(address):
        return db.GqlQuery(
                    "SELECT * FROM Office WHERE address = :1",
                    address).get()
    @staticmethod
    def getByNameOrAddress(name, address):
        office = Office.getByName(name)
        if not office:
            office = Office.getByAddress(address)

        return office

    @staticmethod
    def getOrCreate(name, fulladdress, phone):
        correctedName = name.replace('@', 'at')
        (address, city, state) = [i.strip() for i in fulladdress.strip().splitlines()]
        zipcode = state.split(',').pop().strip()
        state = state.split(',')[0].strip()

        office = Office.getByNameOrAddress(name, address)
        if not office:
            loc = Office.getLatLong(fulladdress.replace('<br>',' '))
            location = db.GeoPt(loc[0], loc[1])

            office = Office(name=name, address=address, city=city, state=state,
                    zipcode=zipcode, phone=phone, location=location)
            office.put()

        return office


    @staticmethod
    def getLatLong(address):
        #TODO: move this method!
        # This function queries the Google Maps API geocoder with an
        # address. It gets back a csv file, which it then parses and
        # returns a string with the longitude and latitude of the
        # address.

        # This isn't an actual maps key, you'll have to get one
        # yourself.
        # Sign up for one here:
        # http://code.google.com/apis/maps/signup.html
        mapsKey = 'ABQIAAAAr6BUOLVQ0X0ArH9beuKMJBRODXfV2NoUKGsYEY85JGbStTNO0xQ9kGUGvYOYTgefVqOVcvnDXnu2fQ'
        mapsUrl = 'http://maps.google.com/maps/geo?q='

        # This joins the parts of the URL together into
        # one string.
        url = ''.join([mapsUrl,urllib.quote(address),'&output=csv&key=',mapsKey])

        # This retrieves the URL from Google,
        # parses out the longitude and latitude,
        # and then returns them as a string.
        coordinates = urllib.urlopen(url).read().split(',')
        coorText = (coordinates[2], coordinates[3])
        return coorText


class Doc(db.Model):
    name = db.StringProperty(required=True)
    gender = db.StringProperty(required=True)
    certification = db.StringProperty()
    residency = db.StringProperty()
    school = db.StringProperty()
    specialties = db.StringListProperty(required=True)
    office = db.ReferenceProperty(Office)

