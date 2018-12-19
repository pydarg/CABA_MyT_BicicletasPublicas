import os
from urllib.request import urlretrieve
import pandas as pd

#DATOS PRINCIPALES
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
              'bicicleterias' : r'https://data.buenosaires.gob.ar/api/files/bicicleterias-de-la-ciudad.csv/download/csv'}

FILENAME_OTHER = {'estaciones' : r'./data/estaciones-de-bicicletas-publicas.csv',
                  'bicicleterias' : r'./data/bicicleterias-de-la-ciudad.csv'}

#FUNCIONES
def get_data(year = 2018, apply_format = False, filename = FILENAME, url = URL, force_download=False):
    '''    
    PARAMETERS
    ----------
    year: integer (optional)
        periodo de recoleccion de los datos, por defecto 2017
    apply_format: boolean(optional)
        si es True, devuelve un data set con formato de atributos y columnas
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
    df = get_data( year=2017, pply_format = True)
    '''
    if str(year) in url.keys():#verificamos que el periodo de estudio este disponible
        if force_download or not os.path.exists(filename[str(year)]):
            urlretrieve( url[str(year)], filename[str(year)])
        if str(year) in ['2015', '2016', '2017', '2018']:#estos periodos tienen parametros de coding particulares
            data = pd.read_csv(filename[str(year)], sep=",", thousands=".", decimal=",") #Parametros recomendados en http://datos.gob.ars
        else:
            data = pd.read_csv(filename[str(year)], sep=";", thousands=".", decimal=",") #Parametros recomendados en http://datos.gob.ars
            if apply_format == True:
                data = format_data(data, str(year))
    else:
        data = None
        print('data = NONE. Debe escoger un rango de fechas entre 2010 y 2018')
    
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

def format_data(df, year):
    
    if year in ['2010','2011','2012']:
        #FORMATOS
        if year == '2012':
            #una minoria de instancias tienen un formato extraño, por lo que las descartamos aplicando el siguiente filtro
            df['ORIGENFECHA_len'] = df['ORIGENFECHA'].apply(lambda x: len(str(x)))
            len_origenfecha_mean = int(df['ORIGENFECHA_len'].mean()) #longitud media de caracteres
            df = df[df['ORIGENFECHA_len'] >= len_origenfecha_mean] #las menores son fechas con formato distinto
                      
            #ELIMINAMOS
            del df['ORIGENFECHA_len']
                    
            df.index = pd.to_datetime(df['ORIGENFECHA'], format='%Y-%m-%d %H:%M:%S.%f') #damos formato de fecha e indexamos
        else:
            df.index = pd.to_datetime(df['ORIGENFECHA'], format='%d/%m/%Y %H:%M') #damos formato de fecha e indexamos
        df['TIEMPOUSO'] = df['TIEMPOUSO'].astype('int64', errors='ignore') * 60 #convertimos minutos(m) a segundos(s)
        
        #ELIMINAMOS
        del df['PERIODO'] #pasa a ser metadato
        del df['ORIGENFECHA'] 
        del df['DESTINOFECHA']
        
        #RENOMBRES
        columns = ['origen_id', 'origen_nombre', 'destino_id', 'destino_nombre', 'tiempo_uso(s)']
        df.columns = columns
        
    elif year in ['2013','2014']:
        #FORMATOS
        df.index = pd.to_datetime(df['ORIGEN_FECHA'], format='%Y-%m-%d %H:%M:%S.%f')
        #calculamos el tiempo_uso
        df['ORIGEN_FECHA'] = pd.to_datetime(df['ORIGEN_FECHA'], format='%Y-%m-%d %H:%M:%S.%f') 
        df['DESTINO_FECHA'] = pd.to_datetime(df['DESTINO_FECHA'], format='%Y-%m-%d %H:%M:%S.%f')
        df['tiempo_uso'] = df['DESTINO_FECHA'] - df['ORIGEN_FECHA']
        df['tiempo_uso']=pd.to_timedelta(df['tiempo_uso']).dt.seconds
        #ELIMINAMOS
        del df['ORIGEN_FECHA'] 
        del df['DESTINO_FECHA']
        #RENOMBRES
        columns = ['usuario_id', 'origen_nombre', 'destino_nombre', 'tiempo_uso(s)']
        df.columns = columns
    
    return df



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