from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from selenium.webdriver.support.select import Select
from math import floor, ceil
from .classes import ExpediaHosting

def _config():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    option.add_argument("--start-maximized")
    option.add_argument('--headless')
    browser = webdriver.Chrome(options = option)
    browser.get('https://www.expedia.es')
    return browser

def _convert_month(date):
    year = date[0:4]
    monthdict = {
        "enero" : '01',
        "febrero" : '02',
        "marzo" : '03',
        "abril" : '04',
        "mayo" : '05',
        "junio" : '06',
        "julio" : '07',
        "agosto" : '08',
        "septiembre" : '09',
        "octubre" : '10',
        "noviembre" : '11',
        "diciembre" : '12'
    }
    month = list(monthdict.keys())[list(monthdict.values()).index(date[5:7])] + " de " + year
    return month

def _calculate_people(adults,rooms,children,babies):
    from math import floor, ceil
    #dividir adultos en rooms
    divide_adults = adults/rooms
    adults_list = []

    for habitacion in range(int(rooms)):
        if habitacion % 2 == 0:
            adults_in_room = ceil(divide_adults)
            adults_list.append(adults_in_room)
        else:
            adults_in_room = floor(divide_adults)
            adults_list.append(adults_in_room)

    #dividir kids en rooms
    kids = children+babies
    divide_kids = kids/rooms
    kids_list = []

    kids_ages = []
    for children in range(children):
        kids_ages.append("17")
    for baby in range(babies):
        kids_ages.append("1")
    
    for habitacion in range(int(rooms)):
        if habitacion % 2 == 0:
            kids_in_room = ceil(divide_kids)
            kids_list.append(kids_in_room)
        else:
            kids_in_room = floor(divide_kids)
            kids_list.append(kids_in_room)
    
    return adults_list, kids_list, kids_ages
    
#METODO QUE REALIZA LA BÚSQUEDA
def _expedia(city, checkin, checkout, rooms, adults, children, babies):
    browser = _config()
    wait = WebDriverWait(browser, 5)

    # SELECCIONAR DESTINO
    destination_button = browser.find_element_by_class_name('uitk-faux-input')
    destination_button.send_keys(city + Keys.ENTER)
    sleep(0.5)

    # PRESIONAR BOTON PARA ABRIR CALENDARIO
    checkin_button = browser.find_element_by_id('d1-btn')
    browser.execute_script('arguments[0].click();',checkin_button)

    # CONVERTIR MESES AL FORMATO QUE ESTA ESCRITO EN EL SITIO WEB
    checkin_month = _convert_month(checkin)
    checkout_month = _convert_month(checkout)
    
    #CALCULO DE NOCHES EN EL HOTEL
    from datetime import datetime as date
    delta = date.strptime(checkout, '%Y-%m-%d') - date.strptime(checkin, '%Y-%m-%d')
    nights = delta.days

    # SE ESPERA A QUE ESTE DISPONIBLE EL CALENDARIO
    calendar = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME,'uitk-new-date-picker-desktop-months-container')
        )
    )

    ## MOVER CALENDARIO SI EL MES NO CORRESPONDE 
    months_list = []
    actual_month = calendar.find_elements_by_class_name('uitk-new-date-picker-month-name')
    for month in actual_month:
        months_list.append(month.text)
    while(months_list[0] != checkin_month):
        months_list.clear()
        months = calendar.find_elements_by_class_name('uitk-new-date-picker-month-name')
        for month in months:
            months_list.append(month.text)
        if (months_list[0] != checkin_month):
            browser.find_element_by_css_selector('.uitk-flex > .uitk-button:nth-child(2)').click()
        sleep(0.5)

    if checkin_month == checkout_month:
        first_calendar = browser.find_element_by_css_selector('.uitk-new-date-picker-month:nth-child(1)')
        first_days = first_calendar.find_elements_by_class_name('uitk-new-date-picker-day')
        for day in first_days:
            if int(day.get_attribute('data-day')) == int(checkin[8:]):
                day.click()
            if int(day.get_attribute('data-day')) == int(checkout[8:]):
                day.click()
        sleep(4)
    elif checkin_month != checkout_month:
        first_calendar = browser.find_element_by_css_selector('.uitk-new-date-picker-month:nth-child(1)')
        first_days = first_calendar.find_elements_by_class_name('uitk-new-date-picker-day')
        for day in first_days:
            if int(day.get_attribute('data-day')) == int(checkin[8:]):
                day.click()
        second_calendar = browser.find_element_by_css_selector('.uitk-new-date-picker-month:nth-child(2)')
        second_days = second_calendar.find_elements_by_class_name('uitk-new-date-picker-day')
        for day in second_days:
            if int(day.get_attribute('data-day')) == int(checkout[8:]):
                day.click()
        sleep(4)

    # SELECCIONAR VIAJEROS 
    browser.find_element_by_css_selector('.uitk-flex-shrink-0').click()

    travelers_button = browser.find_element_by_xpath('//button[@data-testid="travelers-field-trigger"]')
    browser.execute_script('arguments[0].click();',travelers_button)

    travelers = wait.until(
    EC.presence_of_element_located(
        (By.CLASS_NAME,'uitk-menu-container')
        )
    )
    
    #lo primero es agregar la cantidad de habitaciones que pide
    for contador in range(int(rooms)-1):
        add_room_button = travelers.find_element_by_xpath('//button[text()="Añadir otra habitación"]')
        browser.execute_script('arguments[0].click();',add_room_button)

    #funcion que calcula cantidad de personas por habitacion
    adults_list, kids_list, kids_ages = _calculate_people(adults,rooms,children,babies)

    #ir poniendo la cantidad de adultos y niños correspondiente en cada habitacion
    for contador in range(int(rooms)):
        adult_room = browser.find_element_by_css_selector('.roomPickerRoom:nth-child({}) > .adultStepInput > .uitk-flex'.format(contador + 1))
        adult_input = adult_room.find_element_by_id('adult-input-{}'.format(contador))
        kids_room = browser.find_element_by_css_selector('.roomPickerRoom:nth-child({}) > .childStepInput > .uitk-flex'.format(contador + 1))
        kids_input = kids_room.find_element_by_id('child-input-{}'.format(contador))
        
        while(int(adult_input.get_attribute('value'))!=int(adults_list[contador])):
            #apretar botón de "+" 
            plus_button_ad = browser.find_element_by_css_selector('.roomPickerRoom:nth-child({}) > .uitk-flex:nth-child(2) .uitk-button:nth-child(3)'.format(contador +1))
            browser.execute_script('arguments[0].click();',plus_button_ad)
        sleep(1)
        
        while(int(kids_input.get_attribute('value'))!=int(kids_list[contador])):
            #apretar botón de "+" 
            plus_button_ki = browser.find_element_by_css_selector('.roomPickerRoom:nth-child({}) > .uitk-flex:nth-child(3) .uitk-button:nth-child(3)'.format(contador + 1))
            browser.execute_script('arguments[0].click();',plus_button_ki)
        sleep(1)
        
        #agregar edades de niños
        for kid_index in range(int(kids_list[contador])):            
            dropdown = Select(browser.find_element_by_id('child-age-input-{}-{}'.format(contador, kid_index)))
            dropdown.select_by_value(kids_ages[kid_index])
        
        contador += 1

    accept_travelers = browser.find_element_by_css_selector('.uitk-button-floating')
    browser.execute_script('arguments[0].click();',accept_travelers)
    sleep(2)
    search_button = browser.find_element_by_xpath("//button[@data-testid='submit-button']")
    browser.execute_script('arguments[0].click();',search_button)
    
    #-------------------------------------------FIN PROGRAMA----------------------
    wait.until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, 'results')
        )
    )

    resultados=browser.find_elements_by_css_selector("li[class*='listing']")
    #resultados=browser.find_elements_by_class_name('listing')
    precios = []
    links = []
    offers = []
    for resultado in resultados:
        if resultado.get_attribute("data-stid")=="":
            link = resultado.find_element_by_css_selector("a[class*='listing__link']")
            link = link.get_attribute("href")
            links.append(link)

            precio = resultado.find_element_by_css_selector("span[data-stid='content-hotel-lead-price']")
            precios.append(precio.text)

    contador=0
    for link in links:
        body = browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
        browser.get(link)

        pagina = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'app-layer-base--active')
            )
        )

        nombre = pagina.find_element_by_xpath("//h1[@data-stid='content-hotel-title']")
        descripcion = pagina.find_element_by_css_selector("p[class*='uitk-type-paragraph-300']")

        tipo = pagina.find_element_by_css_selector("div[data-stid='content-markup']").text

        try:
            calificacion = pagina.find_element_by_xpath("//meta[@itemprop='ratingValue']")
            calificacion = calificacion.get_attribute("content")
        except:
            calificacion=0

        ammenities=[]
        ammenities_list = []
        servicios = pagina.find_element_by_xpath("//div[@data-stid='hotel-amenities-list']")
        #servicios = servicios.find_element_by_css_selector("ul[data-stid*='amenities-grid']")
        ammenities = servicios.find_elements_by_css_selector("li[class*='uitk-cell']")
        for servicio in ammenities:
            servicio_p = servicio.find_element_by_css_selector("span[class*='uitk-cell']")
            ammenities_list.append(servicio_p.text)

        offer = ExpediaHosting(name = nombre, location = city, category = tipo, rooms = rooms, services = ammenities_list, nightly_price = '', total_price = precios[contador], rating = calificacion, description = descripcion, url = links[contador])
        offers.append(offer)

        contador+=1
        body = browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
    browser.close()
    return offers

def get_offers(city, checkin, checkout, rooms, adults, children, babies):
    return _expedia(city, checkin, checkout,rooms, adults, children, babies)