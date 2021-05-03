#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 18:23:39 2021

@author: lucia
"""
import importlib.util
import os

path = '/home/tcicchini/Documentos/Cursos/Curso_Twitter/' # Este es el directorio donde está alojado el archivo codigo_General.py
spec = importlib.util.spec_from_file_location('codigo_General', os.path.join(path,'codigo_General.py'))
codigo_General = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codigo_General)


path_proyecto = '/home/tcicchini/Documentos/Cursos/Curso_Twitter/Prueba/' # Este es el nombre del directorio donde está el proyecto. 

#Nombres de los archivos
archivo_tweets = 'PruebaLarreta_Tweets.txt'
archivo_guardado = 'PruebaLarreta_procesado.txt'
archivo_usuarios = 'PruebaLarreta_usuarios.json'
archivo_grafo = 'PruebaLarreta_grafo.gexf'
archivo_grafo_hash = 'PruebaLarreta_grafo_hash.gexf'


#De la bajada de datos no cambie nada.

#Aca procesa y arma 1 csv con los tweets y un json con los usuarios 
codigo_General.procesamiento(path_proyecto + archivo_tweets,
                             path_proyecto + archivo_guardado,
                             path_proyecto + archivo_usuarios)


#Acá se arma el objeto y se cargan los datos (se podría hacer todo junto si queremos)
Larreta=codigo_General.Bases_Datos()
Larreta.cargar_datos(path_proyecto + archivo_guardado)
Larreta.cargar_usuarios(path_proyecto + archivo_usuarios)

#Funciones
Larreta.plot_tipo_tweet()

Larreta.plot_evolucion_temporal()
Larreta.armar_grafo(tipo='usuarios',archivo_grafo=archivo_grafo,tipo_enlace='',dirigido=False)
Larreta.armar_grafo(tipo='hashtags',archivo_grafo=archivo_grafo_hash,tipo_enlace='',dirigido=False)
Larreta.agregar_centrality()
Larreta.plot_nube()
Larreta.plot_nube('veronik50799452')


#En cualquier momento se pueden acceder a las bases con
Larreta.tweets
Larreta.usuarios
Larreta.grafo