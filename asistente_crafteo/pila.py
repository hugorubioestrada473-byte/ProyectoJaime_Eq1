#class PilaHistorial: Implementa una pila propia sin depender de librerías externas, tal como pide la ficha técnica.
class PilaHistorial:

    #Disciplina LIFO (Last In, First Out): El último crafteo que agregas es el primero que se saca al elegir Deshacer último crafteo (Ctrl+Z).   s
    #elf._elementos: list[dict] = []: Lista interna donde se almacenan los registros (diccionarios) de cada transacción de crafteo. 
    #El guion bajo _ indica por convención que es un atributo interno de la clase y que debe manipularse mediante sus métodos (push, pop, peek).
    def __init__(self):
        self._elementos: list[dict] = []

    #Agrega transaccion al final de self._elementos, que funciona como el tope de la pila.   
    #En el proyecto, cada transaccion guarda qué ítem se creó, cuántas unidades y qué ingredientes exactos se descontaron del inventario para poder revertirlos después.   
    def push(self, transaccion: dict) -> None:
        """Apila una transacción de crafteo en el tope."""
        self._elementos.append(transaccion)

    #Primero revisa if self.esta_vacia(): para evitar un error IndexError si intentan deshacer cuando no hay crafteos registrados.
    #Si hay elementos, self._elementos.pop() extrae y devuelve el último diccionario apilado (el crafteo más reciente). 
    #Con esos datos el programa puede restar el ítem fabricado y devolver los ingredientes al inventario.   
    def pop(self) -> dict | None:
        """Desapila y devuelve la última transacción (o None si está vacía)."""
        if self.esta_vacia():
            return None
        return self._elementos.pop()

    #peek(): Mira cuál es la transacción en el tope (self._elementos[-1]) sin sacarla de la pila. Si está vacía, devuelve None.   
    def peek(self) -> dict | None:
        """Consulta la última transacción sin eliminarla."""
        if self.esta_vacia():
            return None
        return self._elementos[-1]

    #esta_vacia(): Devuelve True si no hay elementos en _elementos y False si hay al menos uno.
    def esta_vacia(self) -> bool:
        return len(self._elementos) == 0

    #__len__(): Permite consultar cuántos crafteos hay en el historial usando len(historial) en Python.
    def __len__(self) -> int:
        return len(self._elementos)