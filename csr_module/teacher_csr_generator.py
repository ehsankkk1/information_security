from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend

class CSRGenerator:
    def __init__(self, private_key_path='csr_module/teacher_private.key', csr_folder='csr_module/'):
        self.private_key_path = private_key_path
        self.csr_folder = csr_folder

    def generate_csr(self, teacher_name):
        # Load the private key
        with open(self.private_key_path, 'rb') as private_key_file:
            private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password=None,
                backend=default_backend()
            )

        # Generate a CSR
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "SY"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Damascus"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Damascus University"),
            x509.NameAttribute(NameOID.COMMON_NAME, teacher_name),
        ])

        csr_builder = x509.CertificateSigningRequestBuilder().subject_name(subject)



        csr = csr_builder.sign(
            private_key, algorithm=hashes.SHA256(), backend=default_backend()
        )

        # Save CSR to a file
        csr_filename = f'{teacher_name}_csr.pem'
        csr_filepath = f'{self.csr_folder}{csr_filename}'

        with open(csr_filepath, 'wb') as csr_file:
            csr_pem = csr.public_bytes(serialization.Encoding.PEM)
            csr_file.write(csr_pem)

        # Return CSR content and file path
        return csr_pem.decode('utf-8'), csr_filepath
