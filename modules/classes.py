class Hosting():
    def __init__(self, name, location, url, category, rooms, services, nightly_price, total_price, rating):
        self.name = name
        self.location = location
        self.url = url
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
            +"\nURL: "+self.url
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
    def __init__(self, name, location, url, category, rooms, services, nightly_price, total_price, rating, superhost, description):
        super().__init__(name, location, url, category, rooms, services, nightly_price, total_price, rating)
        self.superhost = superhost
        self.description = description

    def __str__(self):
        text = (
            super().__str__()
            +"SUPERANFITRIÓN: "+str(self.superhost)
            +"\nDESCRIPCIÓN: "+self.description
            +"\n"
        )

        return text

class TrivagoHosting(Hosting):
    def __init__(self, name, location, url, category, rooms, services, nightly_price, total_price, rating, popular_choice):
        super().__init__(name, location, url, category, rooms, services, nightly_price, total_price, rating)
        self.popular_choice = popular_choice

    def __str__(self):
        text = (
            super().__str__()
            +"OPCIÓN POPULAR: "+str(self.popular_choice)
            +"\n"
        )

        return text