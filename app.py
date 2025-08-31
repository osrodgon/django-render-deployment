import streamlit as st
import datetime
import requests

st.sidebar.title('Menú')
st.sidebar.write('Bienvenidxs a mi librería')

st.title('Bienvenidxs a mi librería')
st.write('Estos son mis libros desde mi API:')

# Mostrar libros existentes
response = requests.get('http://127.0.0.1:8000/v1/books')
if response.status_code == 200:
    books = response.json()
    for book in books:
        st.write(f"Titulo: {book['titulo']}")
        st.write(f"Categorías: {', '.join([str(category) for category in book['categories']])}")
        if st.button(f"Ver detalle {book['id']}"):
            st.write(book)
        if st.button(f"Borrar {book['id']}"):
            delete_response = requests.delete(f"http://127.0.0.1:8000/v1/books/{book['id']}")
            if delete_response.status_code == 204:
                st.write(f"Libro {book['id']} borrado")
            else:
                st.write(f"No se pudo borrar el libro {book['id']}")
else:
    st.write('No se encontraron libros')

# Obtener categorías existentes
categories_response = requests.get('http://127.0.0.1:8000/v1/categories')
categories = []
if categories_response.status_code == 200:
    categories = categories_response.json()

# Formulario para crear un nuevo libro
st.sidebar.title('Crear nuevo libro')
title = st.sidebar.text_input('Título')
author = st.sidebar.text_input('Autor')
isbn = st.sidebar.text_input('ISBN')
date_published = st.sidebar.date_input(
    'Fecha de publicación', 
    min_value=datetime.date(1, 1, 1),
    max_value=datetime.date.today()
)
selected_categories = st.sidebar.multiselect(
    'Categorías', [category['id'] for category in categories], format_func=lambda id: next(c['name'] for c in categories if c['id'] == id)
)

if st.sidebar.button('Crear libro'):
    nuevo_libro = {
        'title': title,
        'author': author,
        'isbn': isbn,
        'date_published': str(date_published),
        'categories': selected_categories
    }
    create_response = requests.post('http://127.0.0.1:8000/v1/books/create', json=nuevo_libro)
    if create_response.status_code == 201:
        st.sidebar.write('Libro creado exitosamente')
    else:
        st.sidebar.write('Error al crear el libro!')