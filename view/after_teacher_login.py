import rsa
import json
from app_enum import UserEnum
from app_sockets.client_module import client_send_json_message
from csr_module.private_key_generator import PrivateKeyGenerator
from encryptions.aes_encryption import AesEncryption
from csr_module.teacher_csr_generator import CSRGenerator
from utils import convert_string_to_key, generate_mathematical_equation
from ca_module import ca_cert_generator, teacher_cert_generator
from use_case.asymmetric_enc_keys_manager import AssymetricEncryptionManager
from validators import verify_professor_identity
from use_case.session_manager import SessionManager
from database.database import add_student_mark
from database.database import get_marks
from ca_module.teacher_cert_generator import get_role

session = SessionManager()


def options_after_teacher_login_view(username):
    print("Home Screen: \n")

    print("1. Edit Your Profile")
    print("2. Verify Your Account")
    print("3. send marks")
    print("4. View marks")
    print("5. Exit")
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        edit_view(username)
    elif choice == '2':
        verify_teacher(username)
    elif choice == '3':
        send_marks(username)
    elif choice == '4':
        view_marks(username)
    elif choice == '5':
        close()

    else:
        print("Invalid choice. Please enter 1, 2, 3")


def edit_view(username):
    new_city = input("Enter new city: ")
    new_phone_number = input("Enter new phone number: ")

    aes = AesEncryption(convert_string_to_key(username))
    city_encrypted = aes.encrypt(new_city)
    phone_encrypted = aes.encrypt(new_phone_number)

    edit_request = {
        "route": "edit",
        "parameters": {
            "username": username,
            "city": city_encrypted.decode(),
            "phone_number": phone_encrypted.decode()
        }
    }
    print("city: " + str(city_encrypted))
    print("phone_number: " + str(phone_encrypted))

    serverResponse = client_send_json_message(edit_request)


def verify_teacher(username):
    print("1. Role Professor")
    print("2. Role Teacher")
    role = input("Enter your choice (1/2): ")

    print(role)
    if role != '1' and role != '2':
        print("Invalid role")
        return

    private_key_generator = PrivateKeyGenerator()
    private_key_path = private_key_generator.generate_private_key(username)

    # Generate CSR to send 
    csr_generator = CSRGenerator(private_key_path=private_key_path)
    _, teacher_csr = csr_generator.generate_csr(username)

    # Send a "verification_request" request
    verification_request = {
        "route": "verify",
        "parameters": {
            "username": username,
            "csr": teacher_csr,
            "role": int(role)
        }
    }

    # get the equation 
    response = client_send_json_message({"route": "get_equation", "parameters": {}})
    json_response = json.loads(response)

    # if equation solved successfully
    if verify_professor_identity(json_response["equation"], json_response["answer"], ):
        create_teacher_certificate_response = client_send_json_message(verification_request)
        print("Verification successful your certificate path is : " + create_teacher_certificate_response)

    else:
        print("Wrong answer verification cancelled")


def send_marks(user):
    marks = {}
    choice = '1'
    print("add marks")
    while choice == '1':
        subject_name = input("subject:")
        student_name = input("student name:")
        mark = input("mark:")
        marks[subject_name] = mark
        add_student_mark(student_name, subject_name, mark)
        print("1. add another mark")
        print("2. close")
        choice = input("Enter your choice (1/2)")

    marks = json.dumps(marks)
    private_key = AssymetricEncryptionManager().for_client(user).get().private_key
    signature = rsa.sign(marks.encode(), rsa.PrivateKey.load_pkcs1(private_key), 'SHA-256').hex()

    request = {
        "route": "marks",
        "parameters": {
            "data": marks,
            "signature": signature
        }
    }

    client_send_json_message(request)


def view_marks(username):
    # private_key = AssymetricEncryptionManager().for_client(username).get().private_key
    # data = session.get(private_key)
    # user_certificate = f"teachers_certificates/{user_name}_certificate.pem"
    role = get_role(f"teachers_certificates/{username}_certificate.pem")
    if role == 1:
        data = get_marks()
        print(data)
    else:
        print("You have to be a professor to view marks")


def close():
    request = {
        "route": "close",
        "parameters": {

        }
    }
    client_send_json_message(request)
    from app_sockets.client_module import client_close_connection
    client_close_connection()
