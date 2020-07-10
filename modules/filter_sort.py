### FILTERING
# servicios
# categoría
# rating
# precio total

### SORTING
# precio total
# rating
# nombre (alfabetico)



# def hosting_filter(hosting, category_input):
#     sort_variable = "Alfabeticamente"

#     sort_decision = input("Que tipo de ordenamiento desea:\n1.Precio 2.Servicio")
#     if(sort_decision == 3):
#         cota_inferior = input("Cota inferior?:")
#         cota_superior = input("Cota superior?:")
#         sorted_hosting = filter(lambda x: cota_inferior > x.total_price > cota_superior,hosting)
#         sorted_hosting = sorted(sorted_hosting, key=lambda x: x.total_price)
#     elif(sort_decision == 2):
#         service_list = []
#         for services in hosting:
#             for service in services:
#                 if (service not in service_list):
#                     service_list.append(service)

#         new_data = [list(service) for service in set([tuple(services) for services in hosting])]

############
# FILTRADO #
############

def hosting_filter(hosting, filter_type, filter_list, lower, upper):

    if filter_type == 1:
        hosting = service_filter(hosting, filter_list)

    if filter_type == 2:
        hosting = category_filter(hosting, filter_list)

    if filter_type == 3:
        hosting = rating_filter(hosting, lower, upper)

    if filter_type == 4:
        hosting = total_price_filter(hosting, lower, upper)

    return hosting
    
def service_filter(hosting, service_input): #pasar a funcional!
    filtered_host = []
    #Se agrega sin repeticion
    for host in hosting:
        contador = 0
        for asked_service in service_input:
            if((host.services.count(asked_service) >= 1)):
                contador += 1
        if(contador >= len(service_input)-1):
            filtered_host.append(host)
                    
    return filtered_host

def category_filter(hosting, category_input): #category_input es una lista
    filtered_categories = []
    for service in category_input:
        filtered_categories = filter(lambda x: x == category_input,hosting)
    return filtered_categories

def rating_filter(hosting, lower, upper):
    return filter(lambda x: lower > x.rating > upper, hosting)

def total_price_filter(hosting, lower, upper):
    return filter(lambda x: lower > x.total_price > upper, hosting)

################
# ORDENAMIENTO #
################

def hosting_sort(hosting, sort_type):

    if sort_type == 1:
        hosting = total_price_sort(hosting)

    if sort_type == 2:
        hosting = rating_sort(hosting)

    if sort_type == 3:
        hosting = name_sort(hosting)

    return hosting

    

def total_price_sort(hosting):
    sorted_hosting = sorted(hosting, key=lambda x: x.total_price)

    return hosting


def rating_sort(hosting):
    return hosting


def name_sort(hosting):
    return hosting