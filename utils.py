def extract_route(request : str):
  linha_request = request.split()
  caminho_com_barra = linha_request[1]
  route = caminho_com_barra[1:]
  return route



request = """ 
GET /img/logo-getit.png HTTP/1.1
Host: 0.0.0.0:8080
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Referer: http://0.0.0.0:8080/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,pt;q=0.8
"""

extract_route(request)


def read_file(filepath):
    file = open(filepath, "rb") #APENAS O B NAO FUNCIONAVA, TEM QUE SER RB (read, binary) ; Definindo como o arquivo será aberto
    content = file.read() #efetivamente lê o conteudo, tem que abrir, depois ler
    file.close()
    return content #TAMBEM TEM COMO UTILIZAR O WITH, QUE GARANTE QUE O ARQUIVO SERÁ FECHADO
