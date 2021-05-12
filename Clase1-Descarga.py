#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antes de empezar es necesario tener un usuario para la api de Twitter.
Abrir un proyecto en https://developer.twitter.com/en/apps
Generar las claves y guardarlas en un archivo .txt en la misma carpeta que codigo_General, con el siguiente formato:
    CONSUMER_KEY
    CONSUMER_SECRET
    ACCESS_TOKEN
    ACCES_TOKEN_SECRET
Importamos una librería que se llama codigo_General que tiene todas las funciones que vamos a usar

El código a continuación está armado como ejemplo, pero la idea es que puedan entenderlo para poder usarlo, modificarlo, copiar partes, etc.
"""


import importlib.util
import os

path = '/home/lucia/Escritorio/Curso Redes/Codigos2.0/Curso_Twitter/' # Este es el directorio donde está alojado el archivo codigo_General.py

# Si estamos en la carpeta correcta podemos importar codigo_General import codigo_General

# Para evitar problemas de carpeta podemos en cambio hacer:
spec = importlib.util.spec_from_file_location('codigo_General', os.path.join(path,'codigo_General.py'))
codigo_General = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codigo_General)




# Definimos el conjunto de palabras para realizar la desarga

palabras = ['Alberto Fernandez', 'FMI', 'Club de Paris'] # Defino conjunto de palabras
path_guardado = '/home/tcicchini/Documentos/Cursos/busqueda_12_05_2021' # Defino a dónde quiero que se guarden los archivos
archivo_guardado = 'descarga_12_05_2121.txt' # El nombre del archivo para que se guarden los tweets

# Inicializamos la descarga en vivo con el método Descargar_por_palabra_stream
codigo_General.Descargar_por_palabra_stream(Palabras = palabras, # Le pasamos las palabras para filtrar
                                            Archivo_Tweets = os.path.join(path_guardado,
                                                                          archivo_guardado), # Le pasamos la ubicación y nombre de archivo de destino
                                            idioma = ['es'], # indicamos el idioma
                                            ) 

#Otras opciones

#codigo_General.Descargar_por_palabras(palabras,path+Archivo_Tweets,Cantidad)

#codigo_General.Descargar_por_usuarios(usuario,path+Archivo_Tweets,Cantidad)

