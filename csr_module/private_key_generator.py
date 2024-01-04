from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class PrivateKeyGenerator:
    def __init__(self, private_key_folder='csr_module/'):
        self.private_key_folder = private_key_folder

    def generate_private_key(self, teacher_name):
        # Generate a private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Save private key to a file
        private_key_filename = f'{teacher_name}_private.key'
        private_key_path = f'{self.private_key_folder}{private_key_filename}'

        with open(private_key_path, 'wb') as private_key_file:
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            private_key_file.write(private_key_pem)

        # Return the private key path
        return private_key_path
