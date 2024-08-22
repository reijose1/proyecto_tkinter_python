import tkinter as tk
from tkinter import messagebox, ttk
from library_manager import LibraryManager
from PIL import Image, ImageTk

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca del AWS Re/Start")
        self.root.configure(bg="black")  # Fondo negro
        self.manager = LibraryManager()

        # Variables
        self.titulo_var = tk.StringVar()
        self.autor_var = tk.StringVar()
        self.anio_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Crear componentes de la interfaz
        self.create_widgets()
        self.populate_list()

    def create_widgets(self):
        # Encabezado
        tk.Label(self.root, text="Gestión de Libros", font=("Arial", 22), fg="#ff9900", bg="black").grid(row=0, column=0, columnspan=2, pady=10)

        # Cargar la imagen del Re/Start usando PIL
        image = Image.open("restart.png")
        image = image.resize((150, 60), Image.ANTIALIAS)  # Redimensionar la imagen si es necesario
        img = ImageTk.PhotoImage(image)

        # Crear un Label para mostrar la imagen
        image_label = tk.Label(self.root, image=img, bg="black")
        image_label.image = img  # Guardar una referencia de la imagen
        image_label.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

        # Entradas y etiquetas
        tk.Label(self.root, text="Titulo", font=("Arial", 14), fg="#ff9900", bg="black").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.titulo_var, font=("Arial", 14), width=40).grid(row=2, column=1, columnspan=2)

        tk.Label(self.root, text="Autor", font=("Arial", 14), fg="#ff9900", bg="black").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.autor_var, font=("Arial", 14), width=40).grid(row=3, column=1, columnspan=2)

        tk.Label(self.root, text="Año", font=("Arial", 14), fg="#ff9900", bg="black").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.anio_var, font=("Arial", 14), width=40).grid(row=4, column=1, columnspan=2)

        tk.Label(self.root, text="ISBN", font=("Arial", 14), fg="#ff9900", bg="black").grid(row=5, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.isbn_var, font=("Arial", 14), width=40).grid(row=5, column=1, columnspan=2)

        # Botones
        tk.Button(self.root, text="Agregar", fg="black", bg="#ff9900", font=("Arial", 14), command=self.add_book).grid(row=6, column=0, padx=5, pady=10)
        tk.Button(self.root, text="Actualizar", fg="black", bg="#ff9900", font=("Arial", 14), command=self.update_book).grid(row=6, column=1, padx=5, pady=10)
        tk.Button(self.root, text="Eliminar", fg="black", bg="#ff9900", font=("Arial", 14), command=self.delete_book).grid(row=6, column=2, padx=5, pady=10)
        tk.Button(self.root, text="Limpiar Campos", fg="black", bg="#ff9900", font=("Arial", 14), command=self.clear_fields).grid(row=6, column=3, padx=5, pady=10)

        # Área de búsqueda
        tk.Label(self.root, text="Buscar por Autor", font=("Arial", 14), fg="#ff9900", bg="black").grid(row=7, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.buscar_var, font=("Arial", 14), width=30).grid(row=7, column=1, columnspan=2)
        tk.Button(self.root, text="Buscar", fg="black", bg="#ff9900", font=("Arial", 14), command=self.search_books).grid(row=7, column=3, padx=10, pady=10)

        # Listado de libros
        self.listado = ttk.Treeview(self.root, columns=("ID", "Titulo", "Autor", "Año", "ISBN"), show='headings')
        self.listado.heading("ID", text="ID")
        self.listado.heading("Titulo", text="Titulo")
        self.listado.heading("Autor", text="Autor")
        self.listado.heading("Año", text="Año")
        self.listado.heading("ISBN", text="ISBN")
        self.listado.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

        self.listado.bind("<ButtonRelease-1>", self.load_selected_book)

        # Etiqueta para mostrar el texto adicional del autor
        tk.Label(self.root, text="por Reinaldo Carrillo", font=("Arial", 14), fg="black", bg="#ff9900").grid(row=9, column=0, columnspan=4, pady=10)
        tk.Label(self.root, text="AWS Re/Start - Morris & Opazo", font=("Arial", 12), fg="#ff9900", bg="black").grid(row=10, column=0, columnspan=4, pady=10)

    def populate_list(self):
        self.listado.delete(*self.listado.get_children())
        for row in self.manager.fetch_all_books():
            self.listado.insert("", "end", values=row)

    def add_book(self):
        titulo = self.titulo_var.get()
        autor = self.autor_var.get()
        anio = self.anio_var.get()
        isbn = self.isbn_var.get()

        if not titulo or not autor or not anio or not isbn:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        # Verificación de que el año sea un número
        if not anio.isdigit():
            messagebox.showerror("Error", "El año debe ser un número")
            return

        result = self.manager.add_book(titulo, autor, int(anio), isbn)
        if result:
            messagebox.showerror("Error", result)
        else:
            messagebox.showinfo("Success", "Libro Agregado Exitosamente")
            self.populate_list()
            self.clear_fields()

    def update_book(self):
        selected = self.listado.selection()
        if not selected:
            messagebox.showerror("Error", "No ha seleccionado ningún libro")
            return

        id = self.listado.item(selected[0], "values")[0]
        titulo = self.titulo_var.get()
        autor = self.autor_var.get()
        anio = self.anio_var.get()
        isbn = self.isbn_var.get()

        if not titulo or not autor or not anio or not isbn:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        # Verificación de que el año sea un número
        if not anio.isdigit():
            messagebox.showerror("Error", "El año debe ser un número")
            return

        self.manager.update_book(id, titulo, autor, int(anio), isbn)
        messagebox.showinfo("Success", "Libro Actualizado Exitosamente")
        self.populate_list()
        self.clear_fields()

    def delete_book(self):
        selected = self.listado.selection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún libro")
            return

        id = self.listado.item(selected[0], "values")[0]

        self.manager.delete_book(id)
        messagebox.showinfo("Success", "Libro eliminado exitosamente")
        self.populate_list()
        self.clear_fields()

    def search_books(self):
        autor = self.buscar_var.get()
        if not autor:
            messagebox.showerror("Error", "Campo del autor es requerido")
            return

        results = self.manager.search_books_by_author(autor)
        self.listado.delete(*self.listado.get_children())
        for row in results:
            self.listado.insert("", "end", values=row)

    def load_selected_book(self, event):
        selected = self.listado.selection()
        if not selected:
            return

        id, titulo, autor, anio, isbn = self.listado.item(selected[0], "values")
        self.titulo_var.set(titulo)
        self.autor_var.set(autor)
        self.anio_var.set(anio)
        self.isbn_var.set(isbn)

    def clear_fields(self):
        self.titulo_var.set("")
        self.autor_var.set("")
        self.anio_var.set("")
        self.isbn_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
