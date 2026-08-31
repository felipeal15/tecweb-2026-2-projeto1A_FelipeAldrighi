import sqlite3


class Note:
    def __init__(self, id=None, title=None, content='', favorita=0):
        self.id = id
        self.title = title
        self.content = content
        self.favorita = favorita


class Database:
    COLUNAS = 'id, title, content, favorita'

    def __init__(self, NOME_BANCO):
        self.conn = sqlite3.connect(NOME_BANCO + ".db")  # atributo do construtor
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS note ("
            "  id INTEGER PRIMARY KEY,"
            "  title TEXT,"
            "  content TEXT NOT NULL,"
            "  favorita INTEGER NOT NULL DEFAULT 0"
            ")"
        )  # Comando SQL adaptado para a biblioteca do python
        self._cria_coluna_favorita()
        self.conn.commit()

    def _cria_coluna_favorita(self):
        # Bancos criados no handout 03 não têm a coluna favorita, e o
        # CREATE TABLE IF NOT EXISTS acima não altera uma tabela que já existe.
        colunas = [linha[1] for linha in self.conn.execute("PRAGMA table_info(note)")]
        if 'favorita' not in colunas:
            self.conn.execute(
                "ALTER TABLE note ADD COLUMN favorita INTEGER NOT NULL DEFAULT 0")

    def add(self, note):
        cursor = self.conn.execute(
            "INSERT INTO note (title, content, favorita) VALUES (?, ?, ?);",
            (note.title, note.content, note.favorita),
        )
        self.conn.commit()
        note.id = cursor.lastrowid
        return note

    def get_all(self):
        # As favoritas vêm primeiro; dentro de cada grupo, as mais recentes.
        cursor = self.conn.execute(
            f"SELECT {self.COLUNAS} FROM note ORDER BY favorita DESC, id DESC")
        notes = []
        for linha in cursor:
            notes.append(self._monta_note(linha))
        return notes

    def get(self, note_id):
        cursor = self.conn.execute(
            f"SELECT {self.COLUNAS} FROM note WHERE id = ?;", (note_id,))
        linha = cursor.fetchone()
        if linha is None:
            return None
        return self._monta_note(linha)

    def update(self, entry: Note):
        self.conn.execute(
            "UPDATE note SET title = ?, content = ?, favorita = ? WHERE id = ?;",
            (entry.title, entry.content, entry.favorita, entry.id),
        )
        self.conn.commit()

    def delete(self, note_id):
        self.conn.execute("DELETE FROM note WHERE id = ?;", (note_id,))
        self.conn.commit()

    def toggle_favorita(self, note_id):
        self.conn.execute(
            "UPDATE note SET favorita = 1 - favorita WHERE id = ?;", (note_id,))
        self.conn.commit()

    def _monta_note(self, linha):
        return Note(
            id=linha[0],
            title=linha[1],
            content=linha[2],
            favorita=linha[3],
        )
