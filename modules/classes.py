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
            "nombre de la oferta: "+self.name
            +"\nlugar: "+self.location
            +"\nurl: "+self.url
            +"\ncategoría: "+self.category
            +"\nhabitaciones: "+str(self.rooms)
            +"\nservicios: "+str(self.services)
            +"\nprecio por noche: "+str(self.nightly_price)
            +"\nprecio total: "+str(self.total_price)
            +"\ncalificación: "+str(self.rating)
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
            +"\nes superanfitrión: "+str(self.superhost)
            +"\ndescripción: "+self.description
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
            +"\nes opción popular: "+str(self.popular_choice)
            +"\n"
        )

        return text