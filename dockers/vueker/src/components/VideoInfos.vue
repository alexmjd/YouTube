<template>
  <div class="container-perso">
    <div class="container">
    <!-- <h4>Recommendation</h4> -->
      <div :class="sx.video">
        <div v-if="video.enabled == 1 || user.id == video.user_id">
          <div :class="sx.info_video">
            <div :class="sx.frame">
              <b-img src="https://picsum.photos/600/300/?image=25" fluid alt="fluid imag"></b-img>
            </div>
            <div :class="sx.title" style="display: flex; justify-content: space-between;">
              <div>
                <span> {{ video.name }} </span>
                <div :class="sx.sub_title"> {{ video.view }} vues </div>
              </div>
              <div style="display:flex;">
                <div style="text-align: right; margin-right: 10px">
                  <span style="font-size: smaller"> {{ video.user.username }} </span>
                  <div :class="sx.sub_title" style="font-size: small;"> {{ video.created_at | moment}} </div>
                </div>
                <div style="margin:auto;">
                  <div style="background: #3f51b5; width:40px; height:40px; border-radius: 2em;display: flex;"><font-awesome-icon icon="user" style="margin:auto;"/></div>
                </div>
              </div>
            </div>
          </div>
          <hr>
          <div :class="sx.info_comments">
            <div :class="sx.input_create">
              <b-form @submit.prevent="handleCreateComment" v-if="isLoggedIn">
                <b-row  class="my-3">
                  <b-col style="margin: auto; color: #3f51b5;" sm="1">
                    <font-awesome-icon icon="comment-alt" size="2x" />
                  </b-col>
                  <b-col sm="11">
                    <b-form-textarea id="body" type="text" v-model="body" rows="3" max-rows="6" required placeholder="Ajouter un commentaire public "></b-form-textarea>
                  </b-col>
                </b-row>
                <b-button class="btn-principale px-4" type="submit" style="float: right;">Ajouter</b-button>
              </b-form>
            </div>
            <div :class="sx.list_comments">
              <div :class="sx.comments" v-for="comment in comments" :key="comment.id">
                <div style="margin:auto;">
                  <div style="background: #f44336; width:40px; height:40px; border-radius: 2em;display: flex;"><font-awesome-icon icon="user" style="margin:auto;"/></div>
                </div>
                <div style="margin-left:20px;">
                  <div style="color: white; font-size: 0.9rem; font-weight: 500;"> {{ comment.user.username }} </div>
                  <div style="color: #ffffffe0; font-size: 1rem; font-weight: 400;"> {{ comment.body }} </div>
                </div>
              </div>
            </div>
            <div class="pagination">
              <div>
                <b-pagination
                  v-model="currentPage"
                  change="updateComments()"
                  :total-rows="totalComments.length"
                  :per-page="perPage"
                  aria-controls="my-table"
                ></b-pagination>
              </div>
              <div>
                <b-form-select v-model="perPage" :options="options"></b-form-select>
              </div>
                <!-- vvvvvv  juste pour voir si le endpoint retourne bien les données correspondant à la page  vvvvvv -->
                <!-- <b-table
                  class="table-dark"
                  id="my-table"
                  :items="totalComments"
                  :per-page="perPage"
                  :current-page="currentPage"
                  small
                ></b-table> -->
                <!--  ^^^^^^  juste pour voir si le endpoint retourne bien les données correspondant à la page   ^^^^^^ -->
            </div>
          </div>
          <br/>

        </div>
        <div v-else> Vidéo indisponible.</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      video: [],
      comments: [],
      totalComments: [],
      user: [],

      body: "",

      currentPage: 1,
      nbPages: 1,
      perPage: '5',
        options: [
          { value: '5', text: '5' },
          { value: '15', text: '15' },
          { value: '50', text: '50' },
          { value: '100', text: '100' },
        ]
    }
  },

  watch: {
    // on Change page
    currentPage: function () {
      this.getComments()
    },
    perPage: function () {
      this.getComments()
    }
  },

  computed : {
    isLoggedIn : function() {return this.$store.getters.isLoggedIn}
  },

  mounted () {
    if (this.$store.getters.userInfo) {
      try {
        this.user = JSON.parse(this.$store.getters.userInfo)
      } catch(e) {
        this.user = this.$store.getters.userInfo
      }
    }
    this.getNbPages()
    this.getVideoById()
    this.getComments()
  },

  methods: {
    getVideoById() {
      this.$http.get('video/' + this.$route.params.id).then(response => {
        // get data
        this.video = response.data.data
      }, (response) => {
        // error callback
        console.log('erreur', response)
      })
    },

    getComments() {
      let payload = {
        page: this.currentPage,
        perPage: this.perPage
      }
      this.$http.get('video/' + this.$route.params.id + '/comments', { params: payload }).then(response => {
        // get data
        this.comments = response.data.data
      }, (response) => {
        // error callback
        console.log('erreur comments', response)
      })
    },

    handleCreateComment() {
      let payload = {
        body: this.body
      }
      this.$http.post('video/' + this.video.id + '/comment', payload, { headers: {'Authorization': localStorage.getItem('Authorization')} }).then(response => {
        this.getComments();
        // success toast
        this.$bvToast.toast(`Succès!`, {
          title: 'Votre commentaire a bien été ajouté',
          solid: true,
          variant: 'success',
          autoHideDelay: 5000
        })
        this.body = '';
      }, (response) => {
        // error toast
        if(response.status != 403 && response.status != 401 && response.status != 404 ) {
          this.$bvToast.toast(`Veuillez réessayer`, {
            title: 'Oops!',
            solid: true,
            variant: 'danger',
            autoHideDelay: 4000
          })
        }
      })
    },

    getNbPages() {
      this.$http.get('video/' + this.$route.params.id + '/comments').then(response => {
        this.totalComments = response.data.data
        this.nbPages = Math.ceil(this.totalComments.length / this.perPage);
      }, (response) => { })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss" module="sx">
  .video{
    width: 80%;
    display: flex;
    margin: 25px 0;

    .info_video .frame img{
      width: 1000px;
      height: auto;
    }
    .title{
      padding: 20px 0;

      span{
        color: white;
        font-size: larger;
      }

      .sub_title{
        font-size: smaller;
      }
    }
  }

  .info_comments{

    .list_comments{
      margin: 85px 0;
    }

    .comments{
      display: flex;
      margin-top: 20px;
      width: max-content;
    }
  }

</style>
