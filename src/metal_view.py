import json
from nss_handler import status

class MatalView():
    
    def get(self, handler):
        
        return handler.response()