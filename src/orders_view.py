import json
from nss_handler import status
from repository import db_get_all, db_get_single,db_create,db_delete,db_update

class OrderView():
    
    
    def get_expanded(self, handler, pk):
        if pk != 0:
            sql = """
            SELECT o.id, o.metalId, o.sizeId, o.sytleId AS order_data
            FROM orders o
            LEFT JOIN orders o ON o.ordersId = o.id
            WHERE o.id = ?
            """
            query_results = db_get_single(sql, pk)

            if query_results:
                order_data = dict(query_results)
                response = {
                    "id": order_data["id"],
                    "metal_id": order_data["metal_id"],
                    "size_id": order_data["size_id"],
                    "style_id": order_data["style_id"]
                }
                return handler.response(json.dumps(response), status.HTTP_200_SUCCESS.value)
            else:
                return "Error", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        else:
            sql = """
            SELECT o.id, o.metalId, o.sizeId, o.styleId AS order_data
            FROM Orders o
            LEFT JOIN Orders o ON o.id = o.id
            """
            query_results = db_get_all(sql)

            expanded_orders = []

            for row in query_results:
                order_data = dict(row)
                response = {
                    "id": order_data["id"],
                    "metal_id": order_data["metal_id"],
                    "size_id": order_data["size_id"],
                    "style_id": order_data["style_id"]
                }
                expanded_orders.append(response)

            if expanded_orders:
                return handler.response(json.dumps(expanded_orders), status.HTTP_200_SUCCESS.value)
            else:
                return handler.response("Error", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
    
    
    
    
    def get(self, handler, pk):
        if pk != 0:
            sql = "SELECT o.id, o.metalId, o.sizeId, styleId FROM orders o WHERE o.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_order = json.dumps(dict(query_results))

            return handler.response(serialized_order, status.HTTP_200_SUCCESS.value)
        else:

            sql = "SELECT o.id, o.metalId, o.styleId, o.sizeId FROM orders o"
            query_results = db_get_all(sql)
            orders = [dict(row) for row in query_results]
            serialized_orders = json.dumps(orders)

            return handler.response(serialized_orders, status.HTTP_200_SUCCESS.value)
        
    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM orders WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, order_data, pk):
        sql = """
        UPDATE orders
        SET
            metalId = ?,
            sizeId = ?,
            styleId = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (order_data['order'], order_data['price'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def insert(self, handler, order_data):
        sql = """
        INSERT INTO orders 
        VALUES(null, ?,?)
                
        """
                
        new_item = db_create(sql,(order_data['metalId'], order_data['styleId']))

        if new_item is not None:
            response_data =  {
                "id" : new_item,
                "metalId": order_data ['metalId'],
                "styleId": order_data ['styleId'],
                "sizeId": order_data ['sizeId']

            }
        
        if new_item > 0:
            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("BAD REQUEST", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)