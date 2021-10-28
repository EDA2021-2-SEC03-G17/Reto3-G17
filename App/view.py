"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
assert cf
import sys
import controller
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.DataStructures import rbt 



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#MENU

def printMenu():
    print("___________________________________________")
    print("    BIENVENIDO AL CATALOGO DE UFO's")
    print("___________________________________________")
    print("")
    print("1 ) Cargar información en el catálogo")
    print("2 ) Contar los avistamientos en una ciudad")
    print("3 ) Contar los avistamientos por duración")
    print("4 ) Contar avistamientos por Hora/Minutos del día")
    print("5 ) Contar los avistamientos en un rango de fechas")
    print("6 ) Contar los avistamientos de una zona geográfica")
    print("7 ) Visualizar los avistamientos de una zona geográfica")
    print("0 ) Salir")
    print("___________________________________________")

#CARGA DE DATOS [1]
def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)


catalog = None

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = initCatalog()
        print("Cargando información de los archivos ....")
        loadData(catalog)
        print (catalog)
    
    elif int(inputs[0]) == 2:
        ciudad = input('Ingrese la ciudad a consultar\n')
        resultado = controller.citysightings(ciudad)
        print(resultado)
    
    elif int(inputs[0]) == 3:
        lim_inferior = input('Ingrese el límite inferior de segundos\n')
        lim_superior = input('Ingrese el límite superior de segundos\n')
        resultado = controller.sightingsduration(lim_inferior,lim_superior)
        print(resultado)

    elif int(inputs[0]) == 4:
        lim_inferior = input('Ingrese el límite inferior en formato HH:MM\n')
        lim_superior = input('Ingrese el límite superior en formato HH:MM\n')
        resultado = controller.sightingsduration(lim_inferior,lim_superior)
        print(resultado)


    elif int(inputs[0]) == 5:
        lim_inferior = input('Ingrese el límite inferior en formato AAAA-MM-DD\n')
        lim_superior = input('Ingrese el límite superior en formato AAAA-MM-DD\n')
        resultado = controller.sightingsdaterange(lim_inferior,lim_superior)
        print(resultado)
        
    elif int(inputs[0]) == 6:
        longitud_min_max = input('Ingrese el límite mínimo y máximo de longitud\n')
        latitud_min_max = input('Ingrese el límite mínimo y máximo de latitud\n')
        resultado = controller.countsightingsbyzone(lim_inferior,lim_superior)
        print(resultado)

    elif int(inputs[0]) == 7:
        longitud_min_max = input('Ingrese el límite mínimo y máximo de longitud\n')
        latitud_min_max = input('Ingrese el límite mínimo y máximo de latitud\n')
        resultado = controller.seesightingsbyzone(lim_inferior,lim_superior)
        print(resultado)
        
        pass
    else:
        sys.exit(0)
sys.exit(0)
