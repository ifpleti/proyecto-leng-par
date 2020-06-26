from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://www.airbnb.cl/')

city = "Viña del Mar"
# checkin = "2020-06-27"
# checkout = "2020-06-30"
# adults = 2
# children = 2
# babies = 1

time.sleep(1)

# lugar
locationBox = driver.find_element_by_xpath("//input[@data-testid='structured-search-input-field-query']")
locationBox.send_keys(city)

time.sleep(1)

# fecha de entrada
checkinButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-field-split-dates-0']")
checkinButton.click()
checkinDate = driver.find_element_by_xpath("//div[@data-testid='datepicker-day-2020-06-25']")
checkinDate.click()

time.sleep(1)

# fecha de salida
checkoutButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-field-split-dates-1']")
checkoutButton.click()
checkoutDate = driver.find_element_by_xpath("//div[@data-testid='datepicker-day-2020-06-25']")
checkoutDate.click()

time.sleep(1)

# huespedes
guestsButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-field-guests-button']")
guestsButton.click()

time.sleep(1)

# buscar
searchButton = driver.find_element_by_xpath("//button[@data-testid='structured-search-input-search-button']")
searchButton.click()

