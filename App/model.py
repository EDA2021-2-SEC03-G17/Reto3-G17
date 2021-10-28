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


import config as cf
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import rbt 
from DISClib.DataStructures import rbtnode as rbn
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newCatalog():
    catalogo = {}
    catalogo['Avistamientos'] = rbt.newMap(ordenamientoAlfabetico)
    return catalogo
# Construccion de modelos

# Funciones para agregar informacion al catalogo
def addUFO(catalog, ufo):
    ufoInfo = {'datetime':ufo['datetime'],'duration':ufo['duration (seconds)'], 'shape':ufo['shape']} 

    b=rbt.contains(catalog['Avistamientos'], ufo)

    if b:

        a=rbt.get(catalog['Avistamientos'],ufo)
        a=rbn.getValue(a)
        lt.addLast(a,ufoInfo)
        
    else:
        lista=lt.newList("ARRAY_LIST",cmpfunction=BYDATE)
        lt.addLast(lista,ufoInfo)
        rbt.put(catalog['Avistamientos'],ufo['country'],lista)

# req 1   

def ufoporciudad(catalog,city):
    if rbt.contains(catalog,city):
        ufos=rbt.get(catalog,city)
        ufos=rbn.getValue(ufos)
    return ufos

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
    
    primera_letra1 = None
    primera_letra2 = None
    if ciudad1 != '':
        primera_letra1 = ord(ciudad1[0])
    else:
        primera_letra1 = ord('z')
    
    if ciudad2 != '':
        primera_letra2 = ord(ciudad2[0])
    else:
        primera_letra2 = ord('z')
    return primera_letra1 > primera_letra2
