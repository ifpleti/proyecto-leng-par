class Hosting():
    def __init__(self, name, location, category, rooms, services, nightly_price, total_price, rating):
        self.name = name
        self.location = location
        self.category = category
        self.rooms = rooms
        self.services = services
        self.nightly_price = nightly_price
        self.total_price = total_price
        self.rating = rating

    def __str__(self):
        text = (
            "NOMBRE: "+self.name
            +"\nLUGAR: "+self.location
            +"\nCATEGORÍA: "+self.category
            +"\nHABITACIONES: "+str(self.rooms)
            +"\nSERVICIOS: "+str(self.services)
            +"\nPRECIO POR NOCHE: "+str(self.nightly_price)
            +"\nPRECIO TOTAL: "+str(self.total_price)
            +"\nCALIFICACIÓN: "+str(self.rating)
            +"\n"
        )

        return text

class AirbnbHosting(Hosting):
    def __init__(self, name, location, category, rooms, services, nightly_price, total_price, rating, superhost, description, url):
        super().__init__(name, location, category, rooms, services, nightly_price, total_price, rating)
        self.superhost = superhost
        self.description = description
        self.url = url

    def __str__(self):
        text = (
            super().__str__()
            +"SUPERANFITRIÓN: "+str(self.superhost)
            +"\nDESCRIPCIÓN: "+self.description
            +"\nURL: "+self.url
            +"\n"
        )

        return text

class ExpediaHosting(Hosting):
    def __init__(self, name, location, category, rooms, services, nightly_price, total_price, rating, description, url):
        super().__init__(name, location, category, rooms, services, nightly_price, total_price, rating)
        self.description = description
        self.url = url

    def __str__(self):
        text = (
            super().__str__()
            +"DESCRIPCIÓN: "+self.description
            +"URL: "+self.url
            +"\n"
        )

        return text