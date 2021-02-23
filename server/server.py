#!/usr/bin/env python
from flask import Flask, request, make_response
from service_config import SERVER_CONFIG, BASE_CONFIG
from service import ServiceErrors, service
from db_provider import DBProvider

app = Flask(__name__, static_folder="static", static_url_path="")
app.url_map.strict_slashes = False
app.config["BASE_URL"] = BASE_CONFIG.get('BASE_URL')

def main():
    app.run(**SERVER_CONFIG)

@app.errorhandler(Exception)
def error_handler(error):
    return {'error': str(error)}, 500

@app.route(app.config['BASE_URL'] + '/upload', methods=["POST"])
def add_packing_list():
    """Получение от клиента товарной накладной в xls"""
    try:
        response = service.add_packing_list(data=request.get_data())
        code = 200 if response.get('status') == 'ok' else 500
        return make_response(response, code)
    except ServiceErrors as error:
        return make_response({'status': error.message}, 500)

@app.route(app.config['BASE_URL'] + '/warehouse', methods=["GET"])
def get_warehouse_list():
    warehouse = service.get_warehouse_list()
    code = 200 if warehouse else 404
    return make_response({'warehouse': warehouse}, code)

@app.route(app.config['BASE_URL'] + '/remote', methods=["GET"])
def get_remote_list():
    remote = service.get_remote_list()
    code = 200 if remote else 404
    return make_response({'remote': remote}, code)

@app.route(app.config['BASE_URL'] + '/checkout', methods=['GET'])
def checkout():
    service.checkout(request.args.getlist('destination'))
    return 'ok'

@app.route(app.config['BASE_URL'] + '/checkout_list', methods=['GET'])
def checkout_list():
    checkout_list = service.get_checkout_list()
    code = 200 if checkout_list else 404
    return make_response({'checkout_list': checkout_list}, code)
        
if __name__ == '__main__':
    main()
