<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import {mapGetters} from 'vuex'

export default {
  name: 'Home',
  components: {
    HelloWorld
  },

  computed: {
    ...mapGetters([
        'jwtToken'
    ])
  },

  beforeCreate() {
    if (this.jwtToken == null) {
      this.$router.push({name: 'auth.login'})
    }
  }
}
</script>
