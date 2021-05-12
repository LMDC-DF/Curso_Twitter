#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase 1. Primera parte

Introducción a Python
"""

#La programación con la que vamos a trabajar se llama imperativa y se ejecuta línea por línea.


3*4+2

#Variables:
"""
Se puede guardar información en variables, usando el signo =, para ser utilizada después
"""

a=2
b=3
(a+b)*2
c=(a+b)*2

#Printear una variable en la consola
print(c)


#Las variables pueden guardar distintos tipos de datos:
# Números (int o float) 
numero_1=1

#palabras (string). Entre ''
texto='Hola, buen día'
texto2='¿Cómo estás?'

texto_total=texto+texto2
print(texto_total)
# listas
lista=[1,2,10,7,9]
#Las listas tienen indices.
lista[2]
lista[0:2]
lista[-1]
#Las listas pueden ser de otros objetos:
lista_palabras=['Mate','Cafe','Harina']
    

#Cada tipo de dato tienen métodos y funciones que se le pueden aplicar. Estos métodos o funciones pueden necesitar o no argumentos:

texto_en_lista=texto.split(' ')
print(texto_en_lista)
lista_palabras.append('Palmitos')
len(lista_palabras)
lista_palabras.extend(lista)


#Usando for podemos recorrer una lista, y hacer lo indicado abajo con cada elemento
lista_nueva=[]
for x in lista:
    print(x)
    lista_nueva.append(x+1) #Es muy importante la identación!!

#A veces se hace comprimido.
lista_nueva=[elemento+1 for elemento in lista]

#El otro control de flujo importante es if, que permite evaluar una condición
if len(lista_palabras)==3:
    lista_palabras.append('Palmitos')
else:
    print(lista_palabras)


#Podemos inventar nuestas propias funciones!
def nuestra_suma(x,y,z):
    resultado=x+y+z
    return(resultado)
    
nuestra_suma(1,3.2,a)    


def nuestro_sumar_uno(lista):
    lista_nueva=[]
    for elemento in lista:
        lista_nueva.append(elemento+1)
    return(lista_nueva)

nuestro_sumar_uno(lista) #Acá la corremos

#Algunas funciones útiles vienen armadas en librerías.
import numpy as np #Librería muy útil para trabajar con vectores

np.mean(lista)
np.max(lista)

#Otras librerías útiles

import pandas as pd #Librería muy útil para trabajar con tablas.

import tweepy #Librería para interactuar con la API de twitter

#Si no tenemos alguna de las librerías la podemos cargar desde la consola con !pip install libreria_faltante

# Vamos a usar la librería armada específicamente para el curso. Para importarla tenemos que estar en la misma carpeta

import codigo_General