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
</script>
