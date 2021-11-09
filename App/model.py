"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.bst import put
import config as cf
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
import datetime
assert cf


# Construccion de modelos
def newCatalog():
    catalogo = {}
    catalogo["info"]= lt.newList('SINGLE_LINKED', compareDates)
    catalogo['Ciudad'] = mp.newMap(15225, maptype='PROBING', loadfactor=4.0)
    catalogo['Duracion'] = om.newMap(omaptype="RBT", comparefunction=compareDuration)
    catalogo['Fechas'] = om.newMap(omaptype="RBT", comparefunction=compareDate)

    return catalogo

# Funciones para agregar informacion al catalogo
def addUFO(catalog, ufo):

    lt.addLast(catalog["info"], ufo)
    ufobyduration(catalog,ufo)
    ufobydate(catalog,ufo)

    ufoInfo = {'datetime':ufo['datetime'],'duration':ufo['duration (seconds)'], 'shape':ufo['shape']} 

    c=ufo['city']
    if ufo["city"]=="":
        c="city"
    date1=ufo["datetime"]
    date1 =datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')

    b=mp.get(catalog['Ciudad'], c)

    if b is not None:
        a=me.getValue(b)
        om.put(a, date1.date(), ufoInfo)
           
    else:

        tree=om.newMap(omaptype='BST', comparefunction=compareDates)
        om.put(tree, date1.date(), ufoInfo)
        mp.put(catalog['Ciudad'],c,tree)

def ufobyduration(catalog,ufo):
    
    ufoInfo = {'datetime':ufo['datetime'],'city': ufo['city'], 'duration (sec)': ufo['duration (seconds)'],'shape':ufo['shape'],
    'state':ufo['state'],'country':ufo['country']} 

    duration=float(ufo['duration (seconds)'])

    inCatalog=om.get(catalog['Duracion'], duration)

    if inCatalog is not None:
        llave=me.getValue(inCatalog)
        lt.addLast(llave,ufoInfo)
        
           
    else:
        info=lt.newList("ARRAY_LIST",cmpfunction=compareCityState, key=None)
        lt.addLast(info,ufoInfo)
        om.put(catalog["Duracion"], duration, info)

def ufobydate(catalog,ufo):
    
    ufoInfo = {'datetime':ufo['datetime'],'city': ufo['city'], 'duration (sec)': ufo['duration (seconds)'],'shape':ufo['shape'],
    'country':ufo['country']} 

    date=ufo["datetime"].split(" ")
    date=date[0].replace("-","")
    date=int(date)

    inCatalog=om.get(catalog['Fechas'], date)

    if inCatalog is not None:
        llave=me.getValue(inCatalog)
        lt.addLast(llave,ufoInfo)
         
    else:
        info=lt.newList("ARRAY_LIST",cmpfunction=compareDatetime, key=None)
        lt.addLast(info,ufoInfo)
        om.put(catalog["Fechas"], date, info)

# req 1   
def ufoporciudad(catalog,city):
    if om.contains(catalog,city):
        ufos=om.get(catalog,city)
        ufos=me.getValue(ufos)
    return ufos

# Funciones para creacion de datos

# Funciones de consulta
def listsize(listaufo):
    return lt.size(listaufo)

#Requerimiento 1
def citysightings(ciudad):
    return None


#Requerimiento 2
"""Revisar Ordenamiento de Ciudad-Estado"""

def max_duration(catalog):
    avistamiento_mayor_duracion=om.maxKey(catalog)
    return avistamiento_mayor_duracion

def sightingsdurationrange(catalog,lim_inferior, lim_superior):

    duracion_rango=om.values(catalog,lim_inferior, lim_superior)
    muestra = first_last_three (duracion_rango)

    size=0
    for element in lt.iterator(duracion_rango):
        size+=lt.size(element)

    return muestra, size

def first_last_three (rango):

    UFOS=lt.firstElement(rango)
    primerUFOS=lt.subList(UFOS,1,3)
    ultimoUFOS=lt.lastElement(rango)
    ultimoUFOS=lt.subList(UFOS,(lt.size(ultimoUFOS)-3),3)
    return primerUFOS,ultimoUFOS

#Requerimiento 3
def sightingsperhourminute(lim_inferior,lim_superior):
    return None

#Requerimiento 4
"""Revisar el size de fecha rango sale 39 en vez de 45"""
def min_date(catalog):
    avistamiento_menor_fecha=str(om.minKey(catalog))
    avistamiento_menor_fecha=avistamiento_menor_fecha[0:4]+"-"+avistamiento_menor_fecha[4:6]+"-"+avistamiento_menor_fecha[6:8]
    return avistamiento_menor_fecha

def sightingsperdate(catalog,lim_inferior,lim_superior):

    fechas_rango=om.values(catalog,lim_inferior, lim_superior)
    muestra = first_last_three (fechas_rango)

    size=lt.size(fechas_rango)
    print(size)
    return muestra, size

def first_last_three (rango):

    tamanio_muestra=3
    primerosUFOS=lt.newList("ARRAY_LIST")
    ultimosUFOS=lt.newList("ARRAY_LIST")

    while tamanio_muestra!=0:
        UFOS=lt.removeFirst(rango)
        tam= lt.size(UFOS)
        if tam>=3:
            primerUFOS=lt.subList(UFOS,1,tamanio_muestra)
            lt.addLast(primerosUFOS,primerUFOS)
            tamanio_muestra=0
        else:
            primerUFOS=lt.subList(UFOS,1,tam)
            lt.addLast(primerosUFOS,primerUFOS)
            tamanio_muestra-=tam

    tamanio_muestra=3
    while tamanio_muestra!=0:
        ultimoUFOS=lt.removeLast(rango)
        tam= lt.size(UFOS)
        if tam>=3:
            ultimoUFOS=lt.subList(UFOS,(lt.size(ultimoUFOS)-3),tamanio_muestra)
            lt.addFirst(ultimosUFOS,ultimoUFOS)
            tamanio_muestra=0
        else:
            primerUFOS=lt.subList(UFOS,1,tam)
            lt.addFirst(ultimosUFOS,ultimoUFOS)
            tamanio_muestra-=tam

    return primerosUFOS,ultimosUFOS

#Requerimiento 5
def countsightingsbyzone(lim_inferior,lim_superior):
    return None

#Requerimiento 6
def countsightingsbyzone(lim_inferior,lim_superior):
    return None

# Funciones utilizadas para comparar elementos dentro de una lista

def BYDATE(DATE1,DATE2):
    if DATE1!="":
        fecha=DATE1.strip("-: ")
        fecha=int(fecha)
    else:
        fecha=0

    if DATE2!="":
        fecha1=DATE2.strip("-: ")
        fecha1=int(fecha)
    else:
        fecha1=0

    return fecha>fecha1

# Funciones de ordenamiento
def ordenamientoAlfabetico(ciudad1,ciudad2):
    return ciudad1<ciudad2

def compareIds(id1, id2):

    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareDuration (duration1, duration2):

    if float(duration1) == float(duration2):
        return 0
    elif float(duration1) > float(duration2):
        return 1
    else:
        return -1

def compareCityState (ufo1,ufo2):
    citystate=ufo1["city"]+ufo1["country"]
    citystate2=ufo1["city"]+ufo2["country"]
    return citystate<citystate2

def compareDate (date1,date2):

    if float(date1) == float(date2):
        return 0
    elif float(date1) > float(date2):
        return 1
    else:
        return -1

def compareDatetime (date1,date2):

    return date1<date2
