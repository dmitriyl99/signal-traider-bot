<template>
  <div>
    <h2>Пользователи</h2>
    <div class="row" v-if="usersStatistics != null">
      <div class="col-12 col-lg-6 col-xl">
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col">
                <h6 class="text-uppercase text-muted mb-2">Всего пользователей</h6>
                <span class="h2 mb-0">{{ usersStatistics.all_users_count }}</span>
              </div>
              <div class="col-auto">
                <span class="h2 fe fe-user text-muted mb-0"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6 col-xl">
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col">
                <h6 class="text-uppercase text-muted mb-2">Новых пользователей</h6>
                <span class="h2 mb-0">{{ usersStatistics.new_users_count }}</span>
                <span class="badge mt-n1 ms-1" :class="{'bg-success-soft': usersStatistics.growth_users_count > 0, 'bg-danger-soft': usersStatistics.growth_users_count <= 0}">
                      {{ usersStatistics.growth_users_count }}
                </span>
              </div>
              <div class="col-auto">
                <span class="h2 fe fe-user-plus text-muted mb-0"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="border-bottom"></div>
    <div class="row mt-3">

    </div>
  </div>
</template>

<script>
import statisticsApi from "../api/statisticsApi";
export default {
  name: "Dashboard",
  data: () => ({
    usersStatistics: null
  }),
  methods: {
    fetchUsersStatistic() {
      statisticsApi.getUsersStatistics().then(response => {
        this.usersStatistics = response.data;
      })
    }
  },
  created() {
    this.fetchUsersStatistic()
  }
}
</script>