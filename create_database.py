import sqlite3
import os

def create_database():
    db_name = 'restart.db'
    db_exists = os.path.exists(db_name)

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Crear la tabla
    cur.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            anio INTEGER NOT NULL,
            isbn TEXT NOT NULL UNIQUE
        )
    ''')

    # Solo añadir los valores si la base de datos no existía previamente
    if not db_exists:
        valores = [
            ('Cien años de soledad', 'Gabriel García Márquez', 1967, 12345),
            ('El principito', 'Antoine de Saint-Exupéry', 1943, 98765),
            ('El alquimista', 'Paulo Coelho', 1988, 45678),
            ('La Odisea', 'Homero', -400, 789),
            ('El gran Gatsby', 'F. Scott Fitzgerald', 1925, 3210),
            ('Matar a un ruiseñor', 'Harper Lee', 1960, 4321),
            ('1984', 'George Orwell', 1949, 9873210),
            ('El señor de los anillos', 'J.R.R. Tolkien', 1954, 67890),
            ('El hobbit', 'J.R.R. Tolkien', 1937, 45678230),
            ('El código Da Vinci', 'Dan Brown', 2003, 7234560)
        ]

        cur.executemany("INSERT INTO libros (titulo, autor, anio, isbn) VALUES (?, ?, ?, ?)", valores)
        print("La base de datos y la tabla se han creado exitosamente, y se han añadido los valores.")
    else:
        print("La base de datos ya existía, solo se verificó la tabla.")

    result = cur.execute("SELECT * FROM libros")
    print(result.fetchall())

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

