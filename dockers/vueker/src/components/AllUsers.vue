<template>
  <div class="container-perso">
    <div class="container">
      <b-form class="m-3" :class="sx.user" @submit.prevent="searchUser">
        <h1 style="color: white;"> Rechercher un utilisateur</h1>
        <b-form-group id="input-group-1" label="Pseudo:" label-for="input-1">
          <b-form-input id="pseudo" type="text" size="lg" v-model="pseudo" placeholder="Pseudo" autofocus />
        </b-form-group>
        <b-button variant="primary" class="px-4" type="submit">Rechercher</b-button>
      </b-form>
      <div :class="sx.users" v-for="user in users" :key="user.id">
        <div>
          <router-link :to="'/chaine/' + user.id">
            <div> {{ user.username }} </div>
          </router-link>
          <div>pseudo : {{ user.pseudo }}</div>
          <div class="small text-white"> {{ user.id }} * {{ user.created_at }} </div>
        </div>
      </div>
      <br/>
      <div class="pagination">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalUsers.length"
          :per-page="perPage"
          aria-controls="my-table"
        ></b-pagination>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      users: [],
      totalUsers: [],
      pseudo: "",
      page: 1,
      perPage: 3,
      currentPage: 1,
      nbPages: 1
    }
  },
  watch: {
    currentPage: function () {
      // on Change page
      this.searchUser();
    }
  },
  mounted () {
    this.getNbPages();
    this.searchUser();
  },
  methods: {
    searchUser() {
      let payload = {
        pseudo: this.pseudo,
        page: this.currentPage,
        perPage: this.perPage,
      }
      this.$http.get('users', {params: payload}).then(response => {
        this.users = response.data.data
        this.getNbPages()
        // get data
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
        console.log('erreur', response)
      })
    },
    getNbPages() {
      let payload = {
        pseudo: this.pseudo,
      }
      this.$http.get('users', {params: payload}).then(response => {
        this.totalUsers = response.data.data
        this.nbPages = Math.ceil(this.totalUsers.length / this.perPage);
      }, (response) => { })
    }
  }
}
</script>
<style scoped lang="scss" module="sx">
  .users{
    width: max-content;
    display: flex;
  }
</style>
