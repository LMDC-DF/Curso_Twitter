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

path = '/home/tcicchini/Documentos/Cursos/Curso_Twitter/' # Este es el directorio donde está alojado el archivo codigo_General.py

#Si estamos en la carpeta correcta podemos importar codigo_General import codigo_General

#Para evitar problemas de carpeta podemos en cambio hacer:
spec = importlib.util.spec_from_file_location('codigo_General', os.path.join(path,'codigo_General.py'))
codigo_General = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codigo_General)


path_proyecto = '/home/tcicchini/Documentos/Cursos/Curso_Twitter/Prueba/' # Este es el nombre del directorio donde está el proyecto.

 #Lugar donde guardaremos todos los archivos de texto (desde la carpeta desde donde estamos corriendo)
Tema='Biden' # (Opcional) Nombre con el que quiero identificar los archivos de este tema
Archivo_Tweets=Tema+'_tweets.txt' #Acá armamos el nombre del archivo donde se van a descargar los tweets
Cantidad=50 #Cantidad de tweets que desceamos para los métodos al pasado 
idioma=['es'] #Idiomas de los tweets que buscamos ('en' si es inglés)

palabras=['Biden'] #Palabras que buscamos para el método por palabras en stream o al pasadp
usuario=['CFKArgentina'] #Usuarios que buscamos para el método por usuarios




#Podemos elegir estos 3 tipos de descargas

codigo_General.Descargar_por_palabra_stream(palabras,path+Archivo_Tweets,idioma)

codigo_General.Descargar_por_palabras(palabras,path+Archivo_Tweets,Cantidad)

codigo_General.Descargar_por_usuarios(usuario,path+Archivo_Tweets,Cantidad)

