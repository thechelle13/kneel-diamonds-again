import json
from nss_handler import status

class TypeView():
    
    def get(self, handler):
        
        return handler.response()