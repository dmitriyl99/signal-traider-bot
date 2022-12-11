<template>
<nav class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light" id="sidebar">
      <div class="container-fluid">
        <!-- Toggler -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#sidebarCollapse" aria-controls="sidebarCollapse" aria-expanded="false" aria-label="Toggle navigation" @click="toggleSidebarCollapsed">
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
              <hr class="dropdown-divider">
              <button v-on:click="logout" class="dropdown-item">Logout</button>
            </div>
          </div>
        </div>

        <!-- Collapse -->
        <div class="collapse navbar-collapse" :class="{show: sidebarShow}" id="sidebarCollapse">

          <!-- Navigation -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link :to="{name: 'UsersList'}" class="nav-link">
                <i class="fe fe-users"></i> Пользователи Telegram
              </router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{name: 'ListSignals'}" class="nav-link">
                <i class="fe fe-bell"></i> Сигналы
              </router-link>
            </li>
            <li class="nav-item" v-if="currentUserHasAdminRole">
              <router-link class="nav-link" :to="{name: 'ListDistributions'}">
                <i class="fe fe-message-circle"></i> Рассылки
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{name: 'CurrencyPairsList'}">
                <i class="fe fe-dollar-sign"></i> Валютные пары
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{name: 'UtmList'}">
                <i class="fe fe-git-commit"></i> UTM-метки
              </router-link>
            </li>
            <li class="nav-item" v-if="currentUserHasAdminRole">
              <router-link class="nav-link" :to="{name: 'PaymentsList'}">
                <i class="fe fe-credit-card"></i> Платежи
              </router-link>
            </li>
            <li class="nav-item" v-if="currentUserHasAdminRole">
              <router-link class="nav-link" :to="{name: 'admin-users.list'}">
                <i class="fe fe-user-check"></i> Администраторы
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
                <div v-if="$store.state.auth.current_user != null">
                    {{ $store.state.auth.current_user.username }}
                  </div>

                <!-- Menu -->
                <div class="dropdown-menu" aria-labelledby="sidebarIconCopy">
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
  data: () => ({
    sidebarShow: false
  }),
  created() {
    console.log(this.$router.currentRoute.value.name)
  },
  computed: {
    currentUserHasAdminRole() {
      if (this.$store.state.auth.current_user != null)
        return this.$store.state.auth.current_user.roles.filter(role => role.name === 'Admin').length;
      return false;
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      this.$router.push({ name: 'auth.login' })
    },

    toggleSidebarCollapsed() {
      this.sidebarShow = !this.sidebarShow;
    }
  }
}
</script>

<style scoped>

</style>