import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import storesList

blp = Blueprint("stores", __name__, description="Operaciones en las tiendas")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return storesList[store_id]
        except KeyError:
            abort(404, message="Tienda no encontrada")

    def delete(self, store_id):
        try:
            del storesList[store_id]
            return {"message": "Tienda Borrada"}
        except KeyError:
            abort(404, message="Tienda no encontrada")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(storesList.values())}

    def post(self):
        try:
            # Obtenemos el dato que nos ha enviado el cliente
            store_data = request.get_json()
            if "name" not in store_data:
                abort(
                    400,
                    message="Bad Request. Ensure 'name' is included in the JSON payload.",
                )
            # Comporbar si la tienda existe
            for store in storesList.values():
                if store_data["name"] == store["name"]:
                    abort(
                        400,
                        message=f"La tienda ya existe"
                    )

            # Creamos el identificador universal
            store_id = uuid.uuid4().hex
            # Montamos la nueva tienda
            new_store = {**store_data, "id": store_id}
            # Agregamos el nuevo elemento a la lista
            storesList[store_id] = new_store
            # Retornamos el nuevo elemento creado
            return new_store, 201
        except Exception as ex:
            abort(404, message=f"{ex},{TypeError}")