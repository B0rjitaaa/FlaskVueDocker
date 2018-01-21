
Dockerizing Flask!
===================

For this approch we are going to test the iTunes api JSON in order to get some albums description over a index. It's a simply task to carry out. We want to show some albums as a catalogue.
----------


Back-End Application
-------------

Start with creating a new directory "backend"
Then we create the basic <kbd>run.py</kbd>:

```
# flask_web/run.py

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
```



Dockerfile
-------------
We have chosen python3 image as a base.

```
FROM python:3

WORKDIR /backend

RUN pip install --no-cache-dir Flask==0.10.1 flask_cors

ADD ./backend /backend
ADD ./dist /backend/dist
ADD run.py /backend

CMD ["python", "run.py"]
```


> **Note:**

> - <kbd>ADD</kbd> adds an entire folder to the destination folder.

> - <kbd>pip</kbd> installs  Flask 0.1.0 and flask_cors.


From now, this is our back-end server.


Front-End Application
-------------
Start with creating a new directory "frontend"
The we create a new component "Home.vue"

```
<template>
  <div class="container">
    <input v-model="artist_name" placeholder="artist name">
    <button @click="getRandom">Search albums</button>
    <div class="row marketing">
      <div class="col-lg-6" v-for="album in albums" :key="album.collectionId">
        <div class="card" style="width: 20rem; padding:10px; margin-top:10px; margin-bottom:10px">
          <img class="card-img-top" :src="album.artworkUrl100" alt="">
            <div class="card-block">
              <h4 class="card-title">{{album.collectionName}}</h4>
              <a v-bind:href="album.collectionViewUrl" class="btn btn-primary">Info</a>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      albums: '',
      artist_name: ''
    }
  },
  methods: {
    getRandom () {
      this.albums = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      const path = `http://flask_isolated:5000/api/random` + '?artist_name=' + this.artist_name.replace(/ /g, '')
      axios.get(path)
        .then(response => {
          this.albums = response.data.albums
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
```


Build the images
-------------
Now that we have to build the Dockers. Let's start in backendfolder. 
```
docker build -t flask-img/01 .
```
Then, we have to build the frontend Docker image.
```
docker build -t vue-img/01 .
```

Networking
-------------
Containers in the same network are linked to each other.

We have to create a network for those containers.
```
docker network create --driver bridge isolated_network
```

Running containers
-------------
When running the containers, you have to specify the network.
```
docker run  --net=isolated_network -p 5000:5000 --name flask_isolated flask-img/01
docker run  --net=isolated_network -p 8080:8080 --name vue_isolated vue-img/01
