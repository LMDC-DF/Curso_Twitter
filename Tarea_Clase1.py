
'''
Consigna: En lista Tweets tenemos el texto de 5 tweets.

Crear una nueva variable Lista_Palabras, del tipo lista, y colocar ahí los strings de todas las palabras que aparecen en los 5 Tweets.

Extra: Intentar que las palabras que aparecen repetidas en los tweets aparezcan una sola vez en la lista (es posible que tengan que googlear algún método de las listas para lograr eso.)
Extra2: Intentar que los links que aparecen en algunos Tweets no aparezcan en las listas de palabras.
'''

Lista_Tweets=['Pentágono: Tenemos controlado al #CoheteChino El cohete: https://t.co/YCpSeHw7m8',
              'Cuando te querías suicidar y te enteras que estás cerca de la zona de impacto del #CoheteChino https://t.co/Cf3IyIvlSP',
              'Este video queda mejor con el opening de Dragon Ball Z 😌 #CoheteChino https://t.co/Uzfn33oVME',
              'Ahora los medios internacionales se refieren al #CoheteChino como Long March 5B  lo mismo ocurrió con el #VirusChino al cual prefirieron llamarlo SARSCoV2  pero sus variantes sí son nombradas según el país donde son descubiertas…  El comunismo controlando el mundo.',
              '#CoheteChino //// nosotros vemos la luna llena (completamente redonda)   los chinos    también (!!!!????!!?)']

'''
Lista_Palabras=[]
for tweet in Lista_Tweets:
    tweet=tweet.split(' ')
    #Lista_Palabras.extend(tweet)
    Lista_Palabras.extend([palabra for palabra in tweet if 'https:' not in palabra])
Lista_Palabras=list(set(Lista_Palabras))
'''


Lista_Palabras=[]
for tweet in Lista_Tweets:
    tweet=tweet.split(' ')
    for palabra in tweet:
        if palabra not in Lista_Palabras:
            if 'https:' not in palabra:
                Lista_Palabras.append(palabra)
                