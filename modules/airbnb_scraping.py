from concurrent.futures import ThreadPoolExecutor, as_completed
from .classes import AirbnbHosting
import os, json, requests

def airbnb_scrape(city, checkin, checkout, rooms, adults, children, babies):
    tries = 1
    while True:
        try:
            first_extraction = search(city, checkin, checkout, rooms, adults, children, babies)
            break
        except:
            tries += 1
            if tries == 3:
                return None
            print("busqueda Airbnb fallida, reintentando...")
            pass

    with ThreadPoolExecutor(max_workers = os.cpu_count()) as executor:
        hosting_thread = {executor.submit(refine, row, rooms): row for row in first_extraction}

    hosting = []
    for row in as_completed(hosting_thread):
        try:
            item = row.result()
            hosting.append(item)
        except:
            pass

    return hosting

    
def search(city, checkin, checkout, rooms, adults, children, babies):

    loaded_data = search_request(city, checkin, checkout, adults, children, babies)

    extracted_total = []
    for dict in loaded_data['data']['dora']['exploreV3']['sections'][1]['items']:

        if dict['listing']['bedrooms'] != rooms:
            continue

        extracted_single = []

        search_id = str(loaded_data['data']['dora']['exploreV3']['metadata']['loggingContext']['federatedSearchId'])
        url = str(dict['listing']['id'])
        url = 'https://www.airbnb.cl/rooms/'+url+'?location='+city.replace(' ', '%20').replace('ñ', '%C3%')+'&adults='+str(adults)+'&children='+str(children)+'&infants='+str(babies)+'&checkin='+checkin+'&checkout='+checkout+'&previous_page_section_name=1000'+'&federated_search_id='+search_id
        extracted_single.append(url)

        name = dict['listing']['name']
        extracted_single.append(name)

        category = dict['listing']['roomAndPropertyType']
        extracted_single.append(category)

        if dict['listing']['id'] == 'true':
            superhost = True
        else:
            superhost = False
        extracted_single.append(superhost)

        rating = dict['listing']['avgRating']
        extracted_single.append(rating)

        nightly_price = int(dict['pricingQuote']['rate']['amount'])
        extracted_single.append(nightly_price)

        total_price = int(dict['pricingQuote']['price']['total']['amount'])
        extracted_single.append(total_price)

        extracted_single.append(rooms)


        extracted_total.append(extracted_single)

    return extracted_total

  
def refine(prev_extraction, rooms):

    url = prev_extraction[0]
    name = prev_extraction[1]
    category = prev_extraction[2]
    superhost = prev_extraction[3]
    rating = prev_extraction[4]
    nightly_price = prev_extraction[5]
    total_price = prev_extraction[6]

    new_extraction = extract_hosting(url) # escraping del sitio del hosting
    description = new_extraction[0]
    location = new_extraction[1]
    services = new_extraction[2]

    new_hosting = AirbnbHosting(name, location, category, rooms, services, nightly_price, total_price, rating, superhost, description, url)

    return new_hosting

def extract_hosting(url):

    loaded_data = hosting_request(url)

    for dict in loaded_data['data']['merlin']['pdpSections']['sections']:

        if dict['sectionId'] == 'DESCRIPTION_DEFAULT':
            description = dict['section']['htmlDescription']['htmlText']
            description = description.replace('<br />', '\n').replace('<br/>', '\n').replace('</b>', '').replace('<b>', '')

        if dict['sectionId'] == 'LOCATION_DEFAULT':
            location = dict['section']['subtitle']
            if location == None:
                for dict2 in dict['section']['seeAllLocationDetails']:
                    if dict2['id'] == 'neighborhood-seeAll_'+url[28:][:8]:
                        location = dict2['title']

        if dict['sectionId'] == 'AMENITIES_DEFAULT':
            services = []
            for dict2 in dict['section']['seeAllAmenitiesGroups']:
                if dict2['title'] != 'No incluidos':
                    for dict3 in dict2['amenities']:
                        services.append(dict3['title'])

    result = []
    result.append(description)
    result.append(location)
    result.append(services)

    return result

def search_request(city, checkin, checkout, adults, children, babies):
    headers = {
        'Device-Memory': '8',
        'DNT': '1',
        'X-Airbnb-GraphQL-Platform-Client': 'apollo-niobe',
        'X-CSRF-Token': 'V4$.airbnb.cl$ZNfgUoCZbLw$xBe6H1cUZpVZu4Hj6T0vEG1WTQrvh2jst2K571ET868=',
        'X-Airbnb-API-Key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
        'X-CSRF-Without-Token': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61',
        'Viewport-Width': '1858',
        'content-type': 'application/json',
        'accept': '*/*',
        'Referer': 'https://www.airbnb.cl/s/'+city.replace(' ', '-')+'/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&check_in='+checkin+'&check_out='+checkout+'&adults='+str(adults)+'&children='+str(children)+'&infants='+str(babies)+'&source=structured_search_input_header&search_type=autosuggest',
        'DPR': '1',
        'ect': '4g',
        'X-Airbnb-GraphQL-Platform': 'web',
    }
    params = (
        ('locale', 'es-XL'),
        ('operationName', 'ExploreSearch'),
        ('currency', 'CLP'),
        ('variables', '{"request":{"metadataOnly":false,"version":"1.7.6","itemsPerGrid":20,"tabId":"home_tab","refinementPaths":["/homes"],"checkin":"'+checkin+'","checkout":"'+checkout+'","adults":'+str(adults)+',"children":'+str(children)+',"infants":'+str(babies)+',"source":"structured_search_input_header","searchType":"autosuggest","query":"'+city+'","cdnCacheSafe":false,"simpleSearchTreatment":"simple_search_only","treatmentFlags":["monthly_stays_flexible_dates","stays_flexible_dates","simple_search_1_1"],"screenSize":"large"}}'),
        ('extensions', '{"persistedQuery":{"version":1,"sha256Hash":"8d443d1ee5488418c221b457c82cc185382822ba4eedcfafa57952c92c44b3c3"}}'),
    )
    data = requests.get('https://www.airbnb.cl/api/v3/ExploreSearch', headers=headers, params=params)
    return json.loads(data.text)

def hosting_request(url):
    headers = {
        'Device-Memory': '8',
        'DNT': '1',
        'X-Airbnb-GraphQL-Platform-Client': 'apollo-niobe',
        'X-CSRF-Token': 'V4$.airbnb.cl$OJPrvRpFt_Q$yltRj2wj8wqsi2A_8Cq3KmyfT3hecIyqkNoQWNAUNdk=',
        'X-Airbnb-API-Key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
        'X-CSRF-Without-Token': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58',
        'Viewport-Width': '1858',
        'content-type': 'application/json',
        'accept': '*/*',
        'Referer': url,
        'DPR': '1',
        'ect': '4g',
        'X-Airbnb-GraphQL-Platform': 'web',
    }
    params = (
        ('locale', 'es-XL'),
        ('operationName', 'PdpPlatformSections'),
        ('currency', 'CLP'),
        ('variables', '{"request":{"id":"'+url[28:][:8]+'","layouts":["SIDEBAR","SINGLE_COLUMN"],"translateUgc":false,"preview":false,"bypassTargetings":false,"displayExtensions":null}}'),
        ('extensions', '{"persistedQuery":{"version":1,"sha256Hash":"9b024d3a9845a2f383895666e149c60f3552534722376c5df84c237e4a3a353e"}}'),
    )
    data = requests.get('https://www.airbnb.cl/api/v3/PdpPlatformSections', headers=headers, params=params)
    return json.loads(data.text)
