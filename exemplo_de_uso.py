from database import Database

db = Database('data/banco')

for note in db.get_all():
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')
