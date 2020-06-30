from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
from string import digits
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from .classes import Hosting

def scrape(city, checkin, checkout, adults, children, babies):

    result = search(city, checkin, checkout, adults, children, babies)

    soup_all_results = BeautifulSoup(result.get_attribute("innerHTML"), "html.parser")
    list_rows = soup_all_results.find_all('div', { 'class': '_8ssblpx' })

    ### Threading ###

    nthreads = os.cpu_count()
    if nthreads > 2:
        nthreads = nthreads - 1

    with ThreadPoolExecutor(max_workers = nthreads) as executor:
        hosting_thread = {executor.submit(refine, row): row for row in list_rows}

    hosting = []
    for row in as_completed(hosting_thread):
        item = row.result()
        hosting.append(item)
    
    for i in range(len(hosting)):
        print(hosting[i])



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
    wait.until(EC.presence_of_element_located((By.XPATH,"//input[@data-testid='structured-search-input-field-query']")))
    locationBox = driver.find_element_by_xpath("//input[@data-testid='structured-search-input-field-query']")
    locationBox.send_keys(city)

    # fecha de entrada
    wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-field-split-dates-0']")))
    checkinButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-field-split-dates-0']")
    checkinButton.click()
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[@data-testid='datepicker-day-"+ checkin +"']")))
    checkinDate = driver.find_element_by_xpath("//div[@data-testid='datepicker-day-"+ checkin +"']")
    checkinDate.click()

    # fecha de salida
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[@data-testid='datepicker-day-"+ checkout +"']")))
    checkoutDate = driver.find_element_by_xpath("//div[@data-testid='datepicker-day-"+ checkout +"']")
    checkoutDate.click()

    # huespedes
    wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-field-guests-button']")))
    guestsButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-field-guests-button']")
    guestsButton.click()

    wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-adults' and @aria-label='aumentar valor']/span")))
    addAdult = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-adults' and @aria-label='aumentar valor']/span")
    for _ in range(adults):
        addAdult.click()

    wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-children' and @aria-label='aumentar valor']/span")))
    addChild = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-children' and @aria-label='aumentar valor']/span")
    for _ in range(children):
        addChild.click()

    wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-infants' and @aria-label='aumentar valor']/span")))
    addBabie = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-infants' and @aria-label='aumentar valor']/span")
    for _ in range(babies):
        addBabie.click()

    # buscar
    wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-search-button']")))
    searchButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-search-button']")
    searchButton.click()

    # lista obtenida por la busqueda
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='_fhph4u']")))
    result = driver.find_element_by_xpath("//div[@class='_fhph4u']")

    return result

def refine(row):

    # extraer url
    print("thread creado")
    url = "https://www.airbnb.cl" + row.find_all('a', href=True)[0]['href']

    # extraer descripción y lugar (requiere entrar al alojamiento)

    single_result_chrome_options = webdriver.ChromeOptions()
    single_result_chrome_options.add_argument("--window-size=1920,1080")
    single_result_chrome_options.add_argument("--start-maximized")
    single_result_chrome_options.add_argument('--headless')
    single_result_chrome_options.add_argument('log-level=3')
    single_result_driver = webdriver.Chrome(options = single_result_chrome_options)
    wait = WebDriverWait(single_result_driver, 10)

    single_result_driver.get(url)


    wait.until(EC.presence_of_element_located((By.XPATH,"//h2[@class='_14i3z6h' and contains(text(),'noche en')]")))
    soup_location = single_result_driver.find_element_by_xpath("//h2[@class='_14i3z6h' and contains(text(),'noche en')]")

    wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='_eeq7h0']")))
    soup_description = single_result_driver.find_element_by_xpath("//div[@class='_eeq7h0']")

    description = soup_description.text

    location = soup_location.text.replace(" noches en ", '').replace(" noche en ", '').translate(str.maketrans('', '', digits))

    single_result_driver.quit()

    ## extraer el resto de las variables ##
    # nombre
    name = row.find_all('div', { 'class': '_1c2n35az' })[0].text

    # categoría
    category = row.find_all('div', { 'class': '_167qordg' })[0].text.split(' en ')[0]

    # servicios
    services = row.find_all('div', { 'class': '_kqh46o' })[1].text.split(' · ')

    # precio total
    total_price = row.find_all('button', { 'class': '_ebe4pze' })[0].text.replace("Total: $", '').replace('.', '').replace("Mostrar los detalles", '').replace("CLP", '')

    if(row.find_all('div', { 'class': '_snufp9' })):
        super_host = True
    else:
        super_host = False

    # precio por noche
    nightly_price = row.find_all('span', { 'class': '_1p7iugi' })[0].text.replace("Precio:", '').replace("  CLP por noche", '').replace('.','').replace("CLP", '')
    i = len(nightly_price)-1
    while(nightly_price[i] != '$'):
        i = i-1
    nightly_price = int(nightly_price[i:].replace("$", ''))

    if(row.find_all('span', { 'class': '_10fy1f8' })):
        rating = float(row.find_all('span', { 'class': '_10fy1f8' })[0].text.replace(",", "."))
    else:
        rating = None

    ### crear objeto Hosting ###
    new_hosting = Hosting(name, location, url, category, super_host, services, nightly_price, total_price, rating, description)

    return new_hosting