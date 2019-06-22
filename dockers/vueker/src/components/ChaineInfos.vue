<template>
  <div class="container-perso">
    <div :class="sx.header">
       <b-row  class="my-3">
          <b-col style="margin: auto; color: #3f51b5;" sm="2">
          </b-col>
          <b-col sm="10">
            <div style="display: flex;">
              <div :class="sx.logo">
                <div :class="sx.user_logo"><font-awesome-icon icon="user" style="margin:auto;"/></div>
              </div>
              <div style="margin: auto; margin-left: 10px">
                <div :class="sx.title"> {{ user.username }}  <span> {{ user.pseudo }} </span></div>
                <div> A rejoint Youtube le {{ user.created_at | moment}}</div>
              </div>
            </div>
          </b-col>
        </b-row>
    </div>
    <b-card bg-variant="transparent" style="height: 100vh;" no-body>
      <b-tabs pills card vertical nav-wrapper-class="col-2" active-nav-item-class="font-weight-bold">
        <b-tab title="Mes vidéos" active>
          <div v-if="isLoaded" :class="sx.list" style="padding-bottom: 100px;">
            <div v-for="video in videos" :key="video.id">
              <div v-if="video.enabled == 1 || user.id == currentUser.id" :class="sx.video">
                <b-card
                  bg-variant="transparent"
                  text-variant="white"
                  img-src="https://picsum.photos/600/300/?image=25"
                  img-top
                  style="max-width: 20rem;"
                  class="mb-2"
                  :class="sx.clickable"
                  @click="seeVideo(video.id)"
                >
                  <div class="notOnline" v-if="video.enabled == 0">
                    <span>Cette vidéo n'est pas en ligne, seul vous pouvez la voir</span>
                  </div>
                    <b-card-text style="width: 200px;"> {{ video.name }} </b-card-text>
                    <b-card-text class="small text-white" >{{ video.view }} vues  •  {{ video.created_at | moment}}</b-card-text>
                </b-card>
                <div  v-if="user.id == currentUser.id" :class="sx.trash">
                  <span class="deleteVideo" @click="deleteVideo(video.id)"><font-awesome-icon icon="trash-alt"/></span>
                </div>
              </div>
            </div>
          </div>
          <div v-else :class="sx.list" class="d-flex justify-content-center mb-3" style="height: 100%">
            <b-spinner type="grow" label="Spinning" style="width: 3rem; height: 3rem; margin: auto; color:#f44336"></b-spinner>
            <strong style="margin-left: 0">Loading...</strong>
          </div>
        </b-tab>
        <b-tab title="Mes commentaires" >
          <b-card-text>Mes commentaires</b-card-text>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isLoaded: false,

      videos: [],
      comments: [],
      user: []
    }
  },

  mounted () {
    if (this.$store.getters.userInfo) {
      try {
        this.currentUser = JSON.parse(this.$store.getters.userInfo)
      } catch(e) {
        this.currentUser = this.$store.getters.userInfo
      }
    }

    this.getUser()
    this.getVideosByUser()
    this.getComments()
    // this.updateIndexES()
  },

  methods: {
    getVideosByUser() {
      this.isLoaded = false

      this.$http.get('user/' + this.$route.params.id + '/videos').then(response => {
        // get data
        this.videos = response.data.data
        this.isLoaded = true
      }, (response) => {
        // error callback
        console.log('erreur', response)
      })
    },

    getComments() {
      this.$http.get('video/' + this.$route.params.id + '/comments').then(response => {
        // get data
        this.comments = response.data.data
      }, (response) => {
        // error callback
        console.log('erreur comments', response)
      })
    },

    getUserById() {
      this.$http.get('user/' + this.$route.params.id).then(response => {
        this.user = response.data.data
      }, (response) => {
        console.log('erreur', response)
      })
    },

    getUser() {
      if (this.currentUser) {
        if (this.$route.params.id === this.currentUser.id) {
          this.user = this.currentUser
        } else {
          this.getUserById()
        }
      } else {
        this.getUserById()
      }
    },

    seeVideo(videoId) {
      console.log('seeVideo', videoId)
      this.$router.push({ name: 'VideoInfos', params: { id: videoId }})
    },

    deleteVideo (id) {
      if (confirm('Voulez-vous vraiment supprimer votre video, Vous ne pourrez plus la récupérer.')) {
        this.$http.delete('video/' + id, {headers: {'Authorization': localStorage.getItem('Authorization')}}).then(response => {
          // success toast
          this.$bvToast.toast(`Video supprimée`, {
            title: 'Succès!',
            solid: true,
            variant: 'success',
            autoHideDelay: 5000
          })
          this.getVideosByUser()
          this.updateIndexES()
        }, (response) => {
          // error toast
          this.$bvToast.toast(`Veuillez réessayer`, {
            title: 'Oops!',
            solid: true,
            variant: 'danger',
            autoHideDelay: 4000
          })
        })
      }
    },

    updateIndexES() {
      axios.get("http://localhost:5001/update")
        .then(response => {
          console.log('get /update', response);
        })
        .catch(err => {
          console.log(err);
        })
    },
  }
}
</script>

<style scoped lang="scss" module="sx">
  .logo{
    margin-right: 10px;

    .user_logo{
      background: #3f51b5;
      width:80px;
      height:80px;
      border-radius: 3em;
      display: flex;
    }
  }


  .header{
    margin: auto;
    padding: 35px;

    .title{
      color: white;
      font-size: 1.5rem;
      font-weight: 400;
    }

    .title span{
      color: #bbb;
      font-size: 1rem;
      margin-left: 5px;
      font-weight: 300;
    }
  }


  .list {
    display: flex;
    flex-wrap: wrap;

    .video {
      position: relative;
      margin: 5px;
      width: 267px;
      float: left;
    }
    .clickable:hover {
      opacity: 0.7;
      cursor: pointer;
    }

    .trash {
      position: absolute;
      right: 20px;
      top: 152px;
    }
    .trash:hover {
      cursor: pointer;
      color: #f44336;
    }
  }

  .notOnline {
    color: red;
  }
</style>
