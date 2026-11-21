def quicksort_inventario(
    inventario: list[dict],
    #criterio: Define si se ordena por "nombre" (alfabéticamente) o por "cantidad".   
    criterio: str = "nombre",
    #descendente: Si es True, invierte el resultado final (útil para ver cantidades de mayor a menor).   
    descendente: bool = False,
) -> list[dict]:
    #inventario: Lista de diccionarios con la forma {"item": "...", "cantidad": ...} usando QuickSort(cargada desde inventario.json).
    #Si la lista tiene 0 o 1 elemento, ya está ordenada; devuelve una copia (inventario[:]) para no mutar la lista original de golpe.
    if len(inventario) <= 1:
        return inventario[:]

    #Selección del pivote: pivote = inventario[len(inventario) // 2] toma el elemento central de la lista y obtiene su valor de comparación con _clave_orden.
    pivote = inventario[len(inventario) // 2]
    val_pivote = _clave_orden(pivote, criterio)

    #Partición en tres listas (menores, iguales, mayores): Recorre cada elemento del inventario y lo clasifica comparando val_elem contra val_pivote (partición de tres vías, muy práctica cuando hay cantidades repetidas).
    menores: list[dict] = []
    iguales: list[dict] = []
    mayores: list[dict] = []

    for elemento in inventario:
        val_elem = _clave_orden(elemento, criterio)
        if val_elem < val_pivote:
            menores.append(elemento)
        elif val_elem > val_pivote:
            mayores.append(elemento)
        else:
            iguales.append(elemento)

    #Llamadas recursivas y combinación: Ordena menores y mayores de forma ascendente y los une con ordenados_menores + iguales + ordenados_mayores.
    #Si descendente es True, usa .reverse() antes de devolver resultado.
    ordenados_menores = quicksort_inventario(menores, criterio, descendente=False)
    ordenados_mayores = quicksort_inventario(mayores, criterio, descendente=False)

    resultado = ordenados_menores + iguales + ordenados_mayores
    if descendente:
        resultado.reverse()
    return resultado

#Centraliza cómo se extrae el valor a comparar de cada diccionario del inventario.   
#Si criterio == "cantidad", convierte elemento["cantidad"] a int para ordenar numéricamente (y no como texto, donde "10" iría antes que "2").
#En cualquier otro caso (por defecto "nombre"), devuelve elemento["item"].lower() para ordenar alfabéticamente sin importar mayúsculas.
def _clave_orden(elemento: dict, criterio: str):
    if criterio == "cantidad":
        return int(elemento["cantidad"])
    return elemento["item"].lower()


def busqueda_binaria_inventario(inventario_ordenado_por_nombre: list[dict], nombre_item: str) -> int:
    """
    Busca un ítem por nombre en una lista previamente ordenada alfabéticamente por 'item'.
    Retorna el índice encontrado o -1 si no existe. Complejidad: O(log n).
    """
    objetivo = nombre_item.lower().strip()
    izquierda = 0
    derecha = len(inventario_ordenado_por_nombre) - 1

    while izquierda <= derecha:
        #Calcula el índice central medio = (izquierda + derecha) // 2 y lee el nombre en esa posición.
        medio = (izquierda + derecha) // 2
        actual = inventario_ordenado_por_nombre[medio]["item"].lower()
        #Si actual == objetivo, encontró el ítem y devuelve su índice medio.
        if actual == objetivo:
            return medio
        #Si actual < objetivo, el ítem buscado está después en el orden alfabético, así que mueve izquierda = medio + 1.
        elif actual < objetivo:
            izquierda = medio + 1
        #Si actual > objetivo, está antes, así que mueve derecha = medio - 1.
        else:
            derecha = medio - 1
    #Si el rango se agota (izquierda > derecha) y no se encontró, devuelve -1.x|
    return -1