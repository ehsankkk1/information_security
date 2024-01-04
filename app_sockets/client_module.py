import json
import socket
import struct
import threading
import ssl
from encryptions.aes_encryption import AesEncryption
from utils import convert_string_to_key

# Global variable to store the client socket instance
client_socket = None


def connect_to_server(host, port, cert_path=None, key_path=None, force_secure=False):
    global client_socket
    server_address = (host, port)
    if force_secure and (not cert_path or not key_path):
        # User doesn't have a certificate and secure connection is forced
        print("Secure connection is required, but you don't have a valid certificate yet.")
        print("Please acquire a certificate and try again.")
        return  # Terminate connection attempt

    if cert_path and key_path:  # Use secure connection if certificate is available
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        client_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host)
        client_socket.connect(server_address)

    else:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect(server_address)


def client_send_json_message(fields):
    global client_socket
    # Convert the fields to a JSON string
    message = encrypt_request(json.dumps(fields))
    # Prefix the message with its length
    message_length = len(message)
    length_prefix = struct.pack('!I', message_length)
    message_with_length = length_prefix + message

    # Send the message to the server

    client_socket.sendall(message_with_length)

    # Wait for the server to respond
    return client_receive_response()


def client_receive_response():
    # Receive and print the response from the server
    response = client_socket.recv(1024)
    response = decrypt_response(response)
    print('\n********* Server **********')
    print(response)
    print('********* Server **********\n')
    return response


def client_close_connection():
    global client_socket
    # Close the connection
    client_socket.close()


def encrypt_request(data):
    from view.auth import client_session
    key = client_session.get('session_key') or convert_string_to_key("secret_key")
    aes = AesEncryption(key)
    data = aes.encrypt(data)
    print(client_session.get('session_key'), '\n-----\n', convert_string_to_key("secret_key"), '\n-----\n', key)
    return data


def decrypt_response(data):
    from view.auth import client_session
    key = client_session.get('session_key') or convert_string_to_key("secret_key")
    aes = AesEncryption(key)
    data = aes.decrypt(data)
    return data
