import json
from nss_handler import status
from repository import db_get_all, db_get_single,db_create,db_delete,db_update

class MetalView():
    
    def get(self, handler, pk):
        if pk != 0:
            sql = "SELECT m.id, m.metal, m.price FROM metals m WHERE m.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_metal = json.dumps(dict(query_results))

            return handler.response(serialized_metal, status.HTTP_200_SUCCESS.value)
        else:

            sql = "SELECT m.id, m.metal, m.price FROM metals m"
            query_results = db_get_all(sql)
            metals = [dict(row) for row in query_results]
            serialized_metals = json.dumps(metals)

            return handler.response(serialized_metals, status.HTTP_200_SUCCESS.value)
        
    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM metals WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, metal_data, pk):
        sql = """
        UPDATE Ship
        SET
            metal = ?,
            price = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (metal_data['metal'], metal_data['price'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def insert(self, handler, metal_data):
        sql = """
        INSERT INTO metals 
        VALUES(null, ?,?)
                
        """
                
        new_item = db_create(sql,(metal_data['metal'], metal_data['price']))

        if new_item is not None:
            response_data =  {
                "id" : new_item,
                "metal": metal_data ['metal'],
                "price": metal_data ['price']

            }
        
        if new_item > 0:
            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("BAD REQUEST", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)