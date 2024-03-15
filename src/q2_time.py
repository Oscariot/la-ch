#################################################
## Autor:       Oscar Olivos Hidalgo.
## Descripcion: Problema2 optimizado para Tiempo
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
def q2_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    pd.set_option('mode.chained_assignment', None)  #evita warning
    #cargo el jsonl como dataframe pandas
    pddf=pd.read_json(file_path, lines=True)
    #trabajo solo con una columna, la que hace referencia al body del tweet
    pddf=pddf[['content']]     
    # selecciono solo las filas que tengan al menos un emoji
    pddf = pddf[pddf['content'].str.contains(r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F004\U0001F0CF\U0001F170-\U0001F251\U0001F1E6-\U0001F1FF]', regex=True)]
    # elimino todo contenido que no sea un emoji
    pddf['content'] = pddf['content'].apply(lambda x: ' '.join(re.findall(r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F004\U0001F0CF\U0001F170-\U0001F251\U0001F1E6-\U0001F1FF]', x)))
    # separo las celdas que tengan mas de un emoji en filas
    pddf = pddf.assign(content=pddf['content'].str.split(' ')).explode('content').reset_index(drop=True)
    # selecciono las filas que no sean vacias
    pddf = pddf[pddf['content'] != ' ']
    
    # count de emojis
    df_topemoji = pddf.groupby('content').agg({'content': ['count']})
    df_topemoji = df_topemoji.reset_index()
    # rename de columnas
    df_topemoji.columns = ['content','emoji_count']
    # orderno desc
    df_topemoji=df_topemoji.sort_values(by='emoji_count', ascending=False)
    # selecciono las top10
    df_topemoji = df_topemoji.head(10)
    # dataframe a lista de tuplas
    list_topemoji = list(df_topemoji.to_records(index=False))
    return list_topemoji



'''
if __name__ == '__main__':
    profiler=cProfile.Profile()
    profiler.enable()
    li_q2t = q2_time('c:/Users/Usuario/Downloads/challenge_DE/src/farmers-protest-tweets-2021-2-4.json')
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumtime')
    print('----------------------------')
    stats.print_stats(0)
    print('----------------------------')

    #(t+) se aprecia que el consumo de memoria en al menos 4 instrucciones es de ~1425MiB luego bajando a ~190MiB, 
    #el tiempo es de aproximados 8.7 seconds
    #[('🙏', 7286), 
    # ('😂', 3072),
    # ('️', 3061),
    # ('🚜', 2972),
    # ('✊', 2411),
    # ('🌾', 2363),
    # ('🇮', 2096),
    # ('� '', 2094),
    # ('🏻', 2080), 
    # ('❤', 1779)]
    print(li_q2t)
'''
