import rsa
import json
import os

"""
 AssymetricEncryptionManager, to generate and deal with Assymetric Encryption public-private pair,
 can serve both server and client, stores public-private pair in a file for each side
"""

class AssymetricEncryptionManager():
   

    def __init__(self):
        self.path = './keys/'
        self.file_name = '/keys.json'
        self.user = 'user'  
        self.keys = None
        self.public_key = None
        self.private_key = None


    def for_server(self):
        self.role = 'server'
        self.user = 'server'
        self.path = self.path + self.user + self.file_name

        return self

    def for_client(self, user):
        self.role = 'client'
        self.user = user
        self.path = self.path + 'client/'
        self.path = self.path + self.user + self.file_name
        return self

    def generate_keys(self):
        self.public_key, self.private_key = rsa.newkeys(512)
        self.keys = {'public': self.public_key, 'private': self.private_key}
        return self


    def generate(self):
        self.generate_keys().save()


    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({
                'public': self.public_key.save_pkcs1().decode(),
                'private': self.private_key.save_pkcs1().decode()
                }, f)

        return self


    def get(self):
        with open(self.path, 'r') as f:
                keys_data = json.load(f)
        self.public_key = keys_data['public']
        self.private_key = keys_data['private']
        return self

    
    def get_pair(self):
      return {
         'public' : self.public_key,
         'private' : self.private_key
        }
    
    def get_public_key(self, type = 'text'):
        if type == 'object':
          return rsa.PublicKey.load_pkcs1(self.public_key)
        elif type == 'DER':
          return self.public_key   
        else:
          return self.public_key

    def get_private_key(self, type = 'text'):
        if type == 'object':
          return rsa.PublicKey.load_pkcs1(self.private_key)
        else:
          return self.private_key