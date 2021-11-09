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
 """

import config as cf
import model
import csv
import time
from DISClib.DataStructures import rbt 


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    t2=loadUFO(catalog)
    print("("+str(t2)+")")


def loadUFO(catalog):

    start_time = time.process_time() 
    ufosfile = cf.data_dir + "UFOS-utf8-small.csv"
    #C:\Users\Admin\Documents\Universidad\4TO SEMESTRE\EDA\MODULO 3\Reto3-G17\
    input_file = csv.DictReader(open(ufosfile, encoding='utf-8'))
    for ufo in input_file:
        model.addUFO(catalog, ufo)
    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000  
    return elapsed_time_mseg     

#REQ 1
def ufoporciudad(catalog,city):
    return model.ufoporciudad(catalog["Avistamientos"],city)

#REQ 2
def sightingsdurationrange(catalog,lim_inferior,lim_superior):
    return model.sightingsdurationrange(catalog['Duracion'],lim_inferior,lim_superior)

def max_duration(catalog):
    return model.max_duration(catalog["Duracion"])

#REQ 4
def min_date(catalog):
    return model.min_date(catalog["Fechas"])

def sightingsperdate(catalog,lim_inferior,lim_superior):
    return model.sightingsperdate(catalog['Fechas'],lim_inferior,lim_superior)


#CONSULTA
def listsize(listaufo):
    return model.listsize(listaufo)

# Funciones de consulta sobre el catálogo


def sightingsperhourminute(lim_inferior,lim_superior):
    return model.sightingsperhourminute(lim_inferior,lim_superior)


def countsightingsbyzone(lim_inferior,lim_superior):
    return model.countsightingsbyzone(lim_inferior,lim_superior)

def countsightingsbyzone(lim_inferior,lim_superior):
    return model.seesightingsbyzone(lim_inferior,lim_superior)
