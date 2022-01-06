"""
MVC (Model - View - Controller) приложения удобно рассматривать с контроллеров. 
Например, надо разобраться, чо происходит, если кто-то кидает запрос POST /add_client
Находишь контроллер, который обрабатывает этот URL и этот HTTP глагол, и смотришь, чо там происходит

Контроллеры обрабатывают запросы с фронта, так что считай тут находятся именно они
View тут это шаблоны (render_template)
"""

from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_app.models.models import *
from flask_app.repository.repository import *

app = Flask(__name__)
counter = 0

CLIENT_REP = ClientRepository()
ADDRESS_REP = AddressRepository()
CLIENT_ADDRESS_REP = ClientAddressesRepository()
CONTRACT_REP = ContractRepository()

@app.route('/', methods=["GET"])
def hello_world():
    data = CLIENT_REP.get_all()
    return render_template('index.html', data=data)

@app.route('/add_client', methods=["GET", "POST"])
def add_client():
    if request.method == "GET":
        return render_template('create_client.html')
    if request.method == "POST":
        number = request.form.get('number')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        CLIENT_REP.save(Client(number, first_name, last_name))
        return redirect('/')

@app.route('/delete_client', methods=["POST"])
def delete_client():
    user_id = request.args.get("user_id")
    CLIENT_REP.delete(user_id)
    return redirect('/')

@app.route('/show_addresses', methods=["GET"])
def show_addresses():
    user_id = request.args.get("user_id")
    user = CLIENT_REP.get_by_id(user_id)
    addresses = CLIENT_ADDRESS_REP.get_addresses_by_client_id(user_id)
    print(f"addressess {addresses}")
    return render_template('addresses.html', data=[user, addresses])

@app.route('/add_address', methods=["GET", "POST"])
def add_address():
    user_id = request.args.get("user_id")
    if request.method == "GET":
        return render_template('add_address.html')
    if request.method == "POST":
        address = request.form.get('address')
        CLIENT_REP.add_address(CLIENT_REP.get_by_id(user_id), Address(address))
        return redirect('/')

@app.route('/delete_address', methods=["POST"])
def delete_address():
    address_id = request.args.get("address_id")
    ADDRESS_REP.delete(address_id)
    return redirect('/')

@app.route('/show_contracts', methods=["GET"])
def show_contracts():
    user_id = request.args.get("user_id")
    user = CLIENT_REP.get_by_id(user_id)
    contracts = CONTRACT_REP.get_by_client_id(user_id)
    return render_template('contracts.html', data=[user, contracts])

@app.route('/add_contract', methods=["GET", "POST"])
def add_contract():
    user_id = request.args.get("user_id")
    if request.method == "GET":
        user: Client = CLIENT_REP.get_by_id(user_id)
        addresses: list[Address] = CLIENT_REP.get_addresses(user_id)
        return render_template('add_contract.html', data=[user, addresses])
    if request.method == "POST":
        print(request.form)
        contract = Contract(
            CLIENT_REP.get_by_id(request.form.get("client")),
            ADDRESS_REP.get_by_id(request.form.get("address")),
            request.form.get("date"),
            request.form.get("status"),
            request.form.get("description"),
            request.form.get("document"),
            request.form.get("sum")
        )
        CONTRACT_REP.save(contract)
        return redirect('/')

@app.route('/delete_contract', methods=["POST"])
def delete_contract():
    contract_id = request.args.get("contract_id")
    CONTRACT_REP.delete(contract_id)
    return redirect('/')   