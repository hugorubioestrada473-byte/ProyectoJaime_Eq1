class NodoBST:
    """Nodo del Árbol Binario de Búsqueda con la ficha técnica del ítem."""
    #__init__: Crea un nodo que representa un ítem del catálogo global (catalogo.json).
    def __init__(self, nombre: str, categoria: str, max_stack: int):
        #self.nombre = nombre.lower(): Guarda el nombre en minúsculas para que la ordenación alfabética y las búsquedas no fallen por mayúsculas o minúsculas.
        self.nombre = nombre.lower()
        #self.categoria y self.max_stack: Guardan los atributos de la ficha técnica del ítem (bloque, herramienta, material y el tamaño máximo de pila 64, 16 o 1).
        self.categoria = categoria
        self.max_stack = int(max_stack)
        #self.izquierda y self.derecha: Punteros a los hijos del nodo en el árbol. Inician en None porque al crear un nodo nuevo todavía no tiene hijos.
        self.izquierda: "NodoBST | None" = None
        self.derecha: "NodoBST | None" = None


class ArbolCatalogoBST:
    """BST ordenado alfabéticamente por nombre del ítem."""

    def __init__(self):
        #self.raiz: Guarda el nodo raíz del árbol. Comienza en None cuando el árbol está vacío.
        self.raiz: NodoBST | None = None

    def insertar(self, nombre: str, categoria: str, max_stack: int) -> None:
        nuevo = NodoBST(nombre, categoria, max_stack)
        #Árbol vacío (if self.raiz is None:): Si aún no hay raíz, el nuevo nodo pasa a ser self.raiz y termina (return).
        if self.raiz is None:
            self.raiz = nuevo
            return

        actual = self.raiz
        while True:
            #if nuevo.nombre < actual.nombre:: Compara alfabéticamente. Si el nuevo nombre va antes que el del nodo actual, baja a la izquierda; si actual.izquierda está libre (None), ahí lo inserta.
            if nuevo.nombre < actual.nombre:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    return
                actual = actual.izquierda
                #elif nuevo.nombre > actual.nombre:: Si el nuevo nombre va después alfabéticamente, baja a la derecha; si actual.derecha está libre (None), ahí lo inserta.
            elif nuevo.nombre > actual.nombre:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    return
                actual = actual.derecha
                #else:: Si los nombres son iguales, ya existe ese ítem en el árbol, así que actualiza categoria y max_stack en lugar de duplicarlo.
            else:
                actual.categoria = nuevo.categoria
                actual.max_stack = nuevo.max_stack
                return

    def buscar(self, nombre: str) -> NodoBST | None:
        """Busca un ítem por nombre en O(log n) promedio."""
        #objetivo = nombre.lower().strip():Limpia espacios accidentales y pasa a minúsculas.
        objetivo = nombre.lower().strip()
        actual = self.raiz
        while actual is not None:
            #Si objetivo == actual.nombre, encontró el ítem y devuelve el NodoBST completo (con su categoría y max_stack).   
            if objetivo == actual.nombre:
                return actual
            #Si objetivo < actual.nombre, descarta todo el subárbol derecho y sigue por actual.izquierda.   
            elif objetivo < actual.nombre:
                actual = actual.izquierda
                #Si objetivo > actual.nombre, descarta todo el subárbol izquierdo y sigue por actual.derecha.   
            else:
                #Si llega a None sin coincidir, el ítem no está en el árbol y devuelve
                actual = actual.derecha
        return None

    def recorrido_in_order(self) -> list[NodoBST]:
        #resultado: Lista donde se irán agregando los nodos en el orden en que son visitados.
        resultado: list[NodoBST] = []

        #Orden In-Order (Izquierda -> Raíz -> Derecha):
        # Primero explora todo el subárbol izquierdo (nombres alfabéticamente menores).
        # Luego agrega el nodo actual a resultado.
        # Después explora todo el subárbol derecho (nombres alfabéticamente mayores)
        def _in_order(nodo: NodoBST | None) -> None:
            if nodo is None:
                return
            _in_order(nodo.izquierda)
            resultado.append(nodo)
            _in_order(nodo.derecha)

        _in_order(self.raiz)
        return resultado