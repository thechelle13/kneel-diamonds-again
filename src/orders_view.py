import json
from nss_handler import status
from repository import db_get_all, db_get_single,db_create,db_delete,db_update

class OrderView():
    
    
    def get_expanded(self, handler, pk, expand_params):
        if pk != 0:
            # Original SQL query for fetching an order
            sql = """
            SELECT o.id, o.metalId, o.sizeId, o.styleId
            FROM orders o
            WHERE o.id = ?
            """
            query_results = db_get_single(sql, pk)

            if query_results:
                order_data = dict(query_results)
                expanded_response = self.expand_related_resources(order_data, expand_params)
                return handler.response(json.dumps(expanded_response), status.HTTP_200_SUCCESS.value)
            else:
                return "Error", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        else:
            # Original SQL query for fetching all orders
            sql = """
            SELECT o.id, o.metalId, o.sizeId, o.styleId
            FROM orders o
            """
            query_results = db_get_all(sql)

            expanded_orders = []

            for row in query_results:
                order_data = dict(row)
                expanded_response = self.expand_related_resources(order_data, expand_params)
                expanded_orders.append(expanded_response)

            if expanded_orders:
                return handler.response(json.dumps(expanded_orders), status.HTTP_200_SUCCESS.value)
            else:
                return handler.response("Error", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def expand_related_resources(self, order_data, expand_params):
        expanded_response = {
            "id": order_data["id"],
            "metalId": order_data["metalId"],
            "sizeId": order_data["sizeId"],
            "styleId": order_data["styleId"]
        }

        for param in expand_params:
            if param == 'metal':
                # Fetch and add the 'metal' resource
                metal_data = self.get_expanded_metal(order_data["metalId"])
                expanded_response["metal"] = metal_data
            elif param == 'size':
                # Fetch and add the 'size' resource
                size_data = self.get_expanded_size(order_data["sizeId"])
                expanded_response["size"] = size_data
            elif param == 'style':
                # Fetch and add the 'style' resource
                style_data = self.get_expanded_style(order_data["styleId"])
                expanded_response["style"] = style_data

        return expanded_response

    def get_expanded_metal(self, metal_id):
        # Original SQL query to fetch metal data
        sql = "SELECT id, metal, price FROM metals WHERE id = ?"
        query_results = db_get_single(sql, metal_id)
        return dict(query_results)

    def get_expanded_size(self, size_id):
        # Original SQL query to fetch size data
        sql = "SELECT id, carets, price FROM sizes WHERE id = ?"
        query_results = db_get_single(sql, size_id)
        return dict(query_results)

    def get_expanded_style(self, style_id):
        # Original SQL query to fetch style data
        sql = "SELECT id, style, price FROM styles WHERE id = ?"
        query_results = db_get_single(sql, style_id)
        return dict(query_results)

    
    
    
    
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