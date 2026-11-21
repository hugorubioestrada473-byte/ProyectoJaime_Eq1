#class GrafoCrafteo: Agrupa los datos y comportamientos del grafo de recetas en un solo objeto. 
class GrafoCrafteo:
    """Representa las recetas de crafteo como un Grafo Dirigido Acíclico (DAG)."""
    #Normalización en __init__:item.lower() e ing.lower() convierten los nombres a minúsculas para evitar errores si alguien escribe 
    #"Diamante" o "DIAMANTE" en el JSON o en la consola.int(cant) asegura que las cantidades se guarden como números enteros y no como texto o flotantes por accidente.
    def __init__(self, recetas: dict | None = None):
        #self.adyacencia: Es una lista de adyacencia implementada con un diccionario de Python. 
        #Cada clave (str) es el nombre de un ítem y su valor es una lista de tuplas (ingrediente, cantidad)
        #que representan las dependencias (aristas salientes). Si un ítem es material base, su lista queda vacía []. 
        self.adyacencia: dict[str, list[tuple[str, int]]] = {}
        if recetas:
            for item, ingredientes in recetas.items():
                self.adyacencia[item.lower()] = [
                    (ing.lower(), int(cant)) for ing, cant in ingredientes
                ]

    #existe_item(item): Comprueba si item (en minúsculas) está registrado como clave en self.adyacencia. Devuelve True o False.
    def existe_item(self, item: str) -> bool:
        return item.lower() in self.adyacencia
    
    #obtener_ingredientes_directos(item): Devuelve la lista de tuplas (ingrediente, cantidad) 
    #que pide ese ítem en un solo paso (sin bajar a sub-recetas). Usa .get(..., []) para devolver una lista vacía si no encuentra el ítem.
    def obtener_ingredientes_directos(self, item: str) -> list[tuple[str, int]]:
        return self.adyacencia.get(item.lower(), [])

    #Validaciones iniciales:
    def calcular_materiales_base(self, item_objetivo: str, cantidad: int = 1) -> dict[str, int]:
        """
        Recorre el DAG mediante DFS para acumular materiales crudos (hojas)
        y detecta ciclos si el JSON tuviera alguna dependencia circular.
        """
        item_objetivo = item_objetivo.lower()

        #Si item_objetivo no existe en self.adyacencia, lanza KeyError.
        if item_objetivo not in self.adyacencia:
            raise KeyError(f"El ítem '{item_objetivo}' no existe en las recetas.")
        
        #Si cantidad <= 0, lanza ValueError porque no tiene sentido calcular materiales base para 0 o cantidades negativas.
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0.")

        #acumulado_base: Diccionario donde se van sumando únicamente los materiales base (nodos hoja) y su total acumulado.
        acumulado_base: dict[str, int] = {}

        #visitando: Un set (conjunto) que guarda los nodos que están actualmente activos en la pila de llamadas (la rama en curso del DFS).
        visitando: set[str] = set()  # Nodos en la pila de recursión actual (detecta ciclos)

        #Detección de ciclos: if nodo in visitando: revisa si llegamos a un nodo que ya estamos explorando hacia abajo. 
        #Si es así, hay un ciclo (por ejemplo A -> B -> A) y lanza ValueError para evitar recursión infinita.
        def dfs(nodo: str, cant_actual: int) -> None:
            if nodo in visitando:
                raise ValueError(f"Ciclo detectado en las recetas involucrando a '{nodo}'.")

            #Caso base (nodo hoja): dependencias = self.adyacencia.get(nodo, []). 
            #Si len(dependencias) == 0, significa que nodo no depende de nada más (es un material crudo). 
            #Entonces suma cant_actual a acumulado_base[nodo] y hace return.   
            dependencias = self.adyacencia.get(nodo, [])
            if len(dependencias) == 0:
                acumulado_base[nodo] = acumulado_base.get(nodo, 0) + cant_actual
                return

            #visitando.add(nodo) marca el nodo como en proceso.
            visitando.add(nodo)

            #En el for ingrediente, cant_req in dependencias:, llama recursivamente a dfs(ingrediente, cant_actual * cant_req). 
            #Multiplicar cant_actual * cant_req propaga la cantidad necesaria a través de toda la cadena de crafteo 
            #(por ejemplo, si necesitas 2 libro y cada libro pide 3 papel, al bajar a papel se pasan 2 * 3 = 6).   
            for ingrediente, cant_req in dependencias:
                dfs(ingrediente, cant_actual * cant_req)

            #visitando.remove(nodo) quita el nodo de visitando al terminar de explorar esa rama. 
            #Esto es clave porque un mismo material base (como carbon o palo) sí puede aparecer en distintas ramas del grafo sin ser un ciclo.
            visitando.remove(nodo)

        dfs(item_objetivo, cantidad)
        return acumulado_base

    def imprimir_jerarquia(self, item: str, cantidad: int = 1, nivel: int = 0) -> None:
        """Muestra paso a paso la jerarquía de fabricación usando DFS."""
        item = item.lower()
        #indentacion = "  " * nivel: Agrega dos espacios por cada nivel de profundidad en el árbol de crafteo para que se note visualmente qué depende de qué.
        indentacion = "  " * nivel
        dependencias = self.adyacencia.get(item, [])

        #Caso hoja (if not dependencias:): Imprime el ítem con (material base) y detiene la recursión en esa rama.   
        if not dependencias:
            print(f"{indentacion}- {item} x{cantidad} (material base)")
            return

        #Caso compuesto: Imprime el ítem y su cantidad actual, y luego llama a self.imprimir_jerarquia 
        #para cada ingrediente con cantidad * cant_req y nivel + 1.   
        print(f"{indentacion}- {item} x{cantidad}")
        for ingrediente, cant_req in dependencias:
            self.imprimir_jerarquia(ingrediente, cantidad * cant_req, nivel + 1)