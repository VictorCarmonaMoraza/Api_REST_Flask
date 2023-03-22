import uuid
from flask import Flask, request
from db import itemsList, storesList
from flask_smorest import abort

app = Flask(__name__)

print("Nombre aplicacion: ", __name__)


#region Store

#Obtenemos todas las tiendas de la lista
@app.get("/store")     #http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(storesList.values())}


#Obtener una tienda especifica y sus articulos
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return storesList[store_id]
    except KeyError:
        abort(404, message="Tienda no encontrada")


#Creamos una tienda
@app.post("/store")     #http://127.0.0.1:5000/store
def create_store():
    try:
        # Obtenemos el dato que nos ha enviado el cliente
        store_data = request.get_json()
        if "name" not in store_data:
            abort(
                400,
                message = "Bad Request. Ensure 'name' is included in the JSON payload.",
            )
        #Comporbar si la tienda existe
        for store in storesList.values():
            if store_data["name"] == store["name"]:
                abort(
                    400,
                    message = f"La tienda ya existe"
                )

        # Creamos el identificador universal
        store_id = uuid.uuid4().hex
        #Montamos la nueva tienda
        new_store = {**store_data, "id": store_id}
        #Agregamos el nuevo elemento a la lista
        storesList[store_id] = new_store
        #Retornamos el nuevo elemento creado
        return new_store, 201
    except Exception as ex:
        abort(404, message =f"{ex},{TypeError}")

#endregion Store


#region Articulos

# Obtiene todos los articulos
@app.get("/item")
def get_all_items():
    return {"items": list(itemsList.values())}


# Obtiene un articulo por su id
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return itemsList[item_id]
    except:
        abort(404, message= "Articulo no encontrado")


#Agregamos elementos a nuestra tienda
@app.post("/item")
def create_item():
    item_data = request.get_json()
    #Validaciones de los parametros que pasamos desde el Body de Postman
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message = "Bad Request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload.",
        )
    # Validacion para que no podamos añadir el mismo elemento dos veces
    for item in itemsList.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message = "El articulo ya existe")

    if item_data["store_id"] not in storesList:
        abort(404, message ="Tienda no encontrada")

    item_id = uuid.uuid4().hex
    item ={**item_data, "id": item_id}
    itemsList[item_id] = item

    return item, 201


#endregion Articulos