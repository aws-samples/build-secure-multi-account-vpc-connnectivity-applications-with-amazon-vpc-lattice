from flask import Flask, render_template, jsonify, make_response
import os
import sys
import requests

if os.getenv("LATTICEURL") is None:
    print(f'[ERROR] no Lambda URL configured inside Pod')
    sys.exit(1)
else: 
    print(os.getenv("LATTICEURL"))

    app = Flask(__name__)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def home(path):
        try:
            output = requests.get(os.getenv("LATTICEURL")).text
        except OSError as e:
            return("Something went wrong, check Lattice URL")
        data = {'message': output, 'code': 'SUCCESS'}
        return make_response(jsonify(data), 200)
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=8081)