from flask import Flask, request

app = Flask(__name__)

print("Nombre aplicacion: ", __name__)

#Declaracion de lista para almacenar los datos
storesList = [
    {
        "name":"Tienda 1",
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
