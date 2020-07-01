from modules.airbnb_scraping import scrape
# from modules.trivago_scraping import foobar
import time

def main():

    city = "Viña del Mar"
    checkin = "2020-07-10"
    checkout = "2020-07-12"
    rooms = 2
    adults = 2
    children = 2
    babies = 1

    start_time = time.time()

    airbnb_hosting_list = scrape(city, checkin, checkout, rooms, adults, children, babies)

    # imprimir resultados
    for i in range(len(airbnb_hosting_list)):
        print(airbnb_hosting_list[i])
    print("\n"+str(len(airbnb_hosting_list))+" resultados de AirBnb obtenidos.")

    print("en %s segundos ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()