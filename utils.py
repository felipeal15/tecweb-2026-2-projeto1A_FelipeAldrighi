import json

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
  arquivo = open(f"templates/{template}", "r")
  dados_template = arquivo.read()
  arquivo.close()

  return dados_template


def add_note(nota):
    notas = load_data('notes.json')
    notas.append(nota)

    arquivo = open('data/notes.json', 'w')
    json.dump(notas, arquivo, ensure_ascii=False, indent=2)
    arquivo.close()


def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response += f'{headers}\n'
    response += f'\n{body}'

    return response.encode()
