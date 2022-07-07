<template>
<nav class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light" id="sidebar">
      <div class="container-fluid">
        <!-- Toggler -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#sidebarCollapse" aria-controls="sidebarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <!-- Brand -->
        <router-link :to="{name: 'Home'}" class="navbar-brand">
          <img src="@/assets/img/logo.svg" class="navbar-brand-img mx-auto" alt="...">
        </router-link>
        <!-- User (xs) -->
        <div class="navbar-user d-md-none">
          <!-- Dropdown -->
          <div class="dropdown">
            <!-- Toggle -->
            <a href="#" id="sidebarIcon" class="dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <div class="avatar avatar-sm avatar-online">
                <img src="@/assets/img/avatars/profiles/avatar-6.jpg" class="avatar-img rounded-circle" alt="...">
              </div>
            </a>
            <!-- Menu -->
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="sidebarIcon">
              <a href="./profile-posts.html" class="dropdown-item">Profile</a>
              <hr class="dropdown-divider">
              <button v-on:click="logout" class="dropdown-item">Logout</button>
            </div>
          </div>
        </div>

        <!-- Collapse -->
        <div class="collapse navbar-collapse" id="sidebarCollapse">

          <!-- Navigation -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link :to="{name: 'UsersList'}" class="nav-link">
                <i class="fe fe-user"></i> Пользователи
              </router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link">
                <i class="fe fe-bell"></i> Cигналы
              </a>
            </li>
            <li class="nav-item">
              <router-link class="nav-link " :to="{name: 'PaymentsList'}">
                <i class="fe fe-credit-card"></i> История оплат
              </router-link>
            </li>
          </ul>

          <!-- Push content down -->
          <div class="mt-auto"></div>


            <!-- User (md) -->
            <div class="navbar-user d-none d-md-flex" id="sidebarUser">

              <!-- Dropup -->
              <div class="dropup">

                <!-- Toggle -->
                <a href="#" id="sidebarIconCopy" class="dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <div class="avatar avatar-sm avatar-online">
                    <img src="@/assets/img/avatars/profiles/avatar-6.jpg" class="avatar-img rounded-circle" alt="...">
                  </div>
                </a>

                <!-- Menu -->
                <div class="dropdown-menu" aria-labelledby="sidebarIconCopy">
                  <a href="./profile-posts.html" class="dropdown-item">Profile</a>
                  <hr class="dropdown-divider">
                  <button v-on:click="logout" class="dropdown-item">Logout</button>
                </div>

              </div>

            </div>

        </div> <!-- / .navbar-collapse -->

      </div>
    </nav>
</template>

<script>
export default {
  name: "Sidebar",
  created() {
    console.log(this.$router.currentRoute.value.name)
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      this.$router.push({ name: 'auth.login' })
    }
  }
}
</script>

<style scoped>

</style>