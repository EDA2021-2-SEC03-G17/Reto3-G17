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


# Construccion de modelos
def newCatalog():
    catalogo = {}
    catalogo["info"]= lt.newList('SINGLE_LINKED', compareDates)
    catalogo['Ciudad'] = mp.newMap(15225, maptype='PROBING', loadfactor=4.0)
    catalogo['Longitud'] = om.newMap('RBT',defaultfunction)
    catalogo['Hora'] = om.newMap('RBT', defaultfunction)
    catalogo['Duracion'] = om.newMap(omaptype="RBT", comparefunction=compareDuration)
    catalogo['Fechas'] = om.newMap(omaptype="RBT", comparefunction=compareDate)

    return catalogo

# Funciones para agregar informacion al catalogo
def addUFO(catalog, ufo):
    addUFO2(catalog,ufo)
    addUFO3(catalog, ufo)
    lt.addLast(catalog["info"], ufo)
    ufobyduration(catalog,ufo)
    ufobydate(catalog,ufo)

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

def ufobyduration(catalog,ufo):
    
    ufoInfo = {'datetime':ufo['datetime'],'city': ufo['city'], 'duration (sec)': ufo['duration (seconds)'],'shape':ufo['shape'],
    'state':ufo['state'],'country':ufo['country']} 

    duration=float(ufo['duration (seconds)'])

    inCatalog=om.get(catalog['Duracion'], duration)

    if inCatalog is not None:
        llave=me.getValue(inCatalog)
        lt.addLast(llave,ufoInfo)
        sa.sort(llave, compareCountryCity)
        
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
           
    else:
        info=lt.newList("ARRAY_LIST",cmpfunction=compareCountryCity, key=None)
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

#Requerimiento 1
def citysightings(ciudad):
    return None


#Requerimiento 2
def total_sightings(catalog):
    total=om.size(catalog)
    return total

def max_duration(catalog):
    avistamiento_mayor_duracion=om.maxKey(catalog)
    return avistamiento_mayor_duracion

def sightingsdurationrange(catalog,lim_inferior, lim_superior):

    duracion_rango=om.values(catalog,lim_inferior, lim_superior)
    size = 0
    for element in lt.iterator(duracion_rango):
        size+=lt.size(element)
    #print(duracion_rango)
    muestra = first_last_three (duracion_rango)
    return muestra, size

#Requerimiento 3
def sightingsperhourminute(lim_inferior,lim_superior):
    return None

#Requerimiento 4
def min_date(catalog):
    avistamiento_menor_fecha=str(om.minKey(catalog))
    avistamiento_menor_fecha=avistamiento_menor_fecha[0:4]+"-"+avistamiento_menor_fecha[4:6]+"-"+avistamiento_menor_fecha[6:8]
    return avistamiento_menor_fecha

def sightingsperdate(catalog,lim_inferior,lim_superior):

    fechas_rango=om.values(catalog,lim_inferior, lim_superior)
    size=lt.size(fechas_rango)
    if size==0:
        muestra = "empty"
    else:
        muestra = first_last_three (fechas_rango) 
    return muestra, size

def first_last_three (rango):

    tamanio_muestra=3
    firstUFOS=lt.newList("ARRAY_LIST")
    lastUFOS=lt.newList("ARRAY_LIST")

    while tamanio_muestra!=0:
        UFOS=lt.removeFirst(rango)
        tam= lt.size(UFOS)
        if tam>=3:
            primerUFOS=lt.subList(UFOS,1,tamanio_muestra)
            for UFOSlist in lt.iterator(primerUFOS):
                lt.addLast( firstUFOS,UFOSlist)
            tamanio_muestra=0
        else:
            primerUFOS=lt.subList(UFOS,1,tam)
            for UFOSlist in lt.iterator(primerUFOS):
                lt.addLast( firstUFOS,UFOSlist)
            tamanio_muestra-=tam

    tamanio_muestra=3
    while tamanio_muestra!=0:
        ultimoUFOS=lt.removeLast(rango)
        ultimoUFOS=sa.sort(ultimoUFOS,compareCountryCity2)
        tam= lt.size(ultimoUFOS)
        if tam>=3:
            ultimoUFOS=lt.subList(ultimoUFOS,1,tamanio_muestra)
            for UFOSlist in lt.iterator(ultimoUFOS):
                lt.addFirst( lastUFOS,UFOSlist)
            tamanio_muestra=0

        else:
            ultimoUFOS=lt.subList(ultimoUFOS,1,tam)
            for UFOSlist in lt.iterator(ultimoUFOS):
                lt.addFirst( lastUFOS,UFOSlist)
            tamanio_muestra-=tam

    return  firstUFOS, lastUFOS

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

def compareCountryCity (ufo1,ufo2):
    if ufo1["country"]=="":
        ufo1["country"]="zz"   
    if ufo2["country"]=="":
        ufo2["country"]="zz"  
    citystate = ufo1["city"]
    citystate2 = ufo2["city"]
    return citystate < citystate2

def compareCountryCity2 (ufo1,ufo2):
    if ufo1["country"]=="":
        ufo1["country"]="zz"   
    if ufo2["country"]=="":
        ufo2["country"]="zz"  
    citystate = ufo1["city"]
    citystate2 = ufo2["city"]
    return citystate > citystate2

def compareDate (date1,date2):

    if float(date1) == float(date2):
        return 0
    elif float(date1) > float(date2):
        return 1
    else:
        return -1

def compareDatetime (date1,date2):

    return date1<date2
