<template>
  <div>
    <h2>Статистика</h2>
    <div class="row" v-if="usersStatistics != null && subscriptionsStatistics != null">
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
                <h6 class="text-uppercase text-muted mb-2">Купленных подписок</h6>
                <span class="h2 mb-0">{{ subscriptionsStatistics.all_active_subscriptions_count }}</span>
              </div>
              <div class="col-auto">
                <span class="h2 fe fe-star text-muted mb-0"></span>
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
                <h6 class="text-uppercase text-muted mb-2">Пользователей без подписок</h6>
                <span class="h2 mb-0">{{ subscriptionsStatistics.users_without_subscriptions_count }}</span>
              </div>
              <div class="col-auto">
                <span class="h2 fe fe-user text-muted mb-0"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import statisticsApi from "../api/statisticsApi";

export default {
  name: "Dashboard",
  data: () => ({
    usersStatistics: null,
    subscriptionsStatistics: null
  }),
  methods: {
    fetchUsersStatistic() {
      statisticsApi.getUsersStatistics().then(response => {
        this.usersStatistics = response.data;
      });
    },
    fetchSubscriptionsStatistics() {
      statisticsApi.getSubscriptionsStatistics().then(response => {
        this.subscriptionsStatistics = response.data;
      })
    }
  },
  created() {
    this.fetchUsersStatistic();
    this.fetchSubscriptionsStatistics();
  }
}
</script>