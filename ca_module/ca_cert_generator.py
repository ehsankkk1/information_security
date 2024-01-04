import cryptography
import datetime
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import *
from cryptography.x509.oid import NameOID
from app_router.app_router import handle_AppRouting


def generate_ca_certificate():
    pk = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    ca_subject = Name([
        NameAttribute(NameOID.COMMON_NAME, "Damascus University CA"),
    ])

    issuer = ca_subject

    ca_cert = CertificateBuilder() \
        .subject_name(ca_subject) \
        .issuer_name(issuer) \
        .public_key(pk.public_key()) \
        .serial_number(random_serial_number()) \
        .not_valid_before(datetime.datetime.utcnow()) \
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650)) \
        .add_extension(BasicConstraints(ca=True, path_length=0), critical=True) \
        .sign(pk, cryptography.hazmat.primitives.hashes.SHA256(), default_backend())
    script_dir = os.path.dirname(__file__)
    ca_cert_path = os.path.join(script_dir, 'ca-certificate.pem')
    pk_path = os.path.join(script_dir, 'ca-key.pem')
    with open(ca_cert_path, 'wb') as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))
    with open(pk_path, 'wb') as f:
        f.write(pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

        return ca_cert_path, pk_path
