import json
from pathlib import Path

from bst import ArbolCatalogoBST
from grafo import GrafoCrafteo
from ordenamiento import busqueda_binaria_inventario, quicksort_inventario
from pila import PilaHistorial

BASE_DIR = Path(__file__).resolve().parent
RUTA_RECETAS = BASE_DIR / "recetas.json"
RUTA_CATALOGO = BASE_DIR / "catalogo.json"
RUTA_INVENTARIO = BASE_DIR / "inventario.json"


def cargar_json(ruta: Path):
    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(ruta: Path, datos) -> None:
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)


def construir_bst_desde_catalogo(catalogo_data: list[dict]) -> ArbolCatalogoBST:
    bst = ArbolCatalogoBST()
    for entrada in catalogo_data:
        bst.insertar(
            nombre=entrada["nombre"],
            categoria=entrada["categoria"],
            max_stack=entrada["max_stack"],
        )
    return bst


def sumar_al_inventario(inventario: list[dict], item: str, cantidad: int) -> None:
    """Suma 'cantidad' de 'item' al inventario (crea la entrada si no existe y cantidad > 0)."""
    item = item.lower().strip()
    if cantidad <= 0:
        return

    ordenado = quicksort_inventario(inventario, criterio="nombre")
    idx = busqueda_binaria_inventario(ordenado, item)

    if idx != -1:
        nombre_real = ordenado[idx]["item"]
        for entry in inventario:
            if entry["item"].lower() == nombre_real.lower():
                entry["cantidad"] = int(entry["cantidad"]) + cantidad
                return
    else:
        inventario.append({"item": item, "cantidad": cantidad})


def restar_del_inventario(inventario: list[dict], item: str, cantidad: int) -> None:
    """Resta 'cantidad' de 'item' del inventario."""
    item = item.lower().strip()
    if cantidad <= 0:
        return

    for entry in inventario:
        if entry["item"].lower() == item:
            entry["cantidad"] = max(0, int(entry["cantidad"]) - cantidad)
            return


def opcion_consultar_item(bst: ArbolCatalogoBST) -> None:
    print("\n--- 1. Consultar Ítem (BST) ---")
    print("a) Buscar ítem por nombre")
    print("b) Listar todo el catálogo en orden alfabético (In-Order)")
    sub = input("Elige una opción (a/b): ").strip().lower()

    if sub == "a":
        nombre = input("Nombre del ítem: ").strip().lower()
        nodo = bst.buscar(nombre)
        if nodo:
            print(f"Nombre: {nodo.nombre} | Categoría: {nodo.categoria} | Max Stack: {nodo.max_stack}")
        else:
            print(f"No se encontró '{nombre}' en el catálogo.")
    elif sub == "b":
        nodos = bst.recorrido_in_order()
        print("\nCatálogo completo (In-Order):")
        for n in nodos:
            print(f"  - {n.nombre:<22} | cat: {n.categoria:<12} | stack: {n.max_stack}")
    else:
        print("Subopción no válida.")


def opcion_calcular_crafteo(grafo: GrafoCrafteo) -> None:
    print("\n--- 2. Calcular Árbol de Crafteo (Grafo + DFS) ---")
    item = input("Ítem objetivo: ").strip().lower()
    if not grafo.existe_item(item):
        print(f"El ítem '{item}' no está registrado en recetas.json.")
        return

    try:
        cantidad = int(input("Cantidad deseada: ").strip())
        if cantidad <= 0:
            print("Ingresa un número entero mayor a 0.")
            return
    except ValueError:
        print("Entrada inválida. Debes ingresar un número entero.")
        return

    try:
        print("\nJerarquía de crafteo:")
        grafo.imprimir_jerarquia(item, cantidad)

        base = grafo.calcular_materiales_base(item, cantidad)
        print("\nMateriales base consolidados necesarios:")
        if not base:
            print("  (Este ítem ya es un material base)")
        else:
            for mat, cant in sorted(base.items()):
                print(f"  - {mat}: {cant}")
    except ValueError as err:
        print(f"Error en el grafo: {err}")


def opcion_ver_inventario(inventario: list[dict]) -> None:
    print("\n--- 3. Ver y Ordenar Inventario (QuickSort) ---")
    print("1) Por nombre (A-Z)")
    print("2) Por cantidad (Mayor a menor)")
    print("3) Por cantidad (Menor a mayor)")
    filtro = input("Elige criterio: ").strip()

    if filtro == "1":
        ordenada = quicksort_inventario(inventario, criterio="nombre", descendente=False)
    elif filtro == "2":
        ordenada = quicksort_inventario(inventario, criterio="cantidad", descendente=True)
    elif filtro == "3":
        ordenada = quicksort_inventario(inventario, criterio="cantidad", descendente=False)
    else:
        print("Filtro no válido.")
        return

    print("\nInventario ordenado:")
    for entry in ordenada:
        print(f"  - {entry['item']:<22} : {entry['cantidad']}")


def opcion_fabricar_item(
    grafo: GrafoCrafteo,
    inventario: list[dict],
    historial: PilaHistorial,
) -> None:
    print("\n--- 4. Fabricar Ítem (Búsqueda Binaria + Pila) ---")
    item = input("Ítem a fabricar: ").strip().lower()
    if not grafo.existe_item(item):
        print(f"El ítem '{item}' no existe en recetas.json.")
        return

    ingredientes = grafo.obtener_ingredientes_directos(item)
    if not ingredientes:
        print(f"'{item}' es un material base; no tiene receta para craftearse.")
        return

    try:
        cantidad_craft = int(input("Cantidad a fabricar: ").strip())
        if cantidad_craft <= 0:
            print("Ingresa un número entero mayor a 0.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    inv_ordenado = quicksort_inventario(inventario, criterio="nombre", descendente=False)

    consumos: list[tuple[str, int]] = []
    for ing, cant_unitaria in ingredientes:
        total_req = cant_unitaria * cantidad_craft
        idx = busqueda_binaria_inventario(inv_ordenado, ing)

        if idx == -1:
            print(f"Falta el ingrediente '{ing}' (necesitas {total_req}, tienes 0).")
            return

        disponible = int(inv_ordenado[idx]["cantidad"])
        if disponible < total_req:
            print(
                f"Material insuficiente para '{ing}': necesitas {total_req}, "
                f"pero solo tienes {disponible}."
            )
            return

        consumos.append((ing, total_req))

    for ing, total_req in consumos:
        restar_del_inventario(inventario, ing, total_req)

    sumar_al_inventario(inventario, item, cantidad_craft)
    guardar_json(RUTA_INVENTARIO, inventario)

    historial.push(
        {
            "item_creado": item,
            "cantidad_creada": cantidad_craft,
            "ingredientes_usados": consumos,
        }
    )
    print(f"Crafteo exitoso: {item} x{cantidad_craft}. Inventario actualizado y guardado.")


def opcion_deshacer_crafteo(inventario: list[dict], historial: PilaHistorial) -> None:
    print("\n--- 5. Deshacer Último Crafteo (Pila) ---")
    ultima = historial.pop()
    if ultima is None:
        print("No hay crafteos en el historial para deshacer.")
        return

    item_creado = ultima["item_creado"]
    cantidad_creada = ultima["cantidad_creada"]
    ingredientes_usados = ultima["ingredientes_usados"]

    restar_del_inventario(inventario, item_creado, cantidad_creada)
    for ing, cant_devolver in ingredientes_usados:
        sumar_al_inventario(inventario, ing, cant_devolver)

    guardar_json(RUTA_INVENTARIO, inventario)
    print(
        f"Se revirtió '{item_creado} x{cantidad_creada}' y se devolvieron los materiales "
        f"a inventario.json."
    )


def main() -> None:
    recetas_data = cargar_json(RUTA_RECETAS)
    catalogo_data = cargar_json(RUTA_CATALOGO)
    inventario = cargar_json(RUTA_INVENTARIO)

    grafo = GrafoCrafteo(recetas_data)
    bst = construir_bst_desde_catalogo(catalogo_data)
    historial = PilaHistorial()

    while True:
        print("\n==========================================")
        print("   ASISTENTE DE CRAFTEO E INVENTARIO (AED)")
        print("==========================================")
        print("1. Consultar ítem (BST)")
        print("2. Calcular árbol de crafteo (Grafo + DFS)")
        print("3. Ver y ordenar inventario (QuickSort)")
        print("4. Fabricar ítem (Búsqueda Binaria + Pila)")
        print("5. Deshacer último crafteo (Pila)")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            opcion_consultar_item(bst)
        elif opcion == "2":
            opcion_calcular_crafteo(grafo)
        elif opcion == "3":
            opcion_ver_inventario(inventario)
        elif opcion == "4":
            opcion_fabricar_item(grafo, inventario, historial)
        elif opcion == "5":
            opcion_deshacer_crafteo(inventario, historial)
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()