from flask import Flask

app = Flask(__name__)

print("Nombre aplicacion: ", __name__)

#Declaracion de lista para almacenar los datos
storesList = [
    {
        "name":"Mi tienda",
        "items":[
            {
                "name": "Silla",
                "price": 15.99
            }
        ]
    }
]

"""sumary_line
Devolvera la lista de stores --->storesList
Keyword arguments:
argument -- description
Return: return_description
"""

@app.get("/store")
def get_stores():
    return {"stores": storesList}