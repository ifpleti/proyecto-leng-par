Se cambió la estructura de las carpetas:

Antes:
```
proyecto-leng-par
        ├── modules
        │      ├── __init__.py
        │      ├── airbnb_scraping.py
        │      ├── classes.py
        │      ├── expedia_scraping.py
        │      ├── filter_sorting.py
        │      └── utils.py
        ├── .gitignore
        ├── main.py
        └── requirements.txt
```

Después:
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
        ├── main.py
        └── requirements.txt
```

Ahora el archivo manage.py hace lo que antes hacía el main, y el main llama a la interfaz de busqueda que se encuentra en search_interface.py, que usa a manage.py para usar el resto de los modulos, ejecutar el scraping y por último, se llama a la ventana de post_search_interface.py para filtrar y ordenar, que a su vez también se comunica con manage.py para la ejecución de las funciones necesarias para la obtención de datos
