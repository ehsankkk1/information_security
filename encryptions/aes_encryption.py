import base64
import os
from cryptography.fernet import Fernet
from encryptions.encryption import EncryptionClass

class AesEncryption (EncryptionClass) :

    def __init__(self, key):
        self.secret_Key = key
        self.cipher_suite = Fernet(self.secret_Key)

    def encrypt(self, messageVar):
        return self.cipher_suite.encrypt(messageVar.encode())

    def decrypt(self, encrypted_message):
        return self.cipher_suite.decrypt(encrypted_message).decode()
    
