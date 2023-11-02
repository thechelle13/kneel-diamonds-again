import json
from nss_handler import status
from repository import db_get_all, db_get_single,db_create,db_delete,db_update

class StyleView():
    
    def get(self, handler, pk):
        if pk != 0:
            sql = """
            SELECT
                s.id,
                s.style,
                s.price
            FROM styles s
            WHERE s.id = ?
            """
            query_results = db_get_single(sql, pk)
            serialized_style = json.dumps(dict(query_results))

            return handler.response(serialized_style, status.HTTP_200_SUCCESS.value)
        else:

            query_results = db_get_all("SELECT s.id, s.style,s.price FROM styles s")
            styles = [dict(row) for row in query_results]
            serialized_styles = json.dumps(styles)

            return handler.response(serialized_styles, status.HTTP_200_SUCCESS.value)
        

        
    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM styles WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, style_data, pk):
        sql = """
        UPDATE styles
        SET
            style = ?,
            style_id = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (style_data['style'], style_data['price'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def insert(self, handler, style_data):
        sql = """
        INSERT INTO styles 
        VALUES(null, ?,?)
                
        """
                
        new_item = db_create(sql,(style_data['style'], style_data['price']))

        if new_item is not None:
            response_data =  {
                "id" : new_item,
                "style": style_data ['style'],
                "price": style_data ['price']

            }
        
        if new_item > 0:
            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("BAD REQUEST", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)