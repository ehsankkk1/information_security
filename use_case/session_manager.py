"""
 Session Manager, to save and deal with temporary data on memory for client-server session.
 like :
 1] save session keys
 2] save public keys

 create instance for each side
"""
class SessionManager():
    
    def __init__(self):
        self.data = {}

    
    def set(self, key, value):
        self.data[key] = value

    
    def get(self, key):
        return self.data.get(key, None)

    
    def all(self):
        return self.data.copy()

    
    def remove(self, key):
        if key in self.data:
            del self.data[key]
    
    def clear_storage(self):
        self.data.clear()