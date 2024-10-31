import requests
import webbrowser


def buscar_libros(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict=es'
    response = requests.get(url)
    return response.json()


def mostrar_detalles(libro):
    # Obtenemos y mostramos los detalles del libro
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
    print(f"Calificación promedio: {calificacion}/5")
    print(f"Descripción: {descripcion}")
    print(f"Más información: {url}")

    # Pregunta si se desea abrir la URL en el navegador
    if url != 'No disponible':
        abrir_url = input("\n¿Quieres abrir la URL en tu navegador? (s/n): ").strip().lower()
        if abrir_url == 's':
            webbrowser.open(url)


def buscar():
    query = input("Introduce el título o autor del libro: ")
    resultados = buscar_libros(query)

    if 'items' in resultados:
        print(f"\nSe encontraron {len(resultados['items'])} libros:")
        for idx, libro in enumerate(resultados['items'], 1):
            titulo = libro['volumeInfo'].get('title', 'Título no disponible')
            autores = ', '.join(libro['volumeInfo'].get('authors', ['Autor desconocido']))
            print(f"{idx}. {titulo} por {autores}")

        # Seleccionar un libro para ver detalles
        while True:
            try:
                seleccion = int(input("\nSelecciona el número del libro para ver detalles (0 para salir): "))
                if seleccion == 0:
                    break
                if 1 <= seleccion <= len(resultados['items']):
                    libro = resultados['items'][seleccion - 1]['volumeInfo']
                    mostrar_detalles(libro)
                else:
                    print("Número inválido. Por favor, selecciona un número de la lista.")
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
    else:
        print("No se encontraron libros.")


# Ejecutar la búsqueda
if __name__ == "__main__":
    buscar()
