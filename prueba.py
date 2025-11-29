import os 
from datetime import datetime

fecha_inicial = datetime.now()
directorio = f'video/16_Nov_2025'
if not os.path.exists(directorio): 
    os.makedirs(directorio, mode=0o777, exist_ok=True)