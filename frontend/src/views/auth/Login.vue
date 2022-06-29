<template>
  <div class="container mt-8">
    <div class="row justify-content-center">
      <div class="col-12 col-md-5 col-xl-4 my-5">

        <!-- Heading -->
        <h1 class="display-4 text-center mb-3">
          Sign in
        </h1>
        <p v-if="errorMessageText !== null" class="text-danger">{{ errorMessageText }}</p>
        <!-- Form -->
        <form v-on:submit.prevent="onLoginEvent">
          <!-- Email address -->
          <div class="form-group">

            <!-- Label -->
            <label class="form-label">
              Username
            </label>

            <!-- Input -->
            <input type="text" class="form-control" :class="{'is-invalid': usernameText !== null}" placeholder="Enter your username" v-model="username">
            <div class="invalid-feedback" v-if="usernameText !== null">{{ usernameText }}</div>

          </div>

          <!-- Password -->
          <div class="form-group">
            <div class="row">
              <!-- Label -->
              <label class="form-label">
                Password
              </label>
            </div> <!-- / .row -->

            <!-- Input group -->
            <div class="input-group input-group-merge">

              <!-- Input -->
              <input class="form-control" :class="{'is-invalid': passwordText !== null}" type="password" placeholder="Enter your password" v-model="password">
              <div class="invalid-feedback" v-if="passwordText !== null">{{ passwordText }}</div>

            </div>
          </div>
          <!-- Submit -->
          <button class="btn btn-lg w-100 btn-primary mb-3" type="submit" v-html="loading ? 'Loading...' : 'Sign in'">
          </button>
        </form>
      </div>
    </div> <!-- / .row -->
  </div> <!-- / .container -->
</template>

<script>
export default {
  name: "Login",
  data: () => ({
    username: null,
    password: null,

    loading: false,

    passwordText: null,
    usernameText: null,

    errorMessageText: null
  }),
  methods: {
    onLoginEvent() {
      this.loading = true;
      this.passwordText = null;
      this.usernameText = null;
      this.errorMessageText = null;
      this.$store.dispatch('login', {username: this.username, password: this.password}).then(() => {
        this.loading = false;
        console.log('router push');
        this.$router.push({name: 'Home'})
      }, error => {
        this.loading = false;
        let response = error.response
        console.log(response.status);
        if (response.status === 422) {
          let details = response.data.detail;
          details.forEach(e => {
            if (e.loc[1] === 'password') {
              this.passwordText = 'Password is required';
            }
            if (e.loc[1] === 'username') {
              this.usernameText = 'Username is required'
            }
          })
        }
        if (response.status === 401) {
          this.errorMessageText = response.data.detail;
        }
      })
    }
  }
}
</script>

<style scoped>

</style>