import os

from flask import Flask, render_template, request
from web3 import Web3

app = Flask(__name__, template_folder='www', static_url_path='/static')

# Address del contrato con el que vamos a interactuar
contract_addr = os.environ.get("CONTRACT_ADDR")

# Cadena de conexión con Ganache
provider = os.environ.get("PROVIDER")

# Guardamos en una variable abi, el abi del contrato
with open("static/abi/AddressStorage.abi", "r") as f:
    abi = f.read()


# Ruta de entrada a la aplicación
@app.route("/")
def hello_world():
    return render_template("index.html")


@app.get("/ver/")
def get_ver():
    return render_template("formulario.html")


@app.post("/ver/")
def post_ver():
    web3 = Web3(Web3.HTTPProvider(provider))
    if web3.is_connected():
        contract = web3.eth.contract(abi=abi, address=contract_addr)
        direccion = request.form.get('direccion')
        direccion = Web3.to_checksum_address(direccion)
        saldo = contract.functions.retrieve(direccion).call()
    return render_template("ver.html", saldo=saldo, contract_addr=contract_addr, direccion=direccion)


@app.get('/escribir/')
def get_escribir():
    return render_template("escribir.html")


@app.post("/escribir/")
def post_escribir():
    direccion_origen = Web3.to_checksum_address(request.form.get('direccion_origen'))
    direccion_destino = Web3.to_checksum_address(request.form.get('direccion_destino'))
    numero = int(request.form.get('numero'))

    error = True
    if direccion_origen:
        error = False
        # Establecemos la conexión con la Blockchain
        web3 = Web3(Web3.HTTPProvider(provider))

        if web3.is_connected():
            # Nos conectamos con el contrato utilizando su abi y address
            contract = web3.eth.contract(abi=abi, address=contract_addr)
            # Llamamos a la funcion store del contrato
            # En este caso como vamos a cambiar el estado del contrato tenemos que ejecutar la función transact
            # y pasarle el address que hace la llamada a la función
            contract.functions.store(direccion_destino, numero).transact({"from": direccion_origen})

    return render_template("num_escrito.html", error=error, direccion_origen=direccion_origen,
                           direccion_destino=direccion_destino, numero=numero)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
