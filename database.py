import sqlite3
from dataclasses import dataclass


class Note:
    def __init__(self, id=None, title=None, content=''):
        self.id = id
        self.title = title
        self.content = content

class Database:
    def __init__(self, NOME_BANCO):
        self.conn = sqlite3.connect(NOME_BANCO + ".db") #atributo do construtor 
        self.conn.execute("CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)" ) #Comanmdo SQL adaptado para a biblioteca do python
        
    def add(self, note):       
        self.conn.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}' , '{note.content}');")
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        notes = []
        for linha in cursor:
            note = Note(
            id = linha[0],
            title = linha[1],
            content = linha[2],
            )
            notes.append(note)
        return notes

    def update(self, entry : Note):
        self.conn.execute(f"UPDATE note SET title = '{entry.title}' , content = '{entry.content}' WHERE id = {entry.id};")
        self.conn.commit()
    
    def delete(self, note_id):
        self.conn.execute(f"DELETE FROM note WHERE id = '{note_id}';")
        self.conn.commit()
        




                