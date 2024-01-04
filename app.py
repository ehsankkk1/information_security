import asyncio
import os
import threading
from app_sockets.client_module import connect_to_server
from app_sockets.server_module import start_socket_server
from database.database import initalizeDataBaseTables
from view.choose_user_type import choose_client_type
from cryptography import x509
from view.after_teacher_login import options_after_teacher_login_view
from view.auth import handshake,send_session_key

host = "127.0.0.1"
port = 5001
port2 = 5002

initalizeDataBaseTables()

choice = input("Do you want server(1) or ca server(2) or client(3) : ")


def initialize_client_threads():
    # threads of the client after start

    # trigger this function choose_client_type
    threading.Thread(target=choose_client_type, args=()).start()


def initialize_client_threads_ssl(user_name):
    # threads of the client after start
    handshake(user_name)
    send_session_key()
    # trigger this function choose_client_type
    threading.Thread(target=options_after_teacher_login_view(user_name), args=()).start()


if choice == "1":
    asyncio.run(start_socket_server(host, port, False))

elif choice == "2":
    asyncio.run(start_socket_server(host, port2, True))

elif choice == "3":
    # Un Comment the input values in the day of the presentation
    # host_input = choice("Enter the server host")
    port_input = input("Enter the server port: \n")
    port_integer = int(port_input)

    if port_integer == port:
        connect_to_server(host, port)
        initialize_client_threads()

    elif port_integer == port2:
        user_name = input("For accessing teacher server enter your certificate name : \n")

        user_certificate = f"teachers_certificates/{user_name}_certificate.pem"
        user_pk = f'csr_module/{user_name}_private.key'

        if os.path.exists(user_certificate) and os.path.exists(user_pk):
            connect_to_server(host, port2, user_certificate, user_pk)
            print("Successfully Connected using certificate")
            initialize_client_threads_ssl(user_name)

        else:
            print(f"{user_name} don't have a certificate or private key please verify first ")

    else:
        print("There is no such port running")





else:
    exit()
