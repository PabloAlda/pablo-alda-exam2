print("Este programa se encarga del analisis de trayectorias introducidas en un json.")
# Importamos las librerias json y math, las cuaes son necesarias para nuestro código.
import json
import math
import matplotlib.pyplot as plt
import numpy as np

# Abrimos la lista en json, como un file para así poder leerla y trabajar con ella.
with open ("datos.json","r") as file:
    datos_json = json.loads(file.read())

# Función que utilizamos para calcular la máxima distancia horizontal que alcanzan.
def calcular_distancia_horizontal(velocidad_inicial, angulo, gravedad=9.8):
    angulo_radianes = math.radians(angulo)
    distancia_horizontal = (velocidad_inicial**2 * math.sin(2 * angulo_radianes)) / gravedad
    return distancia_horizontal


# Calcular y mostrar la distancia máxima para cada conjunto de datos.
for datos in datos_json:
    velocidad_inicial = datos["InitialVelocity"]
    angulo = datos["LaunchAngle"]
    
    distancia_maxima = calcular_distancia_horizontal(velocidad_inicial, angulo)
    print(f"Para una velocidad inicial de {velocidad_inicial} m/s y un ángulo de lanzamiento de {angulo} grados, la distancia horizontal máxima es: {distancia_maxima} metros.")

# Función que utilizamos para calcular la altura máxima que alcanzan.
def calcular_altura_maxima(velocidad_inicial, angulo, gravedad=9.8):
    angulo_radianes = math.radians(angulo)
    altura_maxima = (velocidad_inicial**2 * math.sin(angulo_radianes)**2) / (2 * gravedad)
    return altura_maxima


# Inicializar variables para el máximo.
maxima_altura = 0.0
parametros_maxima_altura = None

# Calcular y mostrar la altura máxima para cada conjunto de datos.
for datos in datos_json:
    velocidad_inicial = datos["InitialVelocity"]
    angulo = datos["LaunchAngle"]
    
    altura_maxima = calcular_altura_maxima(velocidad_inicial, angulo)
    
    print(f"Para una velocidad inicial de {velocidad_inicial} m/s y un ángulo de lanzamiento de {angulo} grados, la altura máxima es: {altura_maxima} metros.")

    # Actualizar si encontramos una nueva altura máxima.
    if altura_maxima > maxima_altura:
        maxima_altura = altura_maxima
        parametros_maxima_altura = {"InitialVelocity": velocidad_inicial, "LaunchAngle": angulo}

# Mostrar los parámetros del lanzamiento con la máxima altura.
print("\nEl lanzamiento que alcanza la máxima altura tiene los siguientes parámetros:")
print(f"Velocidad inicial: {parametros_maxima_altura['InitialVelocity']} m/s")
print(f"Ángulo de lanzamiento: {parametros_maxima_altura['LaunchAngle']} grados")
print(f"Altura máxima: {maxima_altura} metros")

# Función la cual utilizamos para calcular el tiempo de vuelo de cada proyectil.
def calcular_tiempo_vuelo(velocidad_inicial, angulo, gravedad=9.8):
    angulo_radianes = math.radians(angulo)
    tiempo_vuelo = (2 * velocidad_inicial * math.sin(angulo_radianes)) / gravedad
    return tiempo_vuelo



# Mostrar los lanzamientos que superan un tiempo de vuelo de 3 segundos.
print("Lanzamientos que superan un tiempo de vuelo de 3 segundos:")

for datos in datos_json:
    velocidad_inicial = datos["InitialVelocity"]
    angulo = datos["LaunchAngle"]
    
    tiempo_vuelo = calcular_tiempo_vuelo(velocidad_inicial, angulo)
    
    if tiempo_vuelo > 3.0:
        print(f"Para una velocidad inicial de {velocidad_inicial} m/s y un ángulo de lanzamiento de {angulo} grados, el tiempo de vuelo es: {tiempo_vuelo} segundos.")

#Función que calcula la posicion del proyectil.
def calcular_posicion_proyectil(velocidad_inicial, angulo, tiempo, gravedad=9.8):
    angulo_radianes = math.radians(angulo)
    altura = (velocidad_inicial * math.sin(angulo_radianes) * tiempo) - (0.5 * gravedad * tiempo**2)
    distancia_horizontal = velocidad_inicial * math.cos(angulo_radianes) * tiempo
    return {"tiempo": tiempo, "altura": altura, "distancia_horizontal": distancia_horizontal}




# Crear una lista para almacenar los resultados
resultados_proyectiles = []

# Calcular y almacenar la posición del proyectil en intervalos de tiempo hasta tocar el suelo
for datos in datos_json:
    velocidad_inicial = datos["InitialVelocity"]
    angulo = datos["LaunchAngle"]
    
    tiempo_vuelo = calcular_tiempo_vuelo(velocidad_inicial, angulo)
    
    # Intervalo de tiempo entre las posiciones
    intervalo_tiempo = tiempo_vuelo / 10

    resultados_proyectil = []
    for i in range(11):
        tiempo_actual = i * intervalo_tiempo

        if tiempo_actual <= tiempo_vuelo:
            posicion_actual = calcular_posicion_proyectil(velocidad_inicial, angulo, tiempo_actual)
            resultados_proyectil.append(posicion_actual)

    resultados_proyectiles.append({"InitialVelocity": velocidad_inicial, "LaunchAngle": angulo, "resultados": resultados_proyectil})

# Guardar los resultados en un archivo JSON
with open('resultados_proyectiles.json', 'w') as archivo_json:
    json.dump(resultados_proyectiles, archivo_json, indent=2)

# Mostrar los resultados por pantalla
print("Datos guardados en 'resultados_proyectiles.json'.\n")
print("Resultados:")
for resultado in resultados_proyectiles:
    print(f"\nPara una velocidad inicial de {resultado['InitialVelocity']} m/s y un ángulo de lanzamiento de {resultado['LaunchAngle']} grados:")
    for posicion in resultado['resultados']:
        print(f"Tiempo: {posicion['tiempo']:.2f} segundos - Altura: {posicion['altura']:.2f} metros - Distancia Horizontal: {posicion['distancia_horizontal']:.2f} metros")


print("Vamos a ver que pasa si sumamos de 10 en 10 grados.")
# Calcular y mostrar solo la distancia final y el tiempo que tarda en alcanzarla
for datos in datos_json:
    velocidad_inicial = datos["InitialVelocity"]
    angulo_base = datos["LaunchAngle"]
    
    for i in range(10):
        angulo = angulo_base + i * 10
        # Limitar el ángulo a 90 grados
        angulo = min(angulo, 90)
        
        tiempo_vuelo = calcular_tiempo_vuelo(velocidad_inicial, angulo)
        distancia_final = calcular_posicion_proyectil(velocidad_inicial, angulo, tiempo_vuelo)["distancia_horizontal"]

        print(f"\nPara una velocidad inicial de {velocidad_inicial} m/s y un ángulo de lanzamiento de {angulo} grados:")
        print(f"Tiempo de vuelo: {tiempo_vuelo:.2f} segundos")
        print(f"Distancia final: {distancia_final:.2f} metros")

print("Ahora vamos a ver las diferentes trayectorias.")
# Visualizar las trayectorias
for datos in datos_json:
    velocidad_inicial = datos["InitialVelocity"]
    angulo_base = datos["LaunchAngle"]
    
    for i in range(10):
        angulo = angulo_base + i * 10
        # Limitar el ángulo a 90 grados
        angulo = min(angulo, 90)
        
        tiempo_vuelo = calcular_tiempo_vuelo(velocidad_inicial, angulo)

        # Calcular la trayectoria
        t = np.linspace(0, tiempo_vuelo, num=1000)
        trayectoria_x = velocidad_inicial * np.cos(math.radians(angulo)) * t
        trayectoria_y = velocidad_inicial * np.sin(math.radians(angulo)) * t - 0.5 * 9.8 * t**2

        # Visualizar la trayectoria
        plt.plot(trayectoria_x, trayectoria_y, label=f"{angulo}°")

    plt.title(f"Trayectorias para velocidad inicial de {velocidad_inicial} m/s")
    plt.xlabel("Distancia Horizontal (metros)")
    plt.ylabel("Altura (metros)")
    plt.legend()
    plt.show()
