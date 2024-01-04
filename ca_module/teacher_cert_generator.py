import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography import x509
import datetime


def generate_teacher_certificate(ca_cert, ca_key, teacher_csr, username):
    # Load the CA certificate and private key
    with open(ca_cert, 'rb') as f:
        ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())
    with open(ca_key, 'rb') as f:
        ca_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

    # Load the teacher's CSR
    with open(teacher_csr, 'rb') as f:
        teacher_csr = x509.load_pem_x509_csr(f.read(), default_backend())

    # Identity verification step
    public_key = teacher_csr.public_key()
    try:
        public_key.verify(
            teacher_csr.signature, 
            teacher_csr.tbs_certrequest_bytes, 
            algorithm=hashes.SHA256(),
            padding=padding.PKCS1v15()
        )
        print("Public key VERIFIED!")
    except cryptography.exceptions.InvalidSignature:
        return "Invalid signature"
        raise ValueError("Invalid CSR signature")

    # Create the teacher's certificate
    teacher_cert = x509.CertificateBuilder() \
            .subject_name(teacher_csr.subject) \
            .issuer_name(ca_cert.subject) \
            .public_key(teacher_csr.public_key()) \
            .serial_number(x509.random_serial_number()) \
            .not_valid_before(datetime.datetime.utcnow()) \
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)) \
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True) \
            .sign(ca_key, cryptography.hazmat.primitives.hashes.SHA256(), default_backend())
        # Save the teacher's certificate
    with open('teachers_certificates/'+username+'_certificate.pem', 'wb') as f:
        f.write(teacher_cert.public_bytes(serialization.Encoding.PEM))

    return 'teachers_certificates/'+username+'_certificate.pem'

def get_role(cert_path):
    with open(cert_path, 'rb') as f:
        cert = x509.load_pem_x509_certificate(f.read(), default_backend())
        for ext in cert.extensions:
            if isinstance(ext.value, x509.BasicConstraints):
                return ext.value.path_length
    return None


def set_role(ca_cert, ca_key ,cert_path, new_role):
    with open(cert_path, 'rb') as f:
        cert = x509.load_pem_x509_certificate(f.read(), default_backend())
    with open(ca_cert, 'rb') as f:
        ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())
    with open(ca_key, 'rb') as f:
        ca_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())


    # Create a new certificate with the updated role
    updated_cert = x509.CertificateBuilder() \
        .subject_name(cert.subject) \
        .issuer_name(cert.issuer) \
        .public_key(cert.public_key()) \
        .serial_number(cert.serial_number) \
        .not_valid_before(cert.not_valid_before) \
        .not_valid_after(cert.not_valid_after) \
        .add_extension(x509.BasicConstraints(ca=True, path_length=new_role), critical=False) \
        .sign(ca_key, hashes.SHA256(), default_backend())
    
    # Save the updated certificate
    with open(cert_path, 'wb') as f:
        f.write(updated_cert.public_bytes(serialization.Encoding.PEM))