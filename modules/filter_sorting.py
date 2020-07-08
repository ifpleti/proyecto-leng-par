def user_filter(hosting):
    sort_decision = input("Que tipo de ordenamiento desea:\n1.Precio 2.Servicio")
    if(sort_decision == 3):
        cota_inferior = input("Cota inferior?:")
        cota_superior = input("Cota superior?:")
        sorted_hosting = filter(lambda x: cota_inferior > x.total_price > cota_superior,hosting)
        sorted_hosting = sorted(sorted_hosting, key=lambda x: x.total_price)
    elif(sort_decision == 2):
        service_list = []
        for services in hosting:
            for service in services:
                if (service not in service_list):
                    service_list.append(service)

        new_data = [list(service) for service in set([tuple(services) for services in hosting])]

    
    #    sorted_hosting = filter(lambda x: x.service )
    #    s
        
        
    #Por servicio
    #Categoria alfabeticamente
    #Rating
    #Precio