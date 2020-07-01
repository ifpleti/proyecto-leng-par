from modules.airbnb_scraping import scrape
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

    scrape(city, checkin, checkout, rooms, adults, children, babies)

    print("--- %s segundos ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()