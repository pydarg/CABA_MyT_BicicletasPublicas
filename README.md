# Bicicletas Públicas -- Argentina, Capital Federal.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pydarg/CABA_MyT_BicicletasPublicas.git/master)

**Descripcion:** El presente repositorio se desarrolla contexto del conjunto de DATASETS referentes al uso de las biclicletas públicas argentinas en CABA, en el cual se buscar describir el comportamiento de entradas y salidas de la estacion de los usuario.

**Objetivo:**

- Evaluar el comportamiento del uso de las ciclovías, tomando como referencia:
    - Factores climáticos.
        - Lluvia.
        - Temperatura.
    - Dias no laborales en el calendario.
    
 ## Fuente de datos:
 
 <a href="https://data.buenosaires.gob.ar/"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHdG_Yw1E_0GI1_EZry16Zo-60hYAxlgzovIh4Fy_mN3Y7Yn3T" alt="Buenos Aires Data" width="150px"></a>
 
- [Buenos Aires Data](https://data.buenosaires.gob.ar/), repositorio general de datos - Capital Federal
- [Movilidad y Trasporte - Bicicletas Públicas](https://data.buenosaires.gob.ar/dataset/bicicletas-publicas), repositorio de caso de estudio.

## DESCRIPCION - DATASETS

Se trabaja sobre un conjunto de data sets:

```python
- #df_2010.csv
    - columns=['PERIODO', 'ORIGENFECHA', 'ORIGENESTACIONID', 'ORIGENNOMBRE', 'DESTINOFECHA',
               'DESTINOESTACIONID', 'DESTINONOMBRE', 'TIEMPOUSO']
    - sep=';'
- #df_2011.csv
    - columns=['PERIODO', 'ORIGENFECHA', 'ORIGENESTACIONID', 'NOMBREORIGEN', 'DESTINOFECHA',
               'DESTINOESTACIONID', 'NOMBREDESTINO', 'TIEMPOUSO']
    - sep=';'
- #df_2012.csv
    - columns=['PERIODO', 'ORIGENFECHA', 'ORIGENESTACIONID', 'ORIGENNOMBRE', 'DESTINOFECHA',
               'DESTINOESTACIONID', 'DESTINONOMBRE', 'TIEMPOUSO']
    - sep=';'
- #df_2013.csv
    - columns=['ID', 'NOMBRE_ORIGEN', 'ORIGEN_FECHA', 'DESTINO_ESTACION', 'DESTINO_FECHA']
    - sep=';'
- #df_2014.csv
    - columns=['ID', 'NOMBRE_ORIGEN', 'ORIGEN_FECHA', 'DESTINO_ESTACION', 'DESTINO_FECHA']
    - sep=';'
- #df_2015.csv
    - columns=['periodo', 'genero', 'fecha_hora_retiro', 'origen_estacion', 'nombre_origen', 
               'destino_estacion', 'nombre_destino, tiempo_uso']
    - sep=','
- #df_2016.csv
    - columns=['periodo', 'genero', 'fecha_hora_retiro', 'origen_estacion', 'nombre_origen', 
               'destino_estacion', 'nombre_destino', 'tiempo_uso']
    - sep=','
- #df_2017.csv
    - columns=['periodo', 'genero', 'fecha_hora_retiro', 'origen_estacion', 'nombre_origen', 
               'destino_estacion', 'nombre_destino', 'tiempo_uso']
    - sep=','
- #df_2018.csv
     - columns=['id_usuario', 'bici_fecha_hora_retiro', 'bici_tiempo_uso', 'bici_nombre_estacion_origen',
                'bici_estacion_origen', 'bici_nombre_estacion_destino', 'bici_estacion_destino', 'bici_sexo', 'bici_edad']
     - sep=','

```

Podemos observar que para cada período, los datos presentan diferentes  número de atributos, y que las columnas que contienen el mismo atributo diferen en el nombre, por lo tanto, en principio no resulta posible plantear un estudio geneneral para todos los años.

## MAIN WORKFLOW

- `CasoInicio.ipynb:` Se trabaja sobre todos los datos, dejando defindas todas las funciones, para trabajar con data frames limpios con formato y lo más homogeneos posible. **[Sin Iniciar]**

- `CasoGPS.ipynb:` como tarea de exploración, visualizamos la posición de las estaciones en un mapa. **[Iniciado]**

- `Caso2010..2018.ipynp:` Un notebook para estudiar individualmente cada dataframe.
  - df_2010: **[Sin Iniciar]**
  - df_2011: **[Sin Iniciar]**
  - df_2012: **[Sin Iniciar]**
  - df_2013: **[Sin Iniciar]**
  - df_2014: **[Sin Iniciar]**
  - df_2015: **[Sin Iniciar]**
  - df_2016: **[Sin Iniciar]**
  - df_2017: **[Sin Iniciar]**
  - df_2018: **[Iniciado]**
  
- `CasoGeneral.ipynb:` Se hace un estudio tomando en cuenta todos los periodos.
  - Estado: **[Sin Iniciar]**


## Software

Este código ha sido probado con Python 3.5, es posible que funcione correctamente con Python 2.7 y otras versionnes anteriores.

Los paquetes necesarios para trabajar con este repositario están listados en [requirements.txt](requirements.txt) (Nota: Es posible que puedas utilizar versiones más nuevas y siga funcionando adecuadamente).
Para instalar los requerimientos en [conda](http://conda.pydata.org), ejecuta la siguiente línea de comandos en la terminal:

```
$ conda install --file requirements.txt
```

Si quieres crear un entorno aislado ``BICIS`` con Python 3.5 y todos los paquetes requeridos, ejecuta el siguiente código:

```
$ conda create -n BICIS python=3.5 --file requirements.txt
```

Puedes leer más acerca de entornos virtuales en [Managing Environments](http://conda.pydata.org/docs/using/envs.html) en la documentación de conda.

**IMPORTANTE:** El fichero `localpacks`es un paquete creado lcoalmente, por lo que se recomienda clonar este repositorio o copiar manualmente el fichero `localpacks` en el directorio de trabajo.

## Uso

```python
from localpacks.maps import draw_map, draw_mult_map
from localpacks.data import get_data,format_data, clean_garbage

#generamos nuestros data sets
df_geo = get_data()
df_tienda = get_data()


#llamamos la función que dibuja nuestro mapa
draw_mult_map(df_geo, df_tienda)

```
![Mapa de Estaciones y Tiendas](images/map.png))


## Acerca de localpacks

Se trata de un concepto genérico que promueve como flujo de trabajo ir compilando el código generado inicialmente en las notebooks en paquetes python, en otras palabras, vamos tomando el código que utilizamos para generar **una determinada acción** y lo hacemos una función o clase en localpacks. Por ejemplo:

- Si nuestra acción consiste en georeferenciar las coordenadas de las estaciones en un mapa:

    - **Primero:** generamos las lineas de código necesarias para verlas en nuestro notebook.
    - **Segundo:** creamos una función `draw_mult_map` basada en el código previamente generado.
    - **Tercero:** ahora podremos hacer el llamado de nuestra función.
    
**Nota:** `get_pack`es una función de localpacks que nos carga nuestros data sets desde la fuente y con los parámetros correctos.


## License


This project is released under an `MIT`.
