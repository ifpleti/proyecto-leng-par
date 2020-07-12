def hosting_filter(hosting, filter_type, filter_list, lower, upper):

    if filter_type == 1:
        return service_filter(hosting, filter_list)

    elif filter_type == 2:
        return category_filter(hosting, filter_list)

    elif filter_type == 3:
        return rating_filter(hosting, lower, upper)

    elif filter_type == 4:
        return total_price_filter(hosting, lower, upper)
    

def service_filter(hosting, service_input): #pasar a funcional!
    new_hosting_list = []
    for host in hosting:
        for service in host.service:
            if(service in service_input):
                new_hosting_list.append(host)
                break
    return new_hosting_list

def category_filter(hosting, category_input): #category_input es una lista
    return filter(lambda x: x.category in category_input,hosting)


def rating_filter(hosting, lower, upper):
    return filter(lambda x: lower > x.rating > upper, hosting)

def total_price_filter(hosting, lower, upper):
    return filter(lambda x: lower > x.total_price > upper, hosting)

################
# ORDENAMIENTO #
################

def hosting_sort(hosting, sort_type):

    if sort_type == 1:
        return total_price_sort(hosting)

    if sort_type == 2:
        return rating_sort(hosting)

    if sort_type == 3:
        return category_sort(hosting)

def total_price_sort(hosting):
    return sorted(hosting, key=lambda x: x.total_price)


def rating_sort(hosting):
    return sorted(hosting, key=lambda x: x.rating)


def category_sort(hosting):
    return sorted(hosting, key=lambda x: x.category)