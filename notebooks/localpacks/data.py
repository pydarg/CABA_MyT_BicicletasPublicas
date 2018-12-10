import os
from urllib.request import urlretrieve
import pandas as pd

#FUENTE DE DATOS
URL = {'2010' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2010.csv/download/csv',
       '2011' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2011.csv/download/csv',
       '2012' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2012.csv/download/csv',
       '2013' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2013.csv/download/csv',
       '2014' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2014.csv/download/csv',
       '2015' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2015.csv/download/csv',
       '2016' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2016.csv/download/csv',
       '2017' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2017.csv/download/csv',
       '2018' : r'https://data.buenosaires.gob.ar/api/files/recorridos-realizados-2018.csv/download/csv'}

FILENAME = {'2010' : r'./data/recorridos-realizados-2010.csv',
            '2011' : r'./data/recorridos-realizados-2011.csv',
            '2012' : r'./data/recorridos-realizados-2012.csv',
            '2013' : r'./data/recorridos-realizados-2013.csv',
            '2014' : r'./data/recorridos-realizados-2014.csv',
            '2015' : r'./data/recorridos-realizados-2015.csv',
            '2016' : r'./data/recorridos-realizados-2016.csv',
            '2017' : r'./data/recorridos-realizados-2017.csv',
            '2018' : r'./data/recorridos-realizados-2018.csv'}

#DATOS ADICIONALES
URL_OTHERS = {'estaciones' : r'https://data.buenosaires.gob.ar/api/files/estaciones-de-bicicletas-publicas.csv/download/csv',
              'bicicleterias' : r'https://data.buenosaires.gob.ar/api/files/bicicleterias-de-la-ciudad.csv/download/csv'
             }

FILENAME_OTHER = { 'estaciones' : r'./data/estaciones-de-bicicletas-publicas.csv',
                  'bicicleterias' : r'./data/bicicleterias-de-la-ciudad.csv'
                 }

#FUNCIONES
def get_data(year = 2017, filename = FILENAME, url = URL, force_download=False):
    '''    
    PARAMETERS
    ----------
    year: integer (optional)
        periodo de recoleccion de los datos, por defecto 2017
    filename: string (optional)
        ruta donde se almacena el data set
    url: string (optional)
        direccion url donde se encuentran alojados los datos
    force_download = boolean (optional)
        si es True, forzara la descarga del data set
    RETURN
    ------
    data: pandas.DataFrame
        retorna un data frame con los datos del sistema de transporte público argentino, en el [year] escogido
    EXAMPLES
    --------
    None
    '''
    if str(year) in url.keys():#verificamos si el periodo de estudio esta disponible
        if force_download or not os.path.exists(filename[str(year)]):
            urlretrieve( url[str(year)], filename[str(year)])
        if str(year) in ['2015', '2016', '2017', '2018']:#estos periodos tienen parametros de coding particulares
            data = pd.read_csv(filename[str(year)], sep=",", thousands=".", decimal=",") #Parametros recomendados en http://datos.gob.ars
        else:
            data = pd.read_csv(filename[str(year)], sep=";", thousands=".", decimal=",") #Parametros recomendados en http://datos.gob.ars
    else:
        data = None
        print('data = NONE. Debe escoger un rango de fechas entre 2010 y 2018')
    
    print('El pandas.DataFrame se ha cargado correctamente para el periodo:', str(year),'\n',
    """
    BICICLETAS PUBLICAS -- BUENOS AIRES\n
    PERIODOS DISPONIBLES: 
    2011,2012,2013,2014,2015,2016,2017,2018
    DESCRIPCION:
    Información Información del sistema de transporte público desde sus inicios hasta la actualidad.
    CONTENIDO:
    Recorrido,horarios, detalles de origen y destino de cada uno de los viajes realizados.
    EXTRA:
    Para información sobre las estaciones de bicicletas se puede acceder al dataset Estaciones de Bicicletas Públicas.
    NOTA:
    Los recursos 2015 y 2016 contienen menos campos debido a un cambio en el sistema.
    """
    )
    return data


def get_data_others(select = 'estaciones', format_data = True, filename = FILENAME_OTHER, url = URL_OTHERS, force_download=False):
    '''    
    PARAMETERS
    ----------
    select: str (optional)
        data set adicional a escoger, entre la opciones están ['estaciones', 'bicicleterias']
    format_data: Bolean (optional)
        da formato a nuestro data frame, fechas, nombre de columnas, etc.
    filename: string (optional)
        ruta donde se almacena el data set
    url: string (optional)
        direccion url donde se encuentran alojados los datos
    force_download = boolean (optional)
        si es True, forzara la descarga del data set
    RETURN
    ------
    data: pandas.DataFrame
        retorna un data frame seleccionado
    EXAMPLES
    --------
    None
    '''
    if select in url.keys():#verificamos si el periodo de estudio esta disponible
        if force_download or not os.path.exists(filename[select]):
            urlretrieve( url[select], filename[select])
        
        data = pd.read_csv(filename[select]) 
        if select == 'estaciones' and format_data == True:
            data = format_estaciones(data)
        elif select == 'bicicleterias' and format_data == True:
            data = format_bicicleterias(data)
    else:
        data = None
        print('data = NONE. El data set que intenta seleccionar no existe en URL_OTHER.keys()')
    return data

def format_estaciones(df):
    '''
    PARAMETERS
    ----------
    df: pandas Data Frame (obligatorio)
        data frame que contiene las estaciones de las bicicletas con las coordenadas gps y datos adicionales.
    RETURN
    ------
    df: pandas Data Frame
        unicamente con los atributos esenciales para georeferenciar las estaciones de las biclicetas
    '''
    df.drop(['domicilio','automat','imagen','observ','horario','dire_norm'], axis = 1, inplace = True) #eliminamos las columnas que no usaremos
    df = df[['nro_est', 'nombre', 'lat', 'long']] #reordenamos el orden de las columnas
    return df

def format_bicicleterias(df):
    '''
    PARAMETERS
    ----------
    df: pandas Data Frame (obligatorio)
        data frame que contiene las bicicleterias con las coordenadas gps y datos adicionales.
    RETURN
    ------
    df: pandas Data Frame
        unicamente con los atributos esenciales para georeferenciar las bicicleterias
    '''
    df.drop(['calle','altura','calle2','telefono','email','web','mecanica_s','horario_de','barrio','comuna','codigo_postal','codigo_postal_argentino'],
                 axis = 1, inplace = True) #eliminamos las columnas que no usaremos
    df = df[['nombre', 'lat', 'long']] #reordenamos el orden de las columnas
    return df




def format_data(df):
    """
    PARAMETERS
    ----------
    df: pandas DataFrame (obligatorio)
        toma un pandas DataFrame con datos crudos
    RETURN
    ------
    df: pandas.DataFrame
        retorna pandas DataFrame con datos en formato pandas
    """
    #1.Damos formato e indexamos
    df.index = pd.to_datetime(df['fecha_hora_retiro'], format='%d/%m/%Y %H:%M:%S')#
    
    #2.Eliminamos 'periodo' dado que se trata de un valor trivial y la 'fecha_horaretiro' que fue pasada como indice
    del df['periodo']
    del df['fecha_hora_retiro']
    
    #3.Convertimos 'tiempo_uso' en un timedelta
    extrae_horas = df['tiempo_uso'].str.extract('(?P<h>[0-99]*)h (?P<m>[0-99]*)min (?P<s>[0-99]*)seg', expand=False)#extramos el valos numerico de las horas, minutos y segundos
    extrae_horas['tiempo_uso'] = extrae_horas.h +':'+ extrae_horas.m +':'+ extrae_horas.s#creamos una nueva columna juntando los valores numericos
    df['tiempo_uso'] = pd.to_datetime(extrae_horas['tiempo_uso'], format='%H:%M:%S') #sobreescribimos la original con un formato tiempo #NOTA: no se como eliminarle el dia y trabajar unicamente con la hora.
    
    print("""
    TAREAS REALIZADAS:\n 
          1.Dimos formato a 'fecha hora retiro' y la pasamos como indice.\n
          2.Eliminamos la columna 'periodo'.\n
          3.Convertimos 'tiempo_uso' en un timedelta.
    """)
    
    return df

def clean_garbage(df):
    '''
    PARAMETERS
    ----------
    df: pandas DataFrame (obligatorio)
        toma un pandas DataFrame con datos crudos
    RETURN
    ------
    clean: pandas.DataFrame
       pandas DataFrame con datos limpios
    null: pandas.DataFrame
       pandas DataFrame con datos nulos
    duplicates: pandas.DataFrame
       pandas DataFrame con datos duplicados
    '''
    #1.Contamos valores nulos
    count_nulls = df.isnull().any().count()
    
    #2.Verificamos columnas con categorias
    df['genero'].unique() == ['M','F']
    
    #3.Verificamos columnas con categorias
    
    #4.Aplicamos correcciones
    nulls = df[df['tiempo_uso'].isnull() == True]
    duplicates = ['null']
    outliers = ['null']
    df.dropna(inplace=True)
    clean = df
    
    print('TAREAS REALIZADAS:','\n',
          '1.Valores nulos eliminados:', count_nulls, '\n',
          '2.Verificamos categorias:', df['genero'].unique(), '\n',
         )
    return clean, nulls, duplicates, outliers

def panel_visualization():
    pass