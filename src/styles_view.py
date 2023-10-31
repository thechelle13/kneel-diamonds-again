import json
from nss_handler import status

class StyleView():
    
    def get(self, handler):
        
        return handler.response()