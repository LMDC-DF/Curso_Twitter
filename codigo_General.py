# -*- coding: utf-8 -*-

"""
En las siguientes líneas, se definirán las principales clases y funciones a
utilizar en la descarga de datos de la red social twitter, así también como
algunas cuestiones referidas a pre-procesamiento y análisis de los datos

Estas funciones pueden ser llamadas desde otros archivos que estén en la misma carpeta, 
cuando comiencen con la linea
from codigo_General import FuncionAUsar
"""

# ------ Algunas de las librerías que se utilizarán -----------
'''
Algunas de estas librerías son necesario instalar previamente. 
Para eso en la consola correr
!pip install LibreriaFaltante

'''

from tweepy.streaming import StreamListener
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import timedelta
import json
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib_venn import venn3
from wordcloud import WordCloud
import re
import codecs 
import networkx as nx
import community
import string
import os
from os import path
import seaborn as sbn
import nltk
import math
nltk.download('stopwords')
nltk.download('punkt')


#------------Funciones auxiliares--------------

# -------------- Defino una función para sacar tildes de las palabras ---------------------------
def saca_tildes(string):
    '''
    Función auxiliar que se usa en varias funciones para cambiar todas las tildes por su vocal sin tilde
    '''
    string = string.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
    return string

# -------------- Defino una función que lea las claves desde un .txt (por privacidad)-------------

def lector_claves(archivo_claves = 'claves_Twitter.txt'):
    """
    Ingresamos con el nombre del archivo y
    nos devuelve las claves en una lista. Cada elemento corresponde, respectivamente, a:
        CONSUMER_KEY
        CONSUMER_SECRET
        ACCESS_TOKEN
        ACCES_TOKEN_SECRET
    Por default, se define el nombre del archivo de entrada como "claves_Twitter.txt", de forma tal 
    que lo único que hay que hacer es crear ese archivo por única vez con los datos de las claves
    """
    with open(archivo_claves, 'r') as f:
        claves = f.read().split('\n')
    return claves # Variable de salida, las claves ordenadas

def nube_palabras(textos_completos, archivo_imagen = ''):
            """
            La idea de esta función es darle los datos, un rango de fechas, y que 
            nos devuelva la nube de palabras asociada a la discusión durante esas fechas.
            """

            # Incorporamos todos los textos de los tweets a textos

            textos = []
            for t in textos_completos:
                textos.append(re.sub(r'https?:\/\/\S*', '', t, flags=re.MULTILINE).lower())

            es_stop = nltk.corpus.stopwords.words('spanish')
            
            #Filtramos las stopwords y sacamos los .,' y tildes
            
            textos = ''.join(textos).replace(',',' ').replace('.',' ').replace("'",' ').split(' ')
            
            textos_filtrado = list(filter(lambda x: x not in es_stop, textos))
            textos = ' '.join(textos_filtrado)
            textos = saca_tildes(textos)
    
            # Armamos la wordcloud
            wc = WordCloud(width=1600,
                           height=800,
                           background_color = "white",
                           contour_width = 3,
                           contour_color = 'steelblue',
                           max_words = 100,
                           collocations=False).generate_from_text(textos)
            sbn.set_context("paper", font_scale = 2)

            plt.figure(figsize = (10,8), dpi = 100)
            plt.title('Nube de Palabras', fontsize = 20)
            plt.imshow(wc, interpolation='bilinear')
            plt.axis("off")
            if archivo_imagen=="":
                plt.show()
            else:
                plt.savefig(archivo_imagen,bbox_inches='tight')
                plt.show()
            plt.clf()            
            sbn.reset_orig()

#------------FUNCIONES DE DESCARGA -----------
# -------------- Defino las clases y funciones que darán lugar al streamer ------------

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list, languages):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(lector_claves()[0], lector_claves()[1])
        auth.set_access_token(lector_claves()[2], lector_claves()[3])
        
        stream = Stream(auth, listener, tweet_mode = 'extended')
        # This line filter Twitter Streams to capture data by the keywords: 
        if len(hash_tag_list) != 0:
            stream.filter(languages = languages,
                          track = hash_tag_list,
                          )
        else:
            stream.sample(languages = languages)
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
    def on_error(self, status):
        print(status)

#------------------------ Defino función de pesca de la actividad de un determinado usuario ----------------------
def Descargar_por_palabra_stream(Palabras,Archivo_Tweets,idioma):
    bajar_tweets = TwitterStreamer()
    i = 0
    while i < 1000:
        try:
            # Esta es la línea que ejecuta la función
            bajar_tweets.stream_tweets(Archivo_Tweets,
                                       Palabras,
                                       idioma)
        except:
            pass
        i += 1

def Descargar_por_palabras(Palabras,Archivo_Tweets,Cantidad=100):
    
    '''
    Esta función busca descargar y guardar en un archivo todos los tweers (originales, QT o RT) de una lista de usuarios
    
    '''
    
    #Se definen las clavesy los accesos
    auth = OAuthHandler(lector_claves()[0], lector_claves()[1])
    auth.set_access_token(lector_claves()[2], lector_claves()[3])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    Busqueda=Palabras[0]
    for p in Palabras[1:]:
        Busqueda+=' OR '+ p
        
        #Descargar todos los tweets (Cantidad)
    Tweets = tweepy.Cursor(api.search,q=Busqueda,tweet_mode = 'extended').items(Cantidad)
        
        #Guardarlos en el archivo
    for tweet in Tweets:
            with open(Archivo_Tweets, 'a') as tf:
                data=json.dumps(tweet._json)
                tf.write(data)
                tf.write("\n")  
#------------------------ Defino función de pesca de la actividad de un determinado usuario ----------------------

def Descargar_por_usuarios(Usuarios,Archivo_Tweets,Cantidad=100):
    
    '''
    Esta función busca descargar y guardar en un archivo todos los tweers (originales, QT o RT) de una lista de usuarios
    
    '''
    
    #Se definen las clavesy los accesos
    auth = OAuthHandler(lector_claves()[0], lector_claves()[1])
    auth.set_access_token(lector_claves()[2], lector_claves()[3])
    api = tweepy.API(auth, wait_on_rate_limit=True)


    for usuario in Usuarios: #Para cada usuario
        
        #Descargar todos los tweets (Cantidad)
        Tweets = tweepy.Cursor(api.user_timeline,screen_name=usuario,tweet_mode = 'extended').items(Cantidad)
        
        #Guardarlos en el archivo
        for tweet in Tweets:
            tweet = tweet._json
            with open(Archivo_Tweets, 'a') as tf:
                data=json.dumps(tweet)
                tf.write(data)
                tf.write("\n")
#----------------------        

        
class Bases_Datos():
    """
    Clase donde guardaremos toda la información procesada, y desde donde la analizaremos. 
    Está compuesta por métodos para cargar y guardar la información en archivos de texto, métodos para plotear los análisis realizados y métodos para armar y guardar los grafos que podamos leer desde gephi.
    """
    def __init__(self):
        """
        Arma la base de datos con todos sus elementos, empezándola vacía.
        """
        self.tweets=pd.DataFrame() 
        self.usuarios=pd.DataFrame() 
 
        self.grafo=nx.Graph()
        self.grafo_menciones=nx.Graph()
        self.grafo_hashtags=nx.Graph()
 

    def cargar_datos(self,archivo_datos):
        """
        Cargar en Bases_Datos la información procesada sobre los tweets que guardamos en el archivo_datos.
        """
        datos = pd.read_csv(archivo_datos,
                            sep = ',',
                            error_bad_lines = False,
                            dtype = {'tw_id' : object,
                                     'or_id' : object},
                            parse_dates = ['tw_created_at','or_created_at'],
                            date_parser = pd.to_datetime)
        self.tweets=datos 
        
    def cargar_usuarios(self,archivo_usuarios):
        """
        Cargar en Bases_Datos la información procesada sobre los usuarios que guardamos en el archivo_usuario.
        """

        with open(archivo_usuarios) as json_file:
             datos_usuarios= json.load(json_file)
        self.usuarios=datos_usuarios
        
    def cargar_grafo(self,archivo_grafo):
        """
        Volver a cargar el grafo que armamos en caso que lo hayamos modificado.
        """

        self.grafo=nx.read_gexf(archivo_grafo)
        
    def guardar_datos(self,archivo_datos):
        """
        Volver a guardar los datos de los tweets en el archivo_datos en caso que lo hayamos moficiado en Bases_Datos
        """ 
        self.tweets.to_csv(archivo_datos) 
        
    def guardar_usuarios(self,archivo_usuarios):
        """
        Volver a guardar los datos de los usuarios en el archivo_usuarios en caso que lo hayamos moficiado en Bases_Datos
        """
        with open(archivo_usuarios, 'w') as outfile:
            json.dump(self.usuarios, outfile)
            
    def guardar_grafo(self,archivo_grafo):
        """
        Volver a guardar los datos de los grafos en el archivo_usuarios en caso que lo hayamos moficiado en Bases_Datos
        """
        nx.write_gexf(self.grafo, archivo_grafo)


    # Analisis Estadisticos
    def plot_rol_usuario(self,archivo_imagen=''): # Rol de los usuarios a partir de los datos preprocesados 
        """
        Gráfico de torta que muestra el porcentaje de usuarios de todos los tweets mostrados (originales o nuevos) según si escribieron tweets nuevos, citaron o retwitearon.
        Se muestran los usuarios que realizaron más de una acción en las intersecciones.
        """
        usuarios_generadores = set(self.tweets.or_user_screenName.values) #Conjunto de usuarios que tienen tweets originales
        usuarios_retweeteadores = set(self.tweets[self.tweets.relacion_nuevo_original == 'RT'].tw_user_screenName.values) #Conjunto de usuarios que retwitearon tweets
        usuarios_citadores = set(self.tweets[self.tweets.relacion_nuevo_original == 'QT'].tw_user_screenName.values) #Conjunto de usuarios que citaron
        
        total_usuarios = len(usuarios_generadores.union(usuarios_retweeteadores).union(usuarios_citadores)) #Cantidad total de todos los usuarios
        
        
        #Realizar la la figura
        sbn.set_context("paper", font_scale = 1.5)        
        plt.figure(figsize = (11,8), dpi = 300) 
        plt.title('Rol de los Usuarios', fontsize = 20)
        v = venn3([usuarios_retweeteadores, usuarios_generadores, usuarios_citadores],
                  set_labels = ('Lxs que retweetean', 'Lxs que generan', 'lxs que citan'),
                  )
        for indice in ['100','110','101','010','011','001','01','10','11','111']:
            try:
                v.get_label_by_id(indice).set_text('{}%'.format(round(int(v.get_label_by_id(indice).get_text())*100/total_usuarios,1)))
            except:
                pass
        plt.text(-.05,-.65,'El total de usuarios registrados durante el período fue de : {}'.format(total_usuarios))

        if archivo_imagen=='':
            plt.show()
        else:
            plt.savefig(archivo_imagen,bbox_inches='tight')
            plt.show()
        
        plt.clf()
        sbn.reset_orig()


    def plot_tipo_tweet(self, archivo_imagen = ''):
        """
        Esta función toma como entrada el archivo de datos preprocesados y
        devuelve una imagen tipo diagrama de Venn con el tipo de tweets pescados
        """
        #Levantar los datos preprocesados del archivo
    
        originales = set(self.tweets.tw_id.values) #Conjunto de tweets originales
        rt = set(self.tweets[self.tweets.relacion_nuevo_original == 'RT'].or_id.values) #Conjunto de retweets
        citas = set(self.tweets[self.tweets.relacion_nuevo_original == 'QT'].or_id.values) #Conjunto de citas    
        total_tweets = len(originales.union(rt).union(citas)) #Cantidad total de tweets
        
        # Realizar la figura
        labels = ['RT', 'Originales', 'QT'] 
        sizes = [100 * len(rt) / total_tweets, 100 * len(originales) / total_tweets, 100 * len(citas) / total_tweets]
        
        sbn.set_context("paper", font_scale = 1.5)
        
        plt.figure(figsize = (11,8), dpi = 300)
        plt.title('Tipos de Tweets', fontsize = 20)
        plt.pie(sizes, autopct='%1.1f%%')
        plt.legend(labels)
        plt.axis('equal')
        plt.text(-.1,-1.2,'El total de tweets registrados durante el período fue de : {}'.format(total_tweets))
        if archivo_imagen=='':
            plt.show()
        else:
            plt.savefig(archivo_imagen,bbox_inches='tight')
            plt.show()
        plt.clf()
        sbn.reset_orig()
        
    def plot_evolucion_temporal(self, archivo_imagen = '',fecha_inicial = '',fecha_final = '', frecuencia = '15min'):
        """
        Esta función toma como entrada el archivo de datos preprocesados y 
        devuelve la evolución temporal de cantidad de tweets, RT y QT
        
        fecha_inicial : str
        		 indicamos la fecha apartir de la cual consideramos el análisis. Si no ponemos nada, se setea en la fecha y hora de inicio de descarga
        fecha_final : str
        		indicamos la fecha de corte del análisis. Por default, es la correspondiente al final de la descarga
        frecuencia : str
        		indica cada cuanto bineamos los datos temporalmente. Tiene que ser de la forma '1min', '1seg', '1h','1d'. Osea, número más algo que indique la cantidad
        archivo_imagen : str
        		nombre que le pondremos al gráfico de querer guardarlo
        
        """
        if fecha_final=='':
            fecha_final=max(self.tweets['tw_created_at'])
        else:
            fecha_final=pd.to_datetime(fecha_final).tz_localize('UTC')
        if fecha_inicial=='':
            fecha_inicial=min(self.tweets['tw_created_at'])
        else:
            fecha_inicial=pd.to_datetime(fecha_inicial).tz_localize('UTC')
        
        d = self.tweets[['or_id', 'or_created_at']].drop_duplicates().rename({'or_id' : 'id', 'or_created_at' : 'fecha'}, axis = 1)
        d['relacion'] = 'Original'
        d = d.append(self.tweets[['tw_id','tw_created_at','relacion_nuevo_original']].rename({'tw_id' : 'id', 'tw_created_at' : 'fecha', 'relacion_nuevo_original' : 'relacion'}, axis = 1))
        #d['fecha'] = d['fecha'].apply(pd.to_datetime, utc = None)
        d = d[d.fecha.between(fecha_inicial, fecha_final)]
        d = d.groupby([pd.Grouper(key = 'fecha',
                                  freq = frecuencia),
                       'relacion']).count().reset_index().rename({'relacion' : 'Tipo de Tweet'}, axis = 1)
        sbn.set_context("paper", font_scale = 2)
        fig, ax = plt.subplots(figsize = (11,8))
        sbn.lineplot(x = 'fecha', y = 'id', data = d[d['Tipo de Tweet'] != 'RT'], hue = 'Tipo de Tweet', ax = ax)
        ax_2 = ax.twinx()
        sbn.lineplot(x = 'fecha', y = 'id', data = d[d['Tipo de Tweet'] == 'RT'], label = 'RT', ax = ax_2, color = 'green')
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax_2.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax_2.legend(lines + lines2, labels + labels2, loc='upper left')
        ax_2.set_ylabel('Cantidad de RT',)
        ax.set_ylabel('Cantidad de Tweets y QT',)
        ax.set_xlabel('Fecha',)
        ax.set_title('Evolución Temporal',)
        ax.grid(linestyle = 'dashed')
        ax.tick_params(axis='x', rotation=45)
        if archivo_imagen == '':
            plt.show()
        else:
            plt.savefig(archivo_imagen,bbox_inches='tight')
            plt.show()
        plt.clf()            
        sbn.reset_orig()
        

    # ----- Armar grafos para usar en Gephi
    def armar_grafo(self,tipo='usuarios',archivo_grafo='',tipo_enlace='',dirigido=False):
    
        
        '''
        A partir de los datos de retweets preprocesados se arma un grafo con los usuarios como nodos, con los atributos del archivo_atributos
        y los retweets como aristas, pesados por la cantidad de retweets que hubo entre cada enlace, y las posibilidades
        de elegir si en grafo es o no dirigido, y si utilizar los RT, las QT o ambas.
        '''    
        G=nx.Graph()
    
        if tipo=='usuarios':
            # Elegir si el grafo es dirigido o no
            if dirigido:
                G = nx.DiGraph()            
            
            
            datos = self.tweets
            #Elegir si nos quedamos con los enlaces RT, QT (o ambos)    
            if tipo_enlace == 'RT' or tipo_enlace == 'QT':
                datos = self.tweets[self.tweets.relacion_nuevo_original == tipo_enlace]
          
            
            enlace_peso={} #diccionario para poner cada enlace y su peso                      
            for i in range(len(datos)): #Para cada RT y/o QT
                try:
                    enlace_peso [(datos.tw_user_screenName.values[i], datos.or_user_screenName.values[i])]+=1 #Si ya existe sumar una al enlace
                except:
                    enlace_peso [(datos.tw_user_screenName.values[i], datos.or_user_screenName.values[i])]=1 #Si no exista agregar el enlace
                G.add_edge(datos.tw_user_screenName.values[i], datos.or_user_screenName.values[i],relacion=self.tweets.relacion_nuevo_original.values[i]) #Agregar los enclaces
            
            nx.set_edge_attributes(G,enlace_peso,'weight') #Agregar los pesos


            comunidades_louvain = community.best_partition(G)
            
            for us in self.usuarios.keys():
                self.usuarios[us]['Comunidad_Louvain']=comunidades_louvain[us]    
            #Agregar los atributos si está el archivo correspondiente
            nx.set_node_attributes(G,self.usuarios)                
            self.grafo=G
        else:

            if tipo=='menciones':
               texto_usuario_original = self.tweets[['or_menciones','or_user_screenName']].drop_duplicates().dropna()+self.tweets[['or_menciones','tw_user_screenName']].drop_duplicates().dropna()
               texto_usuario_original = texto_usuario_original.groupby(['or_user_screenName'])['or_menciones'].apply(' '.join)        
            elif tipo=='hashtags':
               texto_usuario_original = self.tweets[['or_hashtags','or_user_screenName']].drop_duplicates().dropna()+self.tweets[['or_hashtags','tw_user_screenName']].drop_duplicates().dropna()
               texto_usuario_original = texto_usuario_original.groupby(['or_user_screenName'])['or_hashtags'].apply(' '.join)  
            else:
                print('tipo solo puede ser usuarios, menciones o hashtags')
       
            hashtag_ocurrencia = {} #Cantidad de veces que aparece cada hashtag
            enlace_peso = {} #Peso de las aristas (cantidad de tweets que comparten)
            for i in range(len(texto_usuario_original)): #Recorrer las listas de hastgas/menciones de cada tweet
                #Armar para cada tweet una lista con los hashtags/menciones
                try:
                    lista_hashtags_i = sorted(texto_usuario_original.values[i].split(' '))
                    aux = lista_hashtags_i.count('')
                    while aux > 0:
                        lista_hashtags_i.remove('')
                        aux = lista_hashtags_i.count('')
                except:
                    lista_hashtags_i = sorted(texto_usuario_original.values[i].split(' '))
        
                if len(lista_hashtags_i) != 1: #si hay más de uno
                    for j in range(len(lista_hashtags_i)): #Para cada hastag
                        try: #Si ya está en ocurrencia sumar uno
                            hashtag_ocurrencia[saca_tildes(lista_hashtags_i[j].lower())] += 1
                        except: #Si no está agregar
                            hashtag_ocurrencia[saca_tildes(lista_hashtags_i[j].lower())] = 1
                        for k in range(j + 1,len(lista_hashtags_i)): #Recorrer todos los otros hashtags que compartieron ese tweet
                            try: #Si ya estaba la arista sumar uno
                                enlace_peso[(saca_tildes(lista_hashtags_i[j].lower()),saca_tildes(lista_hashtags_i[k].lower()))] += 1
                            except: #Si no estaba agregarla
                                enlace_peso[(saca_tildes(lista_hashtags_i[j].lower()),saca_tildes(lista_hashtags_i[k].lower()))] = 1
                                
            #Agregar todas las aristas con su peso
            for item in enlace_peso.items():
                G.add_edge(item[0][0],item[0][1], weight = item[1])
            
            #Separar en comunidades
            comunidades_louvian = community.best_partition(G)
            
            #Agregar las comunidades y la cantidad de apariciones como atributos
            nx.set_node_attributes(G, comunidades_louvian, 'Comunidad_Louvain')
            nx.set_node_attributes(G, hashtag_ocurrencia, 'Impacto')
            if tipo=='menciones':
                self.grafo_menciones=G
            elif tipo=='hashtags':
                self.grafo_hashtags=G
                
        #Escribir el grafo en un archivo gexf
        if archivo_grafo!='':
            nx.write_gexf(G, archivo_grafo)
        #Devolver el grafo
        return G
    
    def agregar_centrality(self,centrality='grado'):
        '''
        La idea de esta función es recibir un grafo y devolver un archivo con la lista de nodos
        ordenados por su centralidad.
        Como centralidad puede elegirse 'grado','eigenvector' o 'betweenees'.
        '''
        #Elegir la centralidad y calcularla sobre el grafo
        if centrality=='grado':
            centralidad=nx.degree_centrality(self.grafo)
        elif centrality=='eigenvector':
            centralidad=nx.eigenvector_centrality(self.grafo)
        elif centrality=='betweeness':
            centralidad=nx.betweenness_centrality(self.grafo)
        else:
            print('La centralidad solo puede ser grado, eigenvector o betweeness')
            
    
        nx.set_node_attributes(self.grafo, centralidad, 'Centralidad '+ centrality)
    

  

    def plot_nube(self, usuarios = None, archivo_imagen = '',fecha_inicial = '', fecha_final = ''): 
            """
            Gráfico de una nube de palabras principales de los tweets.
            Utilizándo el parámetro usuarios se puede utilizar de tres maneras.
            Si no se completa se graficará la nube de todos los tweets levantados
            Si se completa con el screen_name de un usuario (entre comillas) se mostrará la nube de todos los tweets escritos por esa persona
            Si se completa con el screen_name de varios usuarios (entre corchetes y comillas: ['usuario1','usuario2','usuario3'] ) se mostrará la nube de todos los tweets escritos por ese conjunto de personas             
            Se pueden usar los parámetros fecha_inicial y fecha_final para filtrar por fechas. Si no se completa se utilizarán todos los tweets realizados entre los tiempos de levantados (esto no incluye tweets más viejos que hayan sido retwiteados y citados)
            """
        
            if fecha_final=='':
                fecha_final=max(self.tweets['tw_created_at'])
            else:
                fecha_final=pd.to_datetime(fecha_final).tz_localize('UTC')
            if fecha_inicial=='':
                fecha_inicial=min(self.tweets['tw_created_at'])
            else:
                fecha_inicial=pd.to_datetime(fecha_inicial).tz_localize('UTC')

            #Separamos según si son datos de retweets o los tweets de un usuario  
            if usuarios == None:
                datos = self.tweets.copy()
            elif type(usuarios) == str:
                datos = self.tweets[(self.tweets.tw_user_screenName == usuarios) | (self.tweets.or_user_screenName == usuarios)].copy()
                
            elif type(usuarios) == list:
                datos = self.tweets[(self.tweets.tw_user_screenName.isin(usuarios)) | (self.tweets.or_user_screenName.isin(usuarios))].copy()
            #datos.fecha_original = pd.to_datetime(datos.fecha_original) #Pasar a formato fecha
            #datos.fecha_nuevo = pd.to_datetime(datos.fecha_nuevo) #Pasar a formato fecha
            textos_originales = datos[datos.or_created_at.between(fecha_inicial, fecha_final)].or_text.drop_duplicates().values #Quedarse con los textos originales en las fechas correctas
            textos_qt = datos[(datos.tw_created_at.between(fecha_inicial,fecha_final)) & (datos.relacion_nuevo_original == 'QT')].tw_text.drop_duplicates().values #Quedarse con los textos de las citas en las fechas correctas
            # No incluimos RT, porque el texto es el mismo que en el original
            textos_completos=np.hstack([textos_originales,textos_qt])
            nube_palabras(textos_completos, archivo_imagen )
    
    def plot_principales_Hashtags(self, archivo_imagen = '', fecha_inicial = '', fecha_final = ''):
        """
        Gráfico de los principales Hashtags utilizados en todos los tweets.
        Se pueden usar los parámetros fecha_inicial y fecha_final para filtrar por fechas. Si no se completa se utilizarán todos los tweets realizados entre los tiempos de levantados (esto no incluye tweets más viejos que hayan sido retwiteados y citados)

        """
        
        if fecha_final=='':
            fecha_final=max(self.tweets['tw_created_at'])
        else:
            fecha_final=pd.to_datetime(fecha_final).tz_localize('UTC')
        if fecha_inicial=='':
            fecha_inicial=min(self.tweets['tw_created_at'])
        else:
            fecha_inicial=pd.to_datetime(fecha_inicial).tz_localize('UTC')

        d = self.tweets[(self.tweets.tw_created_at.between(fecha_inicial, fecha_final))|((self.tweets.relacion_nuevo_original=='Original') & (self.tweets.or_created_at.between(fecha_inicial, fecha_final)))].copy()
        
        datos = pd.DataFrame(data = {'Hashtags' : ' '.join(d.tw_hashtags.dropna().values).split()})['Hashtags'].value_counts().sort_values(ascending = True)
        
        sbn.set_context("paper", font_scale = 2)
        fig, ax = plt.subplots(figsize = (11,8))
        datos.plot(kind = 'barh', ax = ax)
        ax.barh(y = range(len(datos)),
                width = datos.values,
                color = plt.get_cmap('Set2').colors,
                tick_label = datos.keys())
        ax.grid(linestyle = 'dashed')
        ax.set_xlabel('Cantidad de Apariciones')
        ax.set_title('Hashtags Principales')
        if archivo_imagen == '':
            plt.show()
        else:
            plt.savefig(archivo_imagen,bbox_inches='tight')
            plt.show()            
        sbn.reset_orig()
    
    def plot_principales_Usuarios(self, metrica_interes = 'or_rtCount',archivo_imagen = '', fecha_inicial = '', fecha_final = '', cant_usuarios = 10):
        """
        Gráfico que muestra los usuarios principales.
        Con el parámetrio metrica_interes se puede elegir qué metrica utilizar.
        COMPLETAR LAS METRICAS
        Se pueden usar los parámetros fecha_inicial y fecha_final para filtrar por fechas. Si no se completa se utilizarán todos los tweets realizados entre los tiempos de levantados (esto no incluye tweets más viejos que hayan sido retwiteados y citados)

        """
        if fecha_final=='':
            fecha_final=max(self.tweets['tw_created_at'])
        else:
            fecha_final=pd.to_datetime(fecha_final).tz_localize('UTC')
        if fecha_inicial=='':
            fecha_inicial=min(self.tweets['tw_created_at'])
        else:
            fecha_inicial=pd.to_datetime(fecha_inicial).tz_localize('UTC')
            
        d = self.tweets[self.tweets.or_created_at.between(fecha_inicial, fecha_final)].copy()
        d = d.drop_duplicates(subset = 'or_id', keep = 'last') # Nos quedamos con los or_id únicos, correspondientes al último que fue replicado, así las métricas son las más actualizadas
        d_sum = d.groupby('or_user_screenName')[metrica_interes].sum().reset_index().rename({metrica_interes : metrica_interes[3:]}, axis = 1) # Sumamos las métricas en cuestión de todos los tweets de un usuario
        d_count = d.groupby('or_user_screenName')[metrica_interes].count().reset_index().rename({metrica_interes : 'Cantidad de Tweets'}, axis = 1) # Contamos los tweets distintos generados por el usuario, para también reportar esto
        
        d = d_sum.merge(d_count, on = 'or_user_screenName').sort_values(metrica_interes[3:], ascending = False)
        d['Promedio'] = (d[metrica_interes[3:]] / d['Cantidad de Tweets']).apply(round, 3)
        
        sbn.set_context("paper", font_scale = 2)
        fig, ax = plt.subplots(figsize = (7,11), dpi = 200)
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText = d.values[:cant_usuarios], colLabels = d.columns, loc='center')
        if archivo_imagen == '':
            plt.show()
        else:
            plt.savefig(archivo_imagen,bbox_inches='tight')
            plt.show()            
        sbn.reset_orig()
    
    def plot_usuarios_Tendencia():
        
        return None


# -------------- Defino una función de lectura y pre-procesamiento del archivo con los tweets descargados ------------


def guardar_tweet(tweet):
            """
            Función auxiliar que utilizaremos en la función procesar
            """
            data={}
            data['tw_id']=tweet['id_str']
            data['tw_created_at']=pd.to_datetime(tweet['created_at'])
            try:
                data['tw_text']=tweet['extended_tweet']['full_text'].replace('\n',' ').replace(',',' ')
            except:
                try:
                    data['tw_text']=tweet['full_text'].replace('\n',' ').replace(',',' ')
                except:
                    data['tw_text']=tweet['text'].replace('\n',' ').replace(',',' ')

            data['tw_favCount']=tweet['favorite_count']
            data['tw_rtCount']=tweet['retweet_count']
            try:
                data['tw_qtCount']=tweet['quote_count']
            except:
                data['tw_qtCount']=""
            try:
                data['tw_rpCount']=tweet['reply_count']
            except:
                data['tw_rpCount']=""
            try:
                data['tw_location']=tweet['place']['full_name'].replace(',',' ')
            except:
                data['tw_location']=' '
            data['user_id']=tweet['user']['id_str']
            data['user_screenName']=tweet['user']['screen_name']
            data['user_followers_count'] = tweet['user']['followers_count']
            hashtags = ''
            if len(tweet['entities']['hashtags']) != 0:
                for h in tweet['entities']['hashtags']:
                    hashtags += h['text'] + ' '
            data['tw_hashtags']=hashtags
            menciones = ''
            if len(tweet['entities']['user_mentions']) != 0:
                for um in tweet['entities']['user_mentions']:
                    menciones += um['screen_name'] + ' '
            data['tw_menciones'] = menciones
            
                        
            return data
    
def guardar_usuario(usuario):
        """
        Función auxiliar que utilizaremos en la función procesar
        """

        data={}
        data['id_str']=usuario['id_str']
        data['screen_name']=usuario['screen_name']
        try:
            data['description']=usuario['description'].replace('\n',' ')
        except:
            data['description']=' '
        data['verified']=usuario['verified']
        data['followers_count']=usuario['followers_count']
        data['friends_count']=usuario['friends_count']
        data['listed_count']=usuario['listed_count']
        data['favourites_count']=usuario['favourites_count']
        data['statuses_count']=usuario['statuses_count']
        data['created_at']=usuario['created_at']
        data['location']=usuario['location']
        if usuario['location'] is None:
            data['location']=' '
            
        return(data)

def procesamiento(archivo_tweets,archivo_guardado,archivo_usuarios):
        """
        Función que utiliza la información descargada por tweepy y guardada en archivo_tweets.
        Devuelve dos archivos archivo_guardado y archivo_usuarios que pueden ser cargados en Bases_Datos.
        """
        usuarios={}
        with open(archivo_guardado, 'w', encoding = 'utf-8') as arch:
                    arch.write(','.join([
                            
            'tw_id' , # id del tweet
            'tw_created_at', # fecha de creacion
            'tw_text' , # texto
            'tw_favCount' , # cantidad de megustas
            'tw_rtCount' , # cantidad de rt
            'tw_qtCount' , # cantidad de citas
            'tw_rpCount' , # cantidad de comentarios
            'tw_location' , # location del tweet (usaremos el place)
            'tw_user_id' , # id del usuario
            'tw_user_screenName', # screen name del usuario
            'tw_user_followers_count',
            'tw_hashtags',
            'tw_menciones',
                              
                               
            'or_id', # id del tweet
            'or_created_at', # fecha de creacion
            'or_text', # texto
            'or_favCount', # cantidad de megustas
            'or_rtCount', # cantidad de rt
            'or_qtCount', # cantidad de citas
            'or_rpCount', # cantidad de comentarios
            'or_location', # location del tweet (usaremos el place)
            'or_user_id' , # id del usuario
            'or_user_screenName', # screen name del usuario
            'or_user_followers_count',
            'or_hashtags',
            'or_menciones',
            
            'relacion_nuevo_original',]))
                    arch.write('\n')

        with open(archivo_tweets, 'r', buffering = 1000000) as f:
            for line in f.read().split('\n'):
                if len(line) != 0:

                    tweet = json.loads(line) # Transformamos la línea (osea el tweet) en un json (diccionario anidado)
                    usuario=tweet['user']
                    usuarios[usuario['screen_name']]=guardar_usuario(usuario)
                    if 'retweeted_status' in tweet.keys(): #Si el original es cita
                        tweet_original = tweet['retweeted_status'] 
                        usuario=tweet_original['user']
                        usuarios[usuario['screen_name']]=guardar_usuario(usuario)

                        relacion_nuevo_original = 'RT' #Guardamos que la relación es un retweet
                        
                        #Guardamos toda la fila
                        with open(archivo_guardado, 'a', encoding = 'utf-8') as arch:
                            arch.write(','.join([str(i) for i in guardar_tweet(tweet).values()]))
                            arch.write(',')
                            arch.write(','.join([str(i) for i in guardar_tweet(tweet_original).values()]))
                            arch.write(',')
                            arch.write('{}\n'.format(relacion_nuevo_original))                    #Citas
                    elif 'quoted_status' in tweet.keys(): #Si el original es una cita
                        tweet_original = tweet['quoted_status']
                        usuario=tweet_original['user']
                        usuarios[usuario['screen_name']]=guardar_usuario(usuario)
  
                        relacion_nuevo_original = 'QT' #Guardamos que la relación es un retweet
    
                        with open(archivo_guardado, 'a', encoding = 'utf-8') as arch:
                            arch.write(','.join([str(i) for i in guardar_tweet(tweet).values()]))
                            arch.write(',')
                            arch.write(','.join([str(i) for i in guardar_tweet(tweet_original).values()]))
                            arch.write(',')
                            arch.write('{}\n'.format(relacion_nuevo_original))
                    else:
                        relacion_nuevo_original = 'Original' #Guardamos que la relación es un retweet
                        with open(archivo_guardado, 'a', encoding = 'utf-8') as arch:
                            arch.write(','.join(['' for i in guardar_tweet(tweet).values()]))
                            arch.write(',')
                            arch.write(','.join([str(i) for i in guardar_tweet(tweet).values()]))
                            arch.write(',')
                            arch.write('{}\n'.format(relacion_nuevo_original))   
                    
                    with open(archivo_usuarios, 'w') as outfile:
                        json.dump(usuarios, outfile)            
                    


                


