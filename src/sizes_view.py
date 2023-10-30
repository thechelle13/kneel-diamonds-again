import json
from nss_handler import status

class SizeView():
    
    def get(self, handler):
        
        return handler.response()