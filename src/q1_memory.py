#################################################
## Autor:       Oscar Olivos Hidalgo.
## Descripcion: Problema1 optimizado para Memoria
## Fecha:       14/03/2024
##
#################################################

from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json

from memory_profiler import profile
#import cProfile,pstats

@profile
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    resp = []
    pd.set_option('mode.chained_assignment', None)  # Levantar una excepción
    with open(file_path, 'r') as f:
        data = [[json.loads(line)['url'], pd.to_datetime(json.loads(line)['date']), json.loads(line)['user']['username']]  for line in f.readlines()]
    columnas = ['url', 'date', 'identificador']
    pddf = pd.DataFrame(data, columns=columnas)
    pddf['date_fecha'] = pddf['date'].dt.date

    df_topdates = pddf.groupby('date_fecha').agg({'url': ['count']})
    df_topdates.columns = ['url_count']
    df_topdates = df_topdates.reset_index()
    df_topdates=df_topdates.sort_values(by='url_count', ascending=False)
    df_topdates = df_topdates.head(10)

    for indice, fila in df_topdates.iterrows():
        df_topuser_xdate = pddf[pddf['date_fecha'] == fila['date_fecha']]
        #df_topuser_xdate['identificador'] = df_topuser_xdate['user'].apply(lambda x: x['username'])
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
    li_q1m = q1_memory('c:/Users/Usuario/Downloads/farmers-protest-tweets-2021-2-4.json')
    profiler.disable()

    stats = pstats.Stats(profiler)
    print('----------------------------')
    stats.print_stats(0)
    print('----------------------------')
    print(li_q1m)
'''
