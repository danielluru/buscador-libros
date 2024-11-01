import requests
import webbrowser


def buscar_libros(query, tipo_busqueda, start_index=0):
    if tipo_busqueda == 'autor':
        url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{query}&langRestrict=es&startIndex={start_index}'
    elif tipo_busqueda == 'isbn':
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{query}&langRestrict=es&startIndex={start_index}'
    elif tipo_busqueda == 'genero':
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{query}&langRestrict=es&startIndex={start_index}'
    else:
        url = f'https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict=es&startIndex={start_index}'

    response = requests.get(url)
    return response.json()


def mostrar_detalles(libro):
    titulo = libro.get('title', 'Título no disponible')
    autores = ', '.join(libro.get('authors', ['Autor desconocido']))
    fecha_publicacion = libro.get('publishedDate', 'Fecha no disponible')
    calificacion = libro.get('averageRating', 'No disponible')
    descripcion = libro.get('description', 'Descripción no disponible')
    url = libro.get('infoLink', 'No disponible')

    print(f"\nDetalles del libro seleccionado:")
    print(f"Título: {titulo}")
    print(f"Autores: {autores}")
    print(f"Fecha de publicación: {fecha_publicacion}")
    print(f"Calificación promedio: {calificacion} sobre 5")
    print(f"Descripción: {descripcion}")
    print(f"Más información: {url}")

    if url != 'No disponible':
        abrir_url = input("\n¿Quieres abrir la URL en tu navegador? (s/n): ").strip().lower()
        if abrir_url == 's':
            webbrowser.open(url)


def buscar():
    while True:
        print("Opciones de búsqueda:")
        print("1. Búsqueda general por título o palabra clave")
        print("2. Búsqueda por autor")
        print("3. Búsqueda por ISBN")
        print("4. Búsqueda por género/categoría")
        opcion = input("\nSelecciona una opción de búsqueda (1-4) o 'q' para salir: ").strip().lower()

        if opcion == 'q':
            print("Saliendo del programa...")
            break

        if opcion == '1':
            query = input("Introduce el título o palabra clave del libro: ")
            tipo_busqueda = 'general'
        elif opcion == '2':
            query = input("Introduce el nombre del autor: ")
            tipo_busqueda = 'autor'
        elif opcion == '3':
            query = input("Introduce el ISBN del libro: ")
            tipo_busqueda = 'isbn'
        elif opcion == '4':
            query = input("Introduce el género o categoría del libro (Ejemplo: Fiction, History, Fantasy): ")
            tipo_busqueda = 'genero'
        else:
            print("Opción no válida.")
            continue

        start_index = 0
        while True:
            resultados = buscar_libros(query, tipo_busqueda, start_index)

            if 'items' in resultados:
                print(f"\nMostrando resultados {start_index + 1} - {start_index + len(resultados['items'])}")
                for idx, libro in enumerate(resultados['items'], 1):
                    titulo = libro['volumeInfo'].get('title', 'Título no disponible')
                    autores = ', '.join(libro['volumeInfo'].get('authors', ['Autor desconocido']))
                    print(f"{idx}. {titulo} por {autores}")

                print("\nSelecciona el número del libro para ver detalles, o elige:")
                print("n - Para ir a la siguiente página")
                print("p - Para ir a la página anterior")
                print("r - Para regresar a la selección de búsqueda")
                print("q - Para salir")

                seleccion = input("Tu selección: ").strip().lower()
                if seleccion == 'q':
                    print("Saliendo del programa...")
                    return
                elif seleccion == 'r':
                    print("Regresando a la selección de búsqueda...")
                    break
                elif seleccion == 'n':
                    start_index += len(resultados['items'])  # Avanzar al siguiente conjunto de resultados
                elif seleccion == 'p':
                    start_index = max(0, start_index - len(resultados['items']))  # Retroceder al conjunto anterior
                else:
                    try:
                        seleccion = int(seleccion)
                        if 1 <= seleccion <= len(resultados['items']):
                            libro = resultados['items'][seleccion - 1]['volumeInfo']
                            mostrar_detalles(libro)
                        else:
                            print("Número inválido. Por favor, selecciona un número de la lista.")
                    except ValueError:
                        print("Entrada inválida. Por favor, ingresa un número, 'n', 'p', 'r', o 'q'.")
            else:
                print("No se encontraron más libros.")
                break


# Ejecutar la búsqueda
if __name__ == "__main__":
    buscar()
