from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

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
print("lugar listo")

# fecha de entrada
wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-field-split-dates-0']")))
checkinButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-field-split-dates-0']")
checkinButton.click()
print("botón fecha de entrada listo")
wait.until(EC.presence_of_element_located((By.XPATH,"//div[@data-testid='datepicker-day-"+ checkin +"']")))
checkinDate = driver.find_element_by_xpath("//div[@data-testid='datepicker-day-"+ checkin +"']")
checkinDate.click()
print("fecha de entrada seleccionada")


# fecha de salida
print("botón fecha de salida listo")
wait.until(EC.presence_of_element_located((By.XPATH,"//div[@data-testid='datepicker-day-"+ checkout +"']")))
checkoutDate = driver.find_element_by_xpath("//div[@data-testid='datepicker-day-"+ checkout +"']")
checkoutDate.click()
print("fecha de salida seleccionada")

# huespedes
wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-field-guests-button']")))
guestsButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-field-guests-button']")
guestsButton.click()
print("botón huespedes listo")

wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-adults' and @aria-label='aumentar valor']/span")))
addAdult = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-adults' and @aria-label='aumentar valor']/span")
for i in range(adults):
    addAdult.click()
    print("adulto añadido")

wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-children' and @aria-label='aumentar valor']/span")))
addChild = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-children' and @aria-label='aumentar valor']/span")
for i in range(children):
    addChild.click()
    print("niño añadido")

wait.until(EC.presence_of_element_located((By.XPATH,"//button[@aria-describedby='searchFlow-title-label-stepper-infants' and @aria-label='aumentar valor']/span")))
addBabie = driver.find_element_by_xpath("//button[@aria-describedby='searchFlow-title-label-stepper-infants' and @aria-label='aumentar valor']/span")
for i in range(babies):
    addBabie.click()
    print("bebe añadido")

# buscar
wait.until(EC.presence_of_element_located((By.XPATH,"//button[@data-testid='structured-search-input-search-button']")))
searchButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-search-button']")
searchButton.click()