
class Airport(object):
    airport = None
    image = None
    opening = None
    city = None
    passangers = None
    air_movements = None
    latitude = None
    longitude = None

    def __init__(self, airport, image, opening, city, passangers, air_movements):
        self.airport = airport
        self.image = image
        self.opening = opening
        self.city = city
        self.passangers = passangers
        self.air_movements = air_movements

    def coordinates(self, longitude, latitude): #longitude E/W, latitude S/N
        self.longitude = longitude
        self.latitude = latitude
