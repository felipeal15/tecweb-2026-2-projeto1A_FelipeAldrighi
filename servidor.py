import socket
from pathlib import Path

from utils import extract_route, read_file, build_response, content_type
from views import index, edit, delete, favorite, not_found

CUR_DIR = Path(__file__).parent
SERVER_HOST = 'localhost'
SERVER_PORT = 8081
# O <textarea> do formulário aceita textos longos: 1024 bytes cortariam o
# corpo da requisição no meio e o POST chegaria incompleto.
BUFFER_SIZE = 65536

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(BUFFER_SIZE).decode()
    if not request:
        client_connection.close()
        continue

    print('*'*100)
    print(request)

    route = extract_route(request)
    # 'delete/3' -> ['delete', '3']: o primeiro pedaço diz o que fazer e o
    # segundo, quando existe, é o id da anotação.
    partes = route.split('/')

    filepath = CUR_DIR / route
    if route and filepath.is_file():
        headers = f'Content-Type: {content_type(filepath)}'
        response = build_response(headers=headers) + read_file(filepath)
    elif route == '':
        response = index(request)
    elif partes[0] == 'edit' and len(partes) == 2:
        response = edit(request, partes[1])
    elif partes[0] == 'delete' and len(partes) == 2:
        response = delete(request, partes[1])
    elif partes[0] == 'favorite' and len(partes) == 2:
        response = favorite(request, partes[1])
    else:
        response = not_found(request)

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()
