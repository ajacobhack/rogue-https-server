#!/usr/bin/python3
import socket
import ssl
import argparse
from _thread import start_new_thread
import os
import requests
import sys
import subprocess
import signal
import re
import mimetypes

# Colores para resaltar mensajes
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BANNER = '\033[1;35m'

# Función para imprimir mensajes en color
def print_color(message, color):
    print(f"{color}{message}{colors.ENDC}")

# Función para crear el servidor TCP/IP
def create_server(ip, port):
    """Crea un servidor de socket TCP/IP en la IP y puerto especificados."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, int(port)))
    server.listen(1)
    return server

# Función para asignar un DNS gratuito a la IP especificada
def asignar_ddns_gratuito(ip, subdominio, token):
    """Asigna un DNS gratuito a la dirección IP especificada utilizando DuckDNS."""
    url = f"https://www.duckdns.org/update?domains={subdominio}&token={token}&ip={ip}"
    response = requests.get(url)

    if response.status_code == 200:
        return f"{subdominio}.duckdns.org"
    else:
        print_color("Error al asignar el DDNS gratuito.", colors.FAIL)
        return None

# Función para manejar la conexión con el cliente
def handle_client(client_socket, ssl_context, subdominio, token):
    with client_socket:
        ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)
        request = ssl_socket.recv(1024)
        print_color(f"[Request] {request.decode().strip()}", colors.OKBLUE)
        #print_color(request, colors.OKBLUE)
        hostname = request.split(b'Host: ')[1].split(b' ')[0].decode()

        # Obtener la ruta del archivo solicitado
        path = re.search(r'GET /(.*?) HTTP', request.decode()).group(1)

        # Comprobar si se solicita el recurso principal "/"
        if path == '':
            path = 'index.html'

        # Construir la ruta completa del archivo
        file_path = os.path.join(os.getcwd(), path)

        # Verificar si el archivo solicitado es un archivo PHP
        if file_path.endswith('.php') and os.path.isfile(file_path):
            # Ejecutar el archivo PHP y obtener la salida
            php_output = subprocess.check_output(['php', file_path])
            response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + php_output
            print_color(f"[Response] {colors.OKGREEN}200 OK{colors.ENDC}", colors.OKGREEN)
        elif os.path.isfile(file_path):
            # El archivo no es un archivo PHP, leer y enviar el contenido como se hacía anteriormente
            with open(file_path, 'rb') as file:
                content = file.read()

            # Obtener el tipo de contenido del archivo
            content_type, _ = mimetypes.guess_type(file_path)

            # Construir la respuesta HTTP con el contenido del archivo
            response = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n'.encode() + content
            print_color(f"[Response] {colors.OKGREEN}200 OK{colors.ENDC}", colors.OKGREEN)
        else:
            # Construir una respuesta de error si el archivo no existe
            response = b'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 9\r\n\r\nNot Found'
            print_color(f"[Response] {colors.FAIL}404 Not Found{colors.ENDC}", colors.FAIL)

        # Enviar la respuesta al cliente
        ssl_socket.sendall(response)

def generate_ssl_files():
    """Genera los archivos cert.pem y key.pem utilizando OpenSSL."""
    if not os.path.isfile("cert.pem") or not os.path.isfile("key.pem"):
        print_color("Generating SSL files...", colors.OKBLUE)
        try:
            # Generar clave privada
            subprocess.run(["openssl", "genrsa", "-out", "key.pem", "2048"], check=True)
            
            # Generar solicitud de firma de certificado (CSR)
            subprocess.run(["openssl", "req", "-new", "-key", "key.pem", "-out", "csr.pem", "-subj", "/CN=localhost"], check=True)
            
            # Generar certificado autofirmado válido por 365 días
            subprocess.run(["openssl", "x509", "-req", "-days", "365", "-in", "csr.pem", "-signkey", "key.pem", "-out", "cert.pem"], check=True)
            
            # Eliminar el archivo CSR
            os.remove("csr.pem")
            
            print_color("SSL files generated successfully.", colors.OKGREEN)
        except subprocess.CalledProcessError as e:
            print_color(f"Error generating SSL files: {e}", colors.FAIL)
            sys.exit(1)

def handle_interrupt(signal, frame):
    """Maneja la interrupción manual del servidor."""
    print_color("\nManually interrupted connection. Server stopped.", colors.WARNING)
    sys.exit(0)

# Función principal
def main():
    # Crear el banner
    banner = f"""{colors.BANNER}


_____________  _____   _  __________ ____   _____________  _________ 
|__/|  || __|  ||___   |__| |  | |__][__    [__ |___|__/|  ||___|__/ 
|  \|__||__]|__||___   |  | |  | |   ___]   ___]|___|  \ \/ |___|  \ 

Rogue Https Server v1.0
Coded by ajacobhack

{colors.ENDC}"""

    # Imprimir banner
    print(banner)

    # Configuración de los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="HTTPS/SSL Server")
    parser.add_argument('-i', '--ip', help='The IP address to bind to.')
    parser.add_argument('-p', '--port', help='The port to listen on.')
    parser.add_argument('-s', '--subdomain', help='The subdomain to assign for free DNS (optional).')
    parser.add_argument('-t', '--token', help='The DuckDNS token for free DNS (optional).')
    args = parser.parse_args()

    # Imprimir menú de ayuda si no se proporcionan argumentos
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Obtener los valores de los argumentos
    ip = args.ip
    port = args.port
    subdomain = args.subdomain
    token = args.token

    # Imprimir información de configuración
    print_color(f"[Configuration] IP: {ip}", colors.OKGREEN)
    print_color(f"[Configuration] Port: {port}", colors.OKGREEN)
    if subdomain and token:
        print_color(f"[Configuration] Subdomain: {subdomain}", colors.OKGREEN)
        print_color(f"[Configuration] DuckDNS Token: {token}", colors.OKGREEN)

    # Generar archivos SSL si no existen
    generate_ssl_files()

    # Crear el contexto SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.check_hostname = False  # Desactivar verificación del nombre de host
    ssl_context.load_cert_chain(certfile='./cert.pem', keyfile='./key.pem')

    # Crear el servidor
    server = create_server(ip, port)
    
    # Manejar la interrupción manual del servidor (Ctrl+C)
    signal.signal(signal.SIGINT, handle_interrupt)

    # Imprimir estado de conexión
    print_color("[Connecting] Server is running and waiting for connections...", colors.OKBLUE)

    # Manejar las conexiones entrantes
    while True:
        client_socket, address = server.accept()
        start_new_thread(lambda: handle_client(client_socket, ssl_context, subdomain, token), ())

if __name__ == '__main__':
    main()
