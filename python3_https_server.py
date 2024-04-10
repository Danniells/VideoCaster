#Desative o servidor quando não estiver em uso:
#Quando não estiver usando o servidor HTTP, desative-o para evitar que ele seja acessado por usuários não autorizados.
#Use o comando kill para matar o processo do servidor HTTP.
#Para rodar o servidor, utilizar o comando sudo python3 -u "caminho/para/o/arquivo/do/servidor/python3_https_server.py"

import http.server
import ssl

httpd = http.server.HTTPServer(('127.0.0.1', 443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.load_cert_chain(certfile='./server.pem')
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()