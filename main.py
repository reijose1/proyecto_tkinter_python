import tkinter as tk
from create_database import create_database
from gui import LibraryApp

def main():
    # Crear la base de datos y la tabla si no existen
    create_database()
    # Inicializar la aplicación GUI
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()




