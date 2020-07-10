from modules.airbnb_scraping import airbnb_scrape
from modules.utils import time_format, save_object_list
from modules.expedia_scraping import get_offers
from modules.filter_sort import hosting_filter, hosting_sort
import time

def main():

    city = "Viña del Mar"
    checkin = "2020-07-10"
    checkout = "2020-07-12"
    rooms = 2
    adults = 2
    children = 2
    babies = 1

    category = 'M'



    hosting = [] # Aquí residirán TODOS los resultados

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


    ### filtering ###
    filter_type = 1 # 1=servicios 2=categoria 3=rating 4=preciototal
    filter_list = ['Wifi', 'Zona para trabajar con computadoras portátiles.', 'TV por cable', 'Plancha', 'Secadora', 'TV', 'Lavadora']
    lower = None
    upper = None
    filtered_hosting = hosting_filter(hosting, filter_type, filter_list, lower, upper)
    save_object_list(filtered_hosting, "genfiltered.txt")


    #### LISTAR SET DE SERVICIOS ####
    # services_set = set()
    # for i in hosting:
    #     for j in i.services:
    #         services_set.add(j)

    # services_list = list(services_set)
    # services_list.sort()
    # print(services_list)


if __name__ == "__main__":
    main()
