from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import requests

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)
driver.get('https://www.airbnb.cl/')

city = "Viña del Mar"
checkin = "2020-06-29"
checkout = "2020-06-30"
adults = 2
children = 2
babies = 1

sleep(2)

# lugar
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
for i in range(adults):
    addAdult.click()

wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-children' and @aria-label='aumentar valor']/span")))
addChild = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-children' and @aria-label='aumentar valor']/span")
for i in range(children):
    addChild.click()

wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-infants' and @aria-label='aumentar valor']/span")))
addBabie = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-infants' and @aria-label='aumentar valor']/span")
for i in range(babies):
    addBabie.click()

# buscar
wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-search-button']")))
searchButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-search-button']")
searchButton.click()

##########################################
## Ya estamos en la lista de resultados ##
##########################################

wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='_fhph4u']")))
result = driver.find_element_by_xpath("//div[@class='_fhph4u']")

soup_all_results = BeautifulSoup(result.get_attribute("innerHTML"), "html.parser")


data = []

for row in soup_all_results.find_all('div', { 'class': '_8ssblpx' }):

    url = "https://www.airbnb.cl" + row.find_all('a', href=True)[0]['href']
    name = row.find_all('div', { 'class': '_1c2n35az' })[0].text
    category = row.find_all('div', { 'class': '_167qordg' })[0].text.split(' en ')[0]
    services = row.find_all('div', { 'class': '_kqh46o' })[1].text.split(' · ')
    total_price = row.find_all('button', { 'class': '_ebe4pze' })[0].text.replace("Total: $", '').replace('.', '').replace("Mostrar los detalles", '').replace("CLP", '')

    if(row.find_all('div', { 'class': '_snufp9' })):
        super_host = True
    else:
        super_host = False

    nightly_price = row.find_all('span', { 'class': '_1p7iugi' })[0].text.replace("Precio:", '').replace("  CLP por noche", '').replace('.','').replace("CLP", '')
    i = len(nightly_price)-1
    while(nightly_price[i] != '$'):
        i = i-1
    nightly_price = int(nightly_price[i:].replace("$", ''))

    if(row.find_all('span', { 'class': '_10fy1f8' })):
        rating = float(row.find_all('span', { 'class': '_10fy1f8' })[0].text.replace(",", "."))
    else:
        rating = -1
        
    print("nombre de la oferta: " + name)
    print("url: " + url)
    print("categoría: " + category)
    print("es superanfitrión: " + str(super_host))
    print("servicios: " + str(services))
    print("precio por noche: " + str(nightly_price))
    print("precio total: " + str(total_price))
    print("calificación: " + str(rating))
    print("")