
from app_enum import UserEnum
from app_sockets.client_module import client_send_json_message
from encryptions.aes_encryption import AesEncryption
from utils import convert_string_to_key


def options_after_login_view(username):

    print("Home Screen: \n")

    print("1. Edit Your Profile")
    print("2. Exist")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        edit_view(username)
        options_after_login_view(username)
    elif choice == '3':
        close()

        
    else:
        print("Invalid choice. Please enter 1")



def edit_view(username):
    new_city = input("Enter new city: ")
    new_phone_number = input("Enter new phone number: ")


    edit_request = {
        "route": "edit",
        "parameters": {
            "username": username,
            "city": new_city,
            "phone_number": new_phone_number
        }
    }
    print("city"+ str(new_city))
    print("phone_number"+ str(new_phone_number))

    serverResponse = client_send_json_message(edit_request)


def close():
    request = {
        "route": "close",
        "parameters": {

        }
    }
    client_send_json_message(request)
    from app_sockets.client_module import client_close_connection
    client_close_connection()