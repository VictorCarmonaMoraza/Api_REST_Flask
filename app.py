import uuid
from flask import Flask, request
from db import itemsList, storesList

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
        return {"message": "Tienda no encontrada"}, 404


#Creamos una tienda
@app.post("/store")     #http://127.0.0.1:5000/store
def create_store():
    try:
        # Obtenemos el dato que nos ha enviado el cliente
        store_data = request.get_json()
        # Creamos el identificador universal
        store_id = uuid.uid4().hex
        #Montamos la nueva tienda
        new_store = {**store_data, "id": store_id}
        #Agregamos el nuevo elemento a la lista
        storesList[store_id] = new_store
        #Retornamos el nuevo elemento creado
        return new_store, 201
    except Exception as ex:
        print(f'Ocurrio un error {ex},{TypeError}')

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
        return {"message": "Articulo no encontrado"}, 404


#Agregamos elementos a nuestra tienda
@app.post("/item")
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in storesList:
        return {"message": "Tienda no encontrada"}, 404

    item_id = uuid.uuid4().hex
    item ={**item_data, "id": item_id}
    itemsList[item_id] = item

    return item, 201


#endregion Articulos