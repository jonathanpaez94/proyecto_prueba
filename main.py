import os
import cv2
import time
from datetime import datetime, timedelta
from correo import enviar_correo
from gestion_directorio import eliminar_directorio





# Salida de video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
modo_fuera_casa = False

while True:
    captura = cv2.VideoCapture(0)

    # Properties
    frame_width = int(captura.get(3))
    frame_height = int(captura.get(4))
    fps = captura.get(cv2.CAP_PROP_FPS)
    delay = 1/fps

    grabar = False
    control_nombre_archivo = True

    fecha_inicial = datetime.now()
    tiempo_grabacion = datetime.now() + timedelta(minutes=1)
    
    while (captura.isOpened()):
        ret, frame1 = captura.read()
        ret, frame2 = captura.read()

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (21, 21), 0)
        thresh = cv2.threshold(blur,30,255,cv2.THRESH_BINARY)[1]
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Filtra los contornos pequeños que probablemente son ruido
            if cv2.contourArea(contour) < 500:
                continue
            else:
                # Deteccion de movimiento
                tiempo_grabacion = datetime.now() + timedelta(minutes=1)
                #print(tiempo_grabacion)
                grabar = True
        
        # Nombre del archivo teniendo en cuenta la deteccion de movimiento
        if grabar == True and control_nombre_archivo == True:
            fecha_inicial = datetime.now()
            nombre_archivo = f'output_{fecha_inicial.strftime("%d_%b_%Y_%H_%M_%S")}.avi'
            directorio = f'video/{fecha_inicial.strftime("%d_%b_%Y")}'
            directorio_archivo = f'{directorio}/{nombre_archivo}'

            if not os.path.exists(directorio): 
                os.makedirs(directorio, mode=0o777, exist_ok=True)

            salida = cv2.VideoWriter(directorio_archivo, fourcc, 60, (frame_width, frame_height))
            control_nombre_archivo = False
            
        # Control duracion maxima de video con movimiento
        if  datetime.now() > (fecha_inicial + timedelta(minutes=5)):
            if grabar == True:
                print("Terminado al tiempo maximo")
                break

        # Control duracion de video con movimiento
        if tiempo_grabacion < datetime.now():
            print("Terminado por no detectar mas movimiento")
            break 

        # Validacion de fotograma
        if ret == True:
            cv2.imshow('video', frame1)
            if grabar == True and control_nombre_archivo == False:
                salida.write(frame1)
                
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
        else: 
            break

        eliminar_directorio()
        time.sleep(delay)

    captura.release()
    salida.release()
    cv2.destroyAllWindows()

    if grabar == True:
        if modo_fuera_casa == True: 
            print("Enviar correo")
            #enviar_correo(f'Movimiento detectado, ver video {nombre_archivo}')
    else:
        # Borra archivo si no se activo la grabacion
        if os.path.exists(directorio_archivo):
            os.remove(directorio_archivo)
        pass
    time.sleep(0.25)


