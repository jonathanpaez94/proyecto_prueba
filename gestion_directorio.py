import os
from datetime import datetime, timedelta
import shutil


def eliminar_directorio():
    lista_directorios = os.listdir('video')
    fecha_actual = datetime.now()
    dias_max_guaradar_video = fecha_actual - timedelta(days=1) 

    for i in lista_directorios:
        directorio_actual = datetime.strptime(i, '%d_%b_%Y')
        if  dias_max_guaradar_video > directorio_actual:
            try:
                shutil.rmtree(f'video/{i}')
            except ValueError:
                os.rmdir(f'video/{i}')
        