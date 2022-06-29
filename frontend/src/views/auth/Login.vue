<template>
    <div class="container mt-8">
      <div class="row justify-content-center">
        <div class="col-12 col-md-5 col-xl-4 my-5">

          <!-- Heading -->
          <h1 class="display-4 text-center mb-3">
            Sign in
          </h1>
          <!-- Form -->
          <form>
            <!-- Email address -->
            <div class="form-group">

              <!-- Label -->
              <label class="form-label">
                Username
              </label>

              <!-- Input -->
              <input type="email" class="form-control" placeholder="Enter your username">

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
                <input class="form-control" type="password" placeholder="Enter your password" v-model="password">

                <!-- Icon -->
                <span class="input-group-text">
                  <i class="fe fe-eye"></i>
                </span>

              </div>
            </div>
            <!-- Submit -->
            <button class="btn btn-lg w-100 btn-primary mb-3">
              Sign in
            </button>
            <!-- Link -->
            <div class="text-center">
              <small class="text-muted text-center">
                Don't have an account yet? <a href="sign-up.html">Sign up</a>.
              </small>
            </div>
          </form>
        </div>
      </div> <!-- / .row -->
    </div> <!-- / .container -->
</template>

<script>
export default {
  name: "Login",
}
</script>

<style scoped>

</style>