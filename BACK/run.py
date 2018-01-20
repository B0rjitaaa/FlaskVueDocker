from flask import Flask, render_template, jsonify, request
from urllib.request import urlopen

import json
from random import *


from flask_cors import CORS
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/random')
def random_number():
	artist_name = request.args.get('artist_name')
	url = urlopen('https://itunes.apple.com/search?term=' + artist_name + '&entity=album&limit=6')
	res = json.loads(url.read())
	albums = res['results']
	response = {
		'randomNumber': randint(1, 100),
		'albums': albums
	}
	return jsonify(response)

@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')


