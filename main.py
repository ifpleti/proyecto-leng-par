from modules.airbnb_scraping import airbnb_scrape
from modules.utils import time_format, save_object_list
from modules.trivago_scraping import search_trivago
import time

def main():

    city = "Viña del Mar"
    checkin = "2020-07-10"
    checkout = "2020-07-12"
    rooms = 2
    adults = 2
    children = 2
    babies = 1

    ### Airbnb scraping ###
    start_time = time.time()
    airbnb_hosting_list = airbnb_scrape(city, checkin, checkout, rooms, adults, children, babies)
    airbnb_execution_time = (time.time() - start_time)

    ### Trivago scraping ###
    start_time = time.time()
    # trivago_hosting_list = trivago_scrape(city, checkin, checkout, rooms, adults, children, babies)
    trivago_execution_time = (time.time() - start_time)

    ### Fusionar listas ###
    hosting = []
    for object in airbnb_hosting_list:
        hosting.append(object)
    # for object in trivago_hosting_list:
    #     hosting.append(object)

    ### imprimir resultados ###
    print("\nairbnb scraping | "+time_format(airbnb_execution_time)+" | "+str(len(airbnb_hosting_list))+" resultados")
    # print("\ntrivago scraping | "+time_format(trivago_execution_time)+" | "+str(len(trivago_hosting_list))+" resultados")

    ### guardar alojamientos en generated.txt ###
    save_object_list(hosting)

if __name__ == "__main__":
    main()