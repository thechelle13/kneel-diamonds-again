import json
from nss_handler import status

class OrderView():
    
    def get(self, handler,url):
        # if url["pk"]:
            
            # serialized_orders = json.dumps()    
        
        return handler.response("serialized_orders",status.HTTP_200_SUCCESS.value)
    
    def delete(self, handler, pk):
        return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
    
    def update(self, handler, pk):
        return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value) 