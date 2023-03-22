from flask import Flask, request

app = Flask(__name__)

print("Nombre aplicacion: ", __name__)

#Declaracion de lista para almacenar los datos
storesList = [
    {
        "name":"Tienda_1",
        "items":[
            {
                "name": "Silla",
                "price": 15.99
            }
        ]
    }
]


#Obtenemos todas las tiendas de la lista
@app.get("/store")     #http://127.0.0.1:5000/store
def get_stores():
    return {"stores": storesList}


#Creamos una tienda
@app.post("/store")     #http://127.0.0.1:5000/store
def create_store():
    try:
        #Obtenemos el dato que nos ha enviado el cliente
        request_data = request.get_json()
        #Montamos la nueva tienda
        new_store = {'name':request_data["name"], "items":[]}
        #Agregamos el nuevo elemento a la lista
        storesList.append(new_store)
        #Retornamos el nuevo elemento creado
        return new_store, 201
    except Exception as ex:
        print(f'Ocurrio un error {ex},{TypeError}')


#Agregamos elementos a nuestra tienda
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in storesList:
        if store["name"] == name:
            new_item = {"name":request_data["name"], "price":request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message":"Store not found"}, 404



#Obtener una tienda especifica y sus articulos
@app.get("/store/<string:name>")
def get_store(name):
    #Recorremos la lista
    for store in storesList:
        if store["name"] == name:
            return store
    return {"message": "Tienda no encontrada"}, 404


#Obtener los articulos de una tienda
@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    #Recorremos las lista de tiendas
    for store in storesList:
        if store["name"] == name:
            #Retornamos los articulos de la tienda
            return {"items":store["items"]}
    return {"message":"Tienda no encontrada"}, 404