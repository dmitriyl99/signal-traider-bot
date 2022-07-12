<template>
  <div class="card">
    <div class="card-header">
      <div class="row align-items-center">
        <div class="col">
          <form>
            <div class="input-group input-group-flush input-group-merge input-group-reverse">
              <input class="form-control list-search" type="search" placeholder="Search">
              <span class="input-group-text">
                              <i class="fe fe-search"></i>
                            </span>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title">Пользовтаели Telegram-бота</div>
      <div class="table-responsive">
        <table class="table table-sm table-hover table-no-wrap card-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Имя</th>
              <th>Номер телефона</th>
              <th>Подписка</th>
              <th>Дата создания</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.phone }}</td>
              <td v-if="user.subscription == null">-</td>
              <td :class="{'text-success': user.subscription.active, 'text-danger': !user.subscription.active}" v-else>{{ user.subscription.subscription_condition.subscription.name }}, {{ user.subscription.subscription_condition.duration_in_month }} мес.</td>
              <td>{{ (new Date(user.created_at)).toLocaleDateString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import usersApi from "../../api/usersApi";
export default {
  name: "UsersList",
  data: () => ({
    users: []
  }),
  created() {
    usersApi.getUsersList().then(response => {
      this.users = response.data
    })
  }
}
</script>

<style scoped>

</style>