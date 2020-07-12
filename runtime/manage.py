from .modules.airbnb_scraping import airbnb_scrape
from .modules.utils import time_format, save_object_list
from .modules.expedia_scraping import get_offers
import time


def manage_search(city, checkin, checkout, rooms, adults, children, babies):

    hosting = [] # Aquí residirán TODOS los resultados

    total_start_time = time.time()

    ### Airbnb scraping ###
    start_time = time.time()
    airbnb_hosting_list = airbnb_scrape(city, checkin, checkout, rooms, adults, children, babies)
    airbnb_execution_time = (time.time() - start_time)
    for object in airbnb_hosting_list:
        hosting.append(object)

    ### Expedia scraping ###
    # start_time = time.time()
    # expedia_hosting_list = get_offers(city, checkin, checkout, rooms, adults, children, babies)
    # expedia_execution_time = (time.time() - start_time)
    # for object in expedia_hosting_list:
    #     hosting.append(object)

    ### imprimir resultados ###
    print("\nairbnb scraping | "+time_format(airbnb_execution_time)+" | "+str(len(airbnb_hosting_list))+" resultados")
    # print("\nexpedia scraping | "+time_format(expedia_execution_time)+" | "+str(len(expedia_hosting_list))+" resultados")

    ### guardar alojamientos en generated.txt ###
    save_object_list(hosting, "generated.txt")



    total_execution_time = time.time() - total_start_time
    total_results = len(hosting)


    return time_format(total_execution_time)+" | "+str(total_results)+" resultados"

