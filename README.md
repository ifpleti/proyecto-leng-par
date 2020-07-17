## Cómo hacerlo funcionar:
1. Instalar [Python 3.8](https://www.python.org/downloads/)
2. Instalar el [driver de Google Chrome para Selenium](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver#quick-installation)
3. Crear entorno virtual de python 3.8 (opcional)
4. En el directorio, ejecutar: ```pip install -r requirements.txt``` o ```pip3 install -r requirements.txt```
5. Ejecutar: ```python main.py``` o ```python3 main.py```


## Breve descripción de lo que hace el programa:
```
proyecto-leng-par
        ├── runtime
        │      ├── modules
        │      │      ├── __init__.py
        │      │      ├── airbnb_scraping.py
        │      │      ├── classes.py
        │      │      ├── expedia_scraping.py
        │      │      ├── filter_sorting.py
        │      │      └── utils.py
        │      ├── __init__.py
        │      ├── manage.py
        │      ├── post_search_interface.py
        │      └── search_interface.py
        ├── .gitignore
        ├── README.md
        ├── main.py
        └── requirements.txt
```

El main llama a la interfáz de busqueda que se encuentra en search_interface.py, que usa a manage.py para acceder al resto de los modulos, ejecutar el scraping y por último, se llama a la ventana de post_search_interface.py para filtrar y ordenar, que a su vez también se comunica con manage.py para la ejecución de las funciones necesarias para las operaciones de filtro y ordenamiento sobre los datos.
