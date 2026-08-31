import json
from urllib.parse import unquote_plus

CONTENT_TYPES = {
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
}


def extract_route(request : str):
  linha_request = request.split()
  caminho_com_barra = linha_request[1]
  route = caminho_com_barra[1:]
  return route


def read_file(filepath):
    file = open(filepath, "rb") #APENAS O B NAO FUNCIONAVA, TEM QUE SER RB (read, binary) ; Definindo como o arquivo será aberto
    content = file.read() #efetivamente lê o conteudo, tem que abrir, depois ler
    file.close()
    return content #TAMBEM TEM COMO UTILIZAR O WITH, QUE GARANTE QUE O ARQUIVO SERÁ FECHADO


def load_data(nome_json):
   arquivo = open(f"data/{nome_json}") #Por padrão é o "r"
   dados = json.load(arquivo)
   arquivo.close()

   return dados


def load_template(template):
  arquivo = open(f"templates/{template}", "r", encoding="utf-8")
  dados_template = arquivo.read()
  arquivo.close()

  return dados_template


def extract_params(request):
    """Devolve um dicionário com os campos enviados no corpo de um POST.

    Desacopla do views.py a leitura da requisição: cabeçalho e corpo estão
    sempre separados por duas quebras de linha, e o corpo vem no formato
    'chave=valor&outra=valor', com os valores codificados pelo navegador.
    """
    request = request.replace('\r', '')  # Remove caracteres indesejados
    partes = request.split('\n\n', 1)
    if len(partes) < 2:
        return {}

    corpo = partes[1]
    params = {}
    for chave_valor in corpo.split('&'):
        if '=' not in chave_valor:
            continue
        chave, valor = chave_valor.split('=', 1)
        params[unquote_plus(chave)] = unquote_plus(valor)

    return params


def content_type(filepath):
    """Descobre o cabeçalho Content-Type a partir da extensão do arquivo."""
    return CONTENT_TYPES.get(filepath.suffix.lower(), 'application/octet-stream')


def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response += f'{headers}\n'
    response += f'\n{body}'

    return response.encode()
