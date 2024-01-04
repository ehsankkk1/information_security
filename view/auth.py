import json
from app_enum import UserEnum
from app_sockets.client_module import client_send_json_message
from view.after_login import options_after_login_view
from view.after_teacher_login import options_after_teacher_login_view
from use_case.asymmetric_enc_keys_manager import AssymetricEncryptionManager
from use_case.session_manager import SessionManager
import secrets
import rsa
import base64

client_session = SessionManager()


def auth_view(userType):
    print("1. Add User")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        sign_up_view(userType)

    elif choice == '2':
        login_view(userType)
    elif choice == '3':
        close()

    else:
        print("Invalid choice. Please enter 1, 2, 3")


def sign_up_view(userType):
    print("Add " + userType.name + ":")
    username = input("Enter username: ")
    city = input("Enter city: ")
    phone_number = input("Enter phone number: ")
    password = input("Enter password: ")

    # Send a "sign up" request
    sign_up_request = {
        "route": "signup",
        "parameters": {
            "username": username,
            "city": city,
            "phone_number": phone_number,
            "password": password,
            "user_type": userType.name
        }
    }
    server_response = client_send_json_message(sign_up_request)

    if (server_response == "Error: Username must be unique. User not added."):
        print(server_response)
        return

    AssymetricEncryptionManager().for_client(username).generate()


def login_view(userType):
    print("Login \n")
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Send a "login" request
    login_request = {
        "route": "login",
        "parameters": {
            "username": username,
            "password": password
        }
    }
    serverResponse = client_send_json_message(login_request)

    if serverResponse == "Login failed no account available":
        return
    else:
        handshake(username)
        send_session_key()
        print(client_session.all())
        if userType is UserEnum.STUDENT:
            options_after_login_view(username)
        elif userType is UserEnum.TEACHER:
            options_after_teacher_login_view(username)


def handshake(user):
    public_key = AssymetricEncryptionManager().for_client(user).get().public_key
    handshake_request = {
        "route": "handshake",
        "parameters": {
            "key": public_key,
            "username": user
        }
    }
    serverResponse = client_send_json_message(handshake_request)
    client_session.set('server_public', serverResponse)


def send_session_key():
    public_key = client_session.get('server_public')
    session_key = base64.urlsafe_b64encode(secrets.token_bytes(32))
    encrypted_session_key = rsa.encrypt(session_key, rsa.PublicKey.load_pkcs1(public_key)).hex()

    session_key_request = {
        "route": "session_key",
        "parameters": {
            "key": encrypted_session_key
        }
    }
    serverResponse = client_send_json_message(session_key_request)

    if serverResponse == 'done':
        client_session.set('session_key', session_key)


def close():
    request = {
        "route": "close",
        "parameters": {

        }
    }
    client_send_json_message(request)

    from app_sockets.client_module import client_close_connection
    client_close_connection()
