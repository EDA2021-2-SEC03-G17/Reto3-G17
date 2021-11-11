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
import folium
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newCatalog():
    catalogo = {}
    catalogo["info"]= lt.newList('SINGLE_LINKED', compareDates)
    catalogo['Ciudad'] = mp.newMap(15225, maptype='PROBING', loadfactor=4.0)
    catalogo['Longitud'] = om.newMap('RBT',defaultfunction)
    catalogo['Hora'] = om.newMap('RBT', defaultfunction)
    return catalogo
# Construccion de modelos

# Funciones para agregar informacion al catalogo
def addUFO(catalog, ufo):
    addUFO2(catalog,ufo)
    addUFO3(catalog, ufo)
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
        
def addUFO2(catalog, ufo):
    ufoInfo2 = {'datetime':ufo['datetime'],'country':ufo['country'],'city':ufo['city'],'duration':ufo['duration (seconds)'],'shape':ufo['shape'],
    'latitude':ufo['latitude'],'longitude':ufo['longitude']}
    
    redondeado_longitud = round(float(ufo['longitude']),2)
    redondeado_latitud = round(float(ufo['latitude']),2)
    existe = om.get(catalog['Longitud'],redondeado_longitud)
    if existe is not None:
        arbol2 = rbn.getValue(existe)
        existe2 = om.get(arbol2, redondeado_latitud)
        if existe2 is not None:
            lista = rbn.getValue(existe2)
            lt.addLast(lista,ufoInfo2)
        else:
            nueva_lista = lt.newList('ARRAY_LIST')
            lt.addLast(nueva_lista,ufoInfo2)
            om.put(arbol2, redondeado_latitud, nueva_lista)
    else:
        nuevo_arbol = om.newMap('RBT',defaultfunction)
        nueva_list  = lt.newList('ARRAY_LIST')
        lt.addLast(nueva_list,ufoInfo2)
        om.put(nuevo_arbol,redondeado_latitud,nueva_list)
        om.put(catalog['Longitud'],redondeado_longitud,nuevo_arbol)

def addUFO3(catalog, ufo):
    ufoInfo = {'datetime':ufo['datetime'],'country':ufo['country'],'city':ufo['city'],'duration':ufo['duration (seconds)'],'shape':ufo['shape']}
    hora = ufo['datetime']
    hora = hora[11:]
    hora = hora.replace(':','')

    existe = om.get(catalog['Hora'],hora)
    if existe is not None:
        lista_valor = rbn.getValue(existe)
        lt.addLast(lista_valor,ufoInfo)
    else:
        lista_nueva = lt.newList('ARRAY_LIST')
        lt.addLast(lista_nueva,ufoInfo)
        om.put(catalog['Hora'], hora, lista_nueva)

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
    mapa_horas = catalog['Hora']
    inf_arreglado = lim_inf.replace(':','')
    sup_arreglado = lim_sup.replace(':','')
    valores = om.values(mapa_horas,inf_arreglado,sup_arreglado)
    mapa_fecha = om.newMap('RBT',defaultfunction)
    contador = 0
    for i in lt.iterator(valores):
        contador += int(lt.size(i))
        for j in lt.iterator(i):
            
            fecha = j['datetime']
            
            fecha = fecha.replace('-','').replace(':','').replace(' ','')
            existe = om.get(mapa_fecha,fecha)
            if existe is not None:
                lista = rbn.getValue(existe)
                lt.addLast(lista, j)
            else:
                nueva_lista = lt.newList('ARRAY_LIST')
                lt.addLast(nueva_lista,j)
                om.put(mapa_fecha,fecha,nueva_lista)
    respuesta = lt.newList('ARRAY_LIST')
    i = 0
    i2 = 0
    while i < 3:
        menor_llave = om.minKey(mapa_fecha)
        pareja = om.get(mapa_fecha, menor_llave)
        info = rbn.getValue(pareja)
        for index in lt.iterator(info):
            lt.addLast(respuesta,index)
        om.remove(mapa_fecha,menor_llave)
        i+=1        
    while i2 < 3:
        mayor_llave = om.maxKey(mapa_fecha)
        pareja = om.get(mapa_fecha, mayor_llave)
        info = rbn.getValue(pareja)
        for index in lt.iterator(info):
            lt.addLast(respuesta,index)
        om.remove(mapa_fecha,mayor_llave)
        i2+=1
    lt.exchange(respuesta, 4, 6)
    mas_tardios = mas_tardio(catalog)   
    return 'Hubo un total de: ' + str(contador) + ' avistamientos en ese rango de horas', respuesta, mas_tardios

def mas_tardio(catalog):
    mapa_copia = om.newMap('RBT', defaultfunction)
    lista_llaves = om.keySet(catalog['Hora'])
    respuesta = lt.newList('ARRAY_LIST')
    for i in lt.iterator(lista_llaves):
        pareja = om.get(catalog['Hora'],i)
        valor = rbn.getValue(pareja)
        om.put(mapa_copia,i,valor)
    i = 0
    while i <= 5:
        llave_grande = om.maxKey(mapa_copia)
        pareja = om.get(mapa_copia, llave_grande)
        valor = rbn.getValue(pareja)
        tamaño = lt.size(valor)
        info = {'fecha':llave_grande,'Cuenta':tamaño}
        lt.addLast(respuesta,info)
        i+=1
    return respuesta

# REQ 5 
def ufoporzona(catalog, longitud_inf, longitud_sup, latitud_inf, latitud_sup):
    decimal1=float(longitud_inf)
    decimal2=float(longitud_sup)
    decimal3 = float(latitud_inf)
    decimal4 = float(latitud_sup)
    avistamientos_filtrados= om.values(catalog['Longitud'],decimal1,decimal2)
    respuesta = lt.newList('ARRAY_LIST')
    for index in lt.iterator(avistamientos_filtrados):
        avistamientos_filtrados2 = om.values(index,decimal3, decimal4)
        for i in lt.iterator(avistamientos_filtrados2):
            for j in lt.iterator(i):
                lt.addLast(respuesta,j)
    avistamientos_totales = lt.size(respuesta)
    mapa_nuevo = om.newMap('RBT',defaultfunction)
    for i in lt.iterator(respuesta):
        fecha = i['datetime']
        fecha = fecha[0:10]
        fecha = fecha.replace('-','')
        om.put(mapa_nuevo,fecha,i)
    lista_respuesta = lt.newList('ARRAY_LIST')
    i = 0
    i2 = 0
    if int(om.size(mapa_nuevo)) > 10:
        while i < 5:
            menor_llave = om.minKey(mapa_nuevo)
            pareja = om.get(mapa_nuevo, menor_llave)
            info = rbn.getValue(pareja)
            lt.addLast(lista_respuesta,info)
            om.remove(mapa_nuevo,menor_llave)
            i+=1
        while i2 < 5:
            mayor_llave = om.maxKey(mapa_nuevo)
            pareja = om.get(mapa_nuevo, mayor_llave)
            info = rbn.getValue(pareja)
            lt.addLast(lista_respuesta,info)
            om.remove(mapa_nuevo,menor_llave)
            i2+=1
        lt.exchange(lista_respuesta,6,10)
        lt.exchange(lista_respuesta,7,9)
    else: 
        ward = False
        while ward != True:
            menor_llave = om.minKey(mapa_nuevo)
            pareja = om.get(mapa_nuevo, menor_llave)
            info = rbn.getValue(pareja)
            lt.addLast(lista_respuesta,info)
            om.remove(mapa_nuevo,menor_llave)
            if om.size(mapa_nuevo) == 0:
                ward = True        
    return 'Los avistamientos totales en esa zona fueron: ' + str(avistamientos_totales), lista_respuesta

# REQ 6
def mapazona(catalog, longitud_inf, longitud_sup, latitud_inf, latitud_sup):
    info = ufoporzona(catalog, longitud_inf, longitud_sup, latitud_inf, latitud_sup)
    mapa = folium.Map(location=[45.5236, -122.6750])
    print(mapa)
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

