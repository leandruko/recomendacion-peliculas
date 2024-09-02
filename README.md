# Sistema de Recomendación de Películas

Este proyecto implementa un sistema de recomendación de películas utilizando técnicas de filtrado colaborativo y similitud de coseno. El sistema está optimizado para un uso eficiente de memoria y se presenta a través de una interfaz de usuario interactiva creada con Streamlit.

## Características

- Recomendación de películas basada en similitud de contenido
- Interfaz de usuario intuitiva con Streamlit
- Optimización de memoria para manejar grandes conjuntos de datos
- Carga eficiente de datos y procesamiento por lotes

## Requisitos del Sistema

- Python 3.7+
- 4GB de RAM (mínimo recomendado)
- Espacio en disco para los conjuntos de datos de películas

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/leandruko/recomendacion-peliculas.git
   cd recomendacion-peliculas
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Configuración de Datos

1. Descarga los conjuntos de datos de MovieLens (versión small o 20M) desde [aquí](https://grouplens.org/datasets/movielens/).
2. Extrae los archivos y coloca `ratings.csv` y `movies.csv` en el directorio raíz del proyecto.

## Uso

1. Ejecuta la aplicación:
   ```
   streamlit run app.py
   ```

2. Abre tu navegador y ve a `http://localhost:8501`.

3. Selecciona una película del menú desplegable y haz clic en "Obtener Recomendaciones" para ver las películas recomendadas.

## Personalización

Puedes ajustar varios parámetros en `app.py` para optimizar el rendimiento:

- `nrows` en `load_data()`: Controla cuántas filas de datos se cargan inicialmente.
- `n_movies` y `n_users` en `create_matrix()`: Ajusta el tamaño de la matriz de películas-usuarios.
- `max_mem_percent` en `limit_memory()`: Establece el límite máximo de uso de memoria.

## Solución de Problemas

- Si encuentras errores de memoria, intenta reducir `nrows`, `n_movies`, y `n_users`.
- Para conjuntos de datos muy grandes, considera implementar un sistema de carga por lotes.


## Contacto

Email - leasotompriv@gmail.com

Enlace del proyecto: [https://github.com/leandruko/recomendacion-peliculas](https://github.com/leandruko/recomendacion-peliculas)
