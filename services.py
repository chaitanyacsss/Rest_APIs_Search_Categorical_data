import json

from flask import Flask, request, jsonify

from data_loader import *

app = Flask(__name__)

@app.route('/api/products/autocomplete', methods=['POST'])
def autocomplete_service():
    try:
        input_json = request.get_json(force=True)
        print('data from client:', input_json)
        return json.dumps(autocomplete(input_json['type'], input_json['prefix']))
    except Exception as e:
        print(e)
        return jsonify(e.__dict__)


@app.route('/api/products/search', methods=['POST'])
def search_service():
    try:
        input_json = request.get_json(force=True)
        print('data from client:', input_json)
        return json.dumps(search_by_conditions(input_json['conditions'], input_json['pagination']))
    except Exception as e:
        print(e)
        return jsonify(e.__dict__)


@app.route('/api/products/keywords', methods=['POST'])
def keyword_frequency_service():
    try:
        input_json = request.get_json(force=True)
        print('data from client:', input_json)
        return json.dumps(get_frequencies(input_json['keywords']))
    except Exception as e:
        print(e)
        return jsonify(e.__dict__)


if __name__ == '__main__':
    app.run(debug=True, port=8088)
