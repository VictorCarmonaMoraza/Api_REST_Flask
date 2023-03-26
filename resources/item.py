import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import itemsList


blp = Blueprint("items", __name__, description="Operaciones en los articulos")


@blp.route("/item/<string:item_id>")
class Store(MethodView):
    def get(self, item_id):
        try:
            return itemsList[item_id]
        except KeyError:
            abort(404, message="Articulo no encontrada")

    def delete(self, item_id):
        try:
            del itemsList[item_id]
            return {"message": "Articulo Borrada"}
        except KeyError:
            abort(404, message="Articulo no encontrada")

    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message="Bad Request. Ensure 'price', and 'name' are included in the JSON payload."
            )
        try:
            item = itemsList[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(
                400,
                message="Articulo no encontrado"
            )


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(itemsList.values())}

    def post(self):
        item_data = request.get_json()
    # Validaciones de los parametros que pasamos desde el Body de Postman
        if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message="Bad Request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload.",
            )
    # Validacion para que no podamos añadir el mismo elemento dos veces
        for item in itemsList.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="El articulo ya existe")

        if item_data["store_id"] not in itemsList:
            abort(404, message="Tienda no encontrada")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        itemsList[item_id] = item

        return item, 201
