from flask import Flask, render_template, jsonify, make_response
import os
import sys
import requests
import json

if os.getenv("LAMBDAURL") or os.getenv("BACKENDURL") is None:
    print(f'[ERROR] no Lattice URLs configured inside Pod')
    sys.exit(1)
else: 
    app = Flask(__name__, template_folder='./templates')
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def home(path): #/backend /lambda
        lambda_url = "{}/{}".format(os.getenv("LAMBDAURL"), path)
        backend_url = "{}/{}".format(os.getenv("BACKENDURL"), path)
        if path == "backend":
            print(backend_url) #debug
            try:
                backend_call = requests.get(backend_url).text
                region = json.loads(backend_call)
            except OSError as e:
                return("Something went wrong, check Lattice URL")
            return render_template("index.html", icon = 'static/images/eks.png', message = "Powered by:", aws_reg = region['message'] )
        elif path == "lambda":
            print(lambda_url) #debug
            try:
                region = requests.get(lambda_url).text
            except OSError as e:
                return("Something went wrong, check Lattice URL")
            return render_template("index.html", icon = 'static/images/lambda.png', message = "Powered by:", aws_reg = region)
        else:
            return("Please specify /backend /lambda path")
        
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=8080)