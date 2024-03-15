#################################################
## Autor:       Oscar Olivos Hidalgo.
## Descripcion: Problema3 optimizado para Tiempo
## Fecha:       14/03/2024
##
#################################################

from typing import List, Tuple
from datetime import datetime
import pandas as pd

from memory_profiler import profile
#import cProfile
#import pstats
import re

@profile
def q3_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    pd.set_option('mode.chained_assignment', None)  #evita warning
    #cargo el jsonl como dataframe pandas
    pddf=pd.read_json(file_path, lines=True)
    #trabajo solo con una columna, la que hace referencia al body del tweet
    pddf=pddf[['content']]     
    # selecciono solo las filas que tengan al menos un emoji
    pddf = pddf[pddf['content'].str.contains(r'(?:[@]([a-zA-Z0-9_]+|$))', regex=True)]
    # elimino todo contenido que no sea un emoji
    pddf['content'] = pddf['content'].apply(lambda x: ' '.join(re.findall(r'(?:[@]([a-zA-Z0-9_]+|$))', x)))
    # separo las celdas que tengan mas de un emoji en filas
    pddf = pddf.assign(content=pddf['content'].str.split(' ')).explode('content').reset_index(drop=True)
    # selecciono las filas que no sean vacias
    pddf = pddf[pddf['content'] != ' ']
    
    # count de emojis
    df_topmention = pddf.groupby('content').agg({'content': ['count']})
    df_topmention = df_topmention.reset_index()
    # rename de columnas
    df_topmention.columns = ['content','mention_count']
    # orderno desc
    df_topmention=df_topmention.sort_values(by='mention_count', ascending=False)
    # selecciono las top10
    df_topmention = df_topmention.head(10)
    # dataframe a lista de tuplas
    list_topmention = list(df_topmention.to_records(index=False))
    return list_topmention



'''
if __name__ == '__main__':
    profiler=cProfile.Profile()
    profiler.enable()
    li_q3t = q3_time('c:/Users/Usuario/Downloads/challenge_DE/src/farmers-protest-tweets-2021-2-4.json')
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumtime')
    print('----------------------------')
    stats.print_stats(0)
    print('----------------------------')

    #(t+) se aprecia que el consumo de memoria en al menos 8 instrucciones es de ~1425MiB luego bajando a ~260MiB, 
    #el tiempo es de aproximados 8.7 seconds
    #[('narendramodi', 2261),
    # ('Kisanektamorcha', 1836),
    # ('RakeshTikaitBKU', 1641),
    # ('PMOIndia', 1422),
    # ('RahulGandhi', 1125),
    # ('GretaThunberg', 1046),
    # ('RaviSinghKA', 1015), 
    # ('rihanna', 972),
    # ('UNHumanRights', 962),
    # ('meenaharris', 925)]
    print(li_q3t)
'''
