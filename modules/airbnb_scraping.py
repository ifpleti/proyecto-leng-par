from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from .classes import AirbnbHosting
import threading
import json
import requests


def airbnb_scrape(city, checkin, checkout, rooms, adults, children, babies):

    while True:
        try:
            list_rows = search(city, checkin, checkout, adults, children, babies)
            break
        except:
            print("busqueda Airbnb fallida, reintentando...")
            pass

    

    ### FORMA PARALELA ###

    physical_threads = os.cpu_count()
    if physical_threads > 2:
        workers = physical_threads - 1
    else:
        workers = 1

    with ThreadPoolExecutor(max_workers = workers) as executor:
        hosting_thread = {executor.submit(refine, row, rooms): row for row in list_rows}

    hosting = []
    for row in as_completed(hosting_thread):
        try:
            item = row.result()
            hosting.append(item)
        except:
            pass
    
    ### FORMA SECUENCIAL ###

    # hosting = []
    # for row in list_rows:
    #     try:
    #         hosting_object = refine(row, rooms)
    #         hosting.append(hosting_object)
    #     except:
    #         pass

    # for i in range(len(hosting)):
    #     print(hosting[i])
    # print("\n"+str(len(hosting))+" resultados de AirBnb obtenidos.")

    return hosting

    
def search(city, checkin, checkout, adults, children, babies):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')

    chrome_options.add_argument('log-level=3')

    driver = webdriver.Chrome(options = chrome_options)
    wait = WebDriverWait(driver, 5)

    driver.get('https://www.airbnb.cl/')

    # lugar
    sleep(1)

    location_box = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@data-testid='structured-search-input-field-query']")))
    location_box.send_keys(city)

    # fecha de entrada
    checkin_button = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-field-split-dates-0']")))
    checkin_button.click()
    checkin_date = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@data-testid='datepicker-day-"+ checkin +"']")))
    checkin_date.click()

    # fecha de salida
    checkout_date = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@data-testid='datepicker-day-"+ checkout +"']")))
    checkout_date.click()

    # huespedes
    guests_button = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-field-guests-button']")))
    guests_button.click()

    add_adult = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-adults' and @aria-label='aumentar valor']/span")))
    for _ in range(adults):
        add_adult.click()

    add_child = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-children' and @aria-label='aumentar valor']/span")))
    for _ in range(children):
        add_child.click()

    add_babie = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-infants' and @aria-label='aumentar valor']/span")))
    for _ in range(babies):
        add_babie.click()

    # buscar
    search_button = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@class='_3h0uzoe']")))
    search_button.click()

    # lista obtenida por la busqueda
    result = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='_fhph4u']")))

    # pasar lista de elementos por beautifulsoup
    soup_all_results = BeautifulSoup(result.get_attribute("innerHTML"), "html.parser")
    list_rows = soup_all_results.find_all('div', { 'class': '_8ssblpx' })

    driver.quit()

    return list_rows

  
def refine(row, requested_rooms):

    # habitaciones igual o mayor habitaciones solicitadas
    rooms = row.find_all('div', { 'class': '_kqh46o' })[0].text.split(' · ')[1]
    rooms = int(rooms.replace(" ", "     ")[:3].replace(" ", ''))
    if(rooms < requested_rooms):
        exit()

    # extraer url
    url = "https://www.airbnb.cl" + row.find_all('a', href=True)[0]['href']

    # nombre
    name = row.find_all('div', { 'class': '_1c2n35az' })[0].text

    # categoría
    category = row.find_all('div', { 'class': '_167qordg' })[0].text.split(' en ')[0]

    # precio total
    total_price = row.find_all('button', { 'class': '_ebe4pze' })[0].text.replace("Total: $", '').replace('.', '').replace("Mostrar los detalles", '').replace("CLP", '')
    total_price = int(total_price)

    # superanfitrión
    if(row.find_all('div', { 'class': '_snufp9' })):
        superhost = True
    else:
        superhost = False

    # precio por noche
    nightly_price = row.find_all('span', { 'class': '_1p7iugi' })[0].text.replace("Precio:", '').replace("  CLP por noche", '').replace('.','').replace("CLP", '')
    i = len(nightly_price)-1
    while(nightly_price[i] != '$'):
        i = i-1
    nightly_price = int(nightly_price[i:].replace("$", ''))

    # rating
    if(row.find_all('span', { 'class': '_10fy1f8' })):
        rating = float(row.find_all('span', { 'class': '_10fy1f8' })[0].text.replace(",", "."))
    else:
        rating = None


    ###########################################################################
    # extraer descripción, lugar y servicios (requiere entrar al alojamiento) #
    ###########################################################################

    hosting_result = hosting_request(url)
    description = hosting_result[0]
    location = hosting_result[1]
    services = hosting_result[2]


    new_hosting = AirbnbHosting(name, location, category, rooms, services, nightly_price, total_price, rating, superhost, description, url)

    return new_hosting

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
        # ('variables', '{"request":{"id":"'+url[28:][:8]+'","layouts":["SIDEBAR","SINGLE_COLUMN"],"translateUgc":false,"preview":false,"bypassTargetings":false,"displayExtensions":null,"checkIn":"'+checkin+'","checkOut":"'+checkout+'","adults":"'+str(adults)+'","children":"'+str(children)+'","infants":"'+str(babies)+'"}}'),
        ('variables', '{"request":{"id":"'+url[28:][:8]+'","layouts":["SIDEBAR","SINGLE_COLUMN"],"translateUgc":false,"preview":false,"bypassTargetings":false,"displayExtensions":null}}'),
        ('extensions', '{"persistedQuery":{"version":1,"sha256Hash":"9b024d3a9845a2f383895666e149c60f3552534722376c5df84c237e4a3a353e"}}'),
    )

    data = requests.get('https://www.airbnb.cl/api/v3/PdpPlatformSections', headers=headers, params=params)
    loaded_data = json.loads(data.text)

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

