import json
import rsa
from ca_module import teacher_cert_generator

# from app_sockets.server_module import server_socket
from database.database import add_user_db, edit_user_info_db, login_user_db, create_teacher_csr_db, \
    insert_client_pub_key, get_client_pub_key
from encryptions.aes_encryption import AesEncryption
from utils import convert_string_to_key, generate_mathematical_equation
from use_case.asymmetric_enc_keys_manager import AssymetricEncryptionManager
from use_case.session_manager import SessionManager
from validators import verify_professor_identity
from ca_module.teacher_cert_generator import set_role,get_role
server_session = SessionManager()
client_address = None


def handle_AppRouting(jsonString, address):
    global client_address
    client_address = address

    request = json.loads(jsonString)
    # Extract route and parameters from the request
    route = request["route"]
    parameters = request["parameters"]
    print("Activated Route: " + route)
    if route == "signup":
        response = sign_up_route(parameters)

    elif route == "login":
        response = login_route(parameters)

    elif route == "edit":
        response = edit_route(parameters)

    elif route == "get_equation":
        response = get_equation()

    elif route == "verify":
        response = verify_route(parameters)

    elif route == "handshake":
        response = handshake_route(parameters)

    elif route == "session_key":
        response = session_key_route(parameters)

    elif route == "marks":
        response = marks(parameters)

    elif route == "close":
        response = close_route(parameters)

    else:
        response = "Invalid Route"

    print(response)
    return response


def sign_up_route(parameters):
    response = add_user_db(
        parameters["username"],
        parameters["city"],
        parameters["phone_number"],
        parameters["password"],
        parameters["user_type"],
    )

    return response


def login_route(parameters):
    user = login_user_db(
        parameters["username"],
        parameters["password"]
    )

    if user:
        return f"Login successful! Welcome, {user[1]}"
    else:
        return "Login failed no account available"


def edit_route(parameters):
    city = parameters["city"]
    phone_number = parameters["phone_number"]

    db_response = edit_user_info_db(
        parameters["username"],
        city,
        phone_number,
    )

    return db_response


def verify_route(parameters):
    teacher_certificate = teacher_cert_generator.generate_teacher_certificate(
        'ca_module/ca-certificate.pem',
        'ca_module/ca-key.pem',
        parameters["csr"],
        parameters["username"],
    )
    set_role(
        'ca_module/ca-certificate.pem',
        'ca_module/ca-key.pem',
        teacher_certificate,
        parameters["role"]
    )

    print(get_role(teacher_certificate))
    db_response = create_teacher_csr_db(
        parameters["username"],
        parameters["csr"],
    )

    return teacher_certificate


def get_equation():
    equation, correct_answer = generate_mathematical_equation()
    return_json = {
        "equation": equation,
        "answer": correct_answer,
    }
    return json.dumps(return_json)


def handshake_route(parameters):
    if get_client_pub_key(parameters['username']) is None:
        insert_client_pub_key(parameters['username'], parameters['key'])

    key = AssymetricEncryptionManager().for_server().get().public_key
    server_session.set(f"{client_address}_public", parameters['key'])
    return key


def session_key_route(parameters):
    private_key = AssymetricEncryptionManager().for_server().get().private_key
    encrypted_session_key = parameters['key']

    try:
        session_key = rsa.decrypt(bytes.fromhex(encrypted_session_key), rsa.PrivateKey.load_pkcs1(private_key))
        server_session.set(f"{client_address}_session", session_key)
        return 'done'
    except rsa.DecryptionError as e:
        return 'fail'


def marks(parameters):
    client_public_key = server_session.get(f"{client_address}_public")

    try:
        rsa.verify(parameters["data"].encode(), bytes.fromhex(parameters["signature"]),
                   rsa.PublicKey.load_pkcs1(client_public_key))
        print(parameters['data'])
        return 'done'
    except rsa.DecryptionError as e:
        return 'fail'


def close_route(parameters):
    server_session.remove(f"{client_address}_session")
    server_session.remove(f"{client_address}_public")
    return 'done'
