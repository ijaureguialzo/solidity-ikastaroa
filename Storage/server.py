from flask import Flask, render_template, request
from web3 import Web3

app = Flask(__name__, template_folder='www', static_url_path='/static')

# Address del contrato con el que vamos a interactuar
contract_addr = "XXXXX"  # CAMBIA ESTE VALOR POR EL ADDRESS DE TU CONTRATO

# Cadena de conexión con Ganache
provider = "http://127.0.0.1:7545"  # REVISA QUE EL PUERTO DE CONEXIÓN A GANACHE ES CORRECTO

# Guardamos en una variable abi, el abi del contrato
with open("static/abi/Storage.abi", "r") as f:
    abi = f.read()


# Ruta de entrada a la aplicación
@app.route("/")
def hello_world():
    return render_template("index.html")


# Ruta para ver el valor almacenado en el
@app.route("/ver/")
def ver():
    # Conexión con Ganache
    web3 = Web3(Web3.HTTPProvider(provider))
    if web3.is_connected():
        # Nos conectamos con el contrato utilizando su abi y address
        contract = web3.eth.contract(abi=abi, address=contract_addr)

        # Llamamos a la funcion retrieve del contrato
        # En este caso es una función que solo recibe un valor del contrato sin cambiar su estado
        # y por eso llamamos a la función call
        num = contract.functions.retrieve().call()

    # Lanzamos la página web en la que vamos a mostrar el resultado y le pasamos el resultado de la función retrieve
    return render_template("ver.html", num=num, contract_addr=contract_addr)


@app.get('/escribir/')
def get_escribir():
    return render_template("escribir.html")


@app.post("/escribir/")
def post_escribir():
    # Recogemos el address que envía el número al contrato y la convertimos al formato checksum necesario para interactuar con la blockchain
    addr = request.form.get('addr')
    addr = Web3.to_checksum_address(addr)
    # Recogemos el número a guardar en la blockchain y lo pasamos a entero
    num = int(request.form.get('num'))
    # LA variable error nos va a permitir saber si hemos recibido el address correctamente o no.
    error = True
    if addr:
        error = False
        # Establecemos la conexión con la Blockchain
        web3 = Web3(Web3.HTTPProvider(provider))

        if web3.is_connected():
            # Nos conectamos con el contrato utilizando su abi y address
            contract = web3.eth.contract(abi=abi, address=contract_addr)
            # Llamamos a la funcion store del contrato
            # En este caso como vamos a cambiar el estado del contrato tenemos que ejecutar la función transact
            # y pasarle el address que hace la llamada a la función
            contract.functions.store(num).transact({"from": addr})

    return render_template("num_escrito.html", error=error, addr=addr)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
