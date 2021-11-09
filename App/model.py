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


from DISClib.DataStructures.arraylist import defaultfunction
import config as cf
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import rbtnode as rbn
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newCatalog():
    catalogo = {}
    catalogo["info"]= lt.newList('SINGLE_LINKED', compareDates)
    catalogo['Ciudad'] = mp.newMap(15225, maptype='PROBING', loadfactor=4.0)
    return catalogo
# Construccion de modelos

# Funciones para agregar informacion al catalogo
def addUFO(catalog, ufo):

    lt.addLast(catalog["info"], ufo)

    ufoInfo = {'datetime':ufo['datetime'],'duration':ufo['duration (seconds)'], 'shape':ufo['shape']} 

    c=ufo['city']
    if ufo["city"]=="":
        c="city"
    date1=ufo["datetime"]
    date1=date1[0:10]
    date1=int(date1.replace('-',''))

    b=mp.get(catalog['Ciudad'], c)

    if b is not None:
        a=me.getValue(b)
        om.put(a, date1, ufoInfo)
           
    else:

        tree=om.newMap(omaptype='RBT', comparefunction=defaultfunction)
        om.put(tree, date1, ufoInfo)
        mp.put(catalog['Ciudad'],c,tree)
        
# req 1   

def ufoporciudad(catalog,city):
    mapa = catalog['Ciudad']
    avistamientos = mp.size(mapa)
    arbol_avistamientos_ciudad = me.getValue(mp.get(mapa,city))
    total_avistamientos_ciudad = om.size(arbol_avistamientos_ciudad)
    mapa_copia = om.newMap('RBT',compareDates)
    lista_llaves = om.keySet(arbol_avistamientos_ciudad)
    for i in lt.iterator(lista_llaves):
        pareja = om.get(arbol_avistamientos_ciudad,i)
        value = rbn.getValue(pareja)
        om.put(mapa_copia,i,value)
    i = 0
    i2 = 0
    list = lt.newList('ARRAY_LIST')
    while i < 3:
        menor_llave = om.minKey(mapa_copia)
        pareja = om.get(mapa_copia, menor_llave)
        info = rbn.getValue(pareja)
        lt.addLast(list,info)
        om.remove(mapa_copia,menor_llave)
        i+=1
    while i2 < 3:
        mayor_llave = om.maxKey(mapa_copia)
        pareja = om.get(mapa_copia, mayor_llave)
        info = rbn.getValue(pareja)
        lt.addLast(list,info)
        om.remove(mapa_copia,mayor_llave)
        i2+=1
    lt.exchange(list, 4, 6)
    return 'El total de avistamientos es ' + str(avistamientos) + ' y el total de avistamientos en ' + str(city) + ' es ' + str(total_avistamientos_ciudad), list

# REQ 3
def ufoporhoraminuto(catalog, lim_inf, lim_sup):
    ufos_list = catalog['info']
    lim_inf_fixed = int(lim_inf.replace(':',''))
    lim_sup_fixed = int(lim_sup.replace(':',''))
    answer = lt.newList('ARRAY_LIST')
    for ufo in lt.iterator(ufos_list):
        time = ufo['datetime']
        timefixed = int(time[11:].replace(':',''))
        if timefixed >= lim_inf_fixed and timefixed <= lim_sup_fixed:
            dict_temporal = {'datetime':ufo['datetime'], 'city':ufo['city'], 'state':ufo['state'], 
            'country':ufo['country'], 'shape':ufo['shape'], 'duration':ufo['duration (seconds)']}
            lt.addLast(answer,dict_temporal)
    x=lt.size(answer)
    print(x)
# Funciones para creacion de datos

# Funciones de consulta
def listsize(listaufo):
    return lt.size(listaufo)

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

