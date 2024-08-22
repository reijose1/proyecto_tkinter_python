import sqlite3

class LibraryManager:
    def __init__(self):
        self.connection = sqlite3.connect('restart.db')
        self.cursor = self.connection.cursor()

    def add_book(self, titulo, autor, anio, isbn):
        try:
            self.cursor.execute(
                "INSERT INTO libros (titulo, autor, anio, isbn) VALUES (?, ?, ?, ?)",
                (titulo, autor, anio, isbn)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            return "Este ISBN ya existe."

    def update_book(self, id, titulo, autor, anio, isbn):
        self.cursor.execute(
            "UPDATE libros SET titulo=?, autor=?, anio=?, isbn=? WHERE id=?",
            (titulo, autor, anio, isbn, id)
        )
        self.connection.commit()

    def delete_book(self, id):
        self.cursor.execute("DELETE FROM libros WHERE id=?", (id,))
        self.connection.commit()

    def fetch_all_books(self):
        self.cursor.execute("SELECT * FROM libros")
        return self.cursor.fetchall()

    def search_books_by_author(self, autor):
        self.cursor.execute("SELECT * FROM libros WHERE autor LIKE ?", ('%' + autor + '%',))
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()
