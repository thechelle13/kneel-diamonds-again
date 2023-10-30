import json
from nss_handler import status

class OrderView():
    
    def get(self, handler):
        
        return handler.response()