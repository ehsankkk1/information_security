import asyncio
import os
import struct
import ssl
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from app_router.app_router import handle_AppRouting
from ca_module import ca_cert_generator
from use_case.asymmetric_enc_keys_manager import AssymetricEncryptionManager
from encryptions.aes_encryption import AesEncryption
from utils import convert_string_to_key

# Global variable to store the server socket instance
server_socket = None

if not os.path.exists('/ca_module/ca-certificate.pem'):
    ca_cert_generator.generate_ca_certificate()


async def handle_client(reader, writer):
    
    from app_router.app_router import server_session
    
    address = writer.get_extra_info('peername')
    print(f"Connection from {address}")
    
    # receive request from the client
    while True:
        try:
            #### here get session key for client ####
            key = server_session.get(f"{address}_session")  or convert_string_to_key("secret_key")
            
            print(server_session.all())
            print('\n key \n', key)

            # Receive the length prefix
            length_prefix = await reader.readexactly(4)
            if not length_prefix:
                break  # Break the loop if no more data is received

            # Unpack the length prefix to get the message length
            message_length = struct.unpack('!I', length_prefix)[0]

            # Receive the message with the calculated length
            data = await reader.readexactly(message_length)
            
            #### here client request decryption ####
            data =  decrypt_request(data, key)

            message = data
            print("Message received in server " + message)

            
            # Trigger the function to process the data
            data_router_response = handle_AppRouting(message, address)
            print("Send: " + data_router_response)
            
            #### here server response encryption ####
            data =  encrypt_response(data_router_response, key)

            writer.write(data)
            await writer.drain()
            
        except asyncio.IncompleteReadError:
            break  # Break the loop if an incomplete read occurs


async def start_socket_server(host, port,use_ssl=False):
    global server_socket
    if use_ssl:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        context.load_verify_locations('ca_module/ca-certificate.pem')
        context.load_cert_chain(certfile='ca_module/ca-certificate.pem', keyfile='ca_module/ca-key.pem')
        server_socket = await asyncio.start_server(
            handle_client, host, port, ssl=context)

    else:
        server_socket = await asyncio.start_server(
            handle_client, host, port)


    generate_public_private_pair()
    address = server_socket.sockets[0].getsockname()
    print(f'Server listening on {address}')

    async with server_socket:
        await server_socket.serve_forever()



def generate_public_private_pair():
    AssymetricEncryptionManager().for_server().generate()

def encrypt_response(data, key):
    
    aes = AesEncryption(key)
    data = aes.encrypt(data)
    return data


def decrypt_request(data, key):
    aes = AesEncryption(key)
    data = aes.decrypt(data)
    return data