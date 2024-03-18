#################################################
## Autor:       Oscar Olivos Hidalgo.
## Descripcion: Problema1 optimizado para Tiempo
## Fecha:       14/03/2024
##
#################################################

from typing import List, Tuple
from datetime import datetime
import pandas as pd

from memory_profiler import profile
import cProfile,pstats


@profile
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    resp = []
    # primer bloque: se obtienen las 10 fechas con mas tweets
    pd.set_option('mode.chained_assignment', None)  # Levantar una excepción
    pddf=pd.read_json(file_path, lines=True)
    pddf=pddf[['date','url','user']] 
    pddf['date_fecha'] = pddf['date'].dt.date

    df_topdates = pddf.groupby('date_fecha').agg({'url': ['count']})
    df_topdates.columns = ['url_count']
    df_topdates = df_topdates.reset_index()
    df_topdates=df_topdates.sort_values(by='url_count', ascending=False)
    df_topdates = df_topdates.head(10)

    # segundo bloque: para cada una de las fechas top, se obtienen el usuario con mas tweets
    for indice, fila in df_topdates.iterrows():
        df_topuser_xdate = pddf[pddf['date_fecha'] == fila['date_fecha']]
        df_topuser_xdate['identificador'] = df_topuser_xdate['user'].apply(lambda x: x['username'])
        df_topuser_xdate = df_topuser_xdate.groupby('identificador').agg({'url': ['count']})
        df_topuser_xdate=df_topuser_xdate.reset_index()
        df_topuser_xdate.columns = ['identificador','url_count']
        df_topuser_xdate=df_topuser_xdate.sort_values(by='url_count', ascending=False)
        df_topuser_xdate = df_topuser_xdate.head(1)
        resp.append((fila['date_fecha'],df_topuser_xdate['identificador'].values[0])) #

    return resp
    


'''
if __name__ == '__main__':
    profiler=cProfile.Profile()
    profiler.enable()
    list_q1t = q1_time('c:/Users/Usuario/Downloads/farmers-protest-tweets-2021-2-4.json')
    profiler.disable()

    stats = pstats.Stats(profiler)
    print('----------------------------')
    stats.print_stats(0)
    print('----------------------------')
    profile.print_stats()
    print('----------------------------')
    print(list_q1t)
'''