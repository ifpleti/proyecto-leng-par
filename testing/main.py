from modules.airbnb_scraping import scrape

def main():

    city = "Viña del Mar"
    checkin = "2020-06-29"
    checkout = "2020-06-30"
    adults = 2
    children = 2
    babies = 1

    scrape(city, checkin, checkout, adults, children, babies)

if __name__ == "__main__":
    main()