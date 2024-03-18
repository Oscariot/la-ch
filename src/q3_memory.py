#################################################
## Autor:       Oscar Olivos Hidalgo.
## Descripcion: Problema3 optimizado para Memoria
## Fecha:       14/03/2024
##
#################################################

from typing import List, Tuple
from datetime import datetime
import pandas as pd

from memory_profiler import profile
import cProfile,pstats
from re import findall
from json import loads

@profile
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    with open(file_path, 'r') as f:
        data = [[loads(line)['content']]  for line in f.readlines()]
    columnas = ['content']
    pddf = pd.DataFrame(data, columns=columnas)
    # trabajo solo con una columna, la que hace referencia al body del tweet
    pddf=pddf[['content']]     
    # elimino todo contenido que no sea una mension
    pddf['content'] = pddf['content'].apply(lambda x: ' '.join(findall(r'(?:[@]([a-zA-Z0-9_]+|$))', x)))
    # separo las celdas que tengan mas de una mension en filas
    pddf = pddf.assign(content=pddf['content'].str.split(' ')).explode('content').reset_index(drop=True)
    # selecciono las filas que no sean vacias
    pddf = pddf[~pddf['content'].isin([' ',''])]
    
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
    list_q3m = q3_memory('c:/Users/Usuario/Downloads/farmers-protest-tweets-2021-2-4.json')
    profiler.disable()

    stats = pstats.Stats(profiler)
    print('----------------------------')
    stats.print_stats(0)
    print('----------------------------')
    print(list_q3m)
'''
