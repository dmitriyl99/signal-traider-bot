<template>
  <div class="card">
    <div class="card-header">
      <div class="row align-items-center">
        <div class="d-flex justify-content-end">
          <router-link :to="{name: 'CreateUser'}" class="btn btn-primary lift">
              Добавить пользователя
            </router-link>
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
              <th>Дата регистрации</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.phone }}</td>
              <td v-if="user.subscription == null">-</td>
              <td :class="{'text-success': user.subscription.active, 'text-danger': !user.subscription.active}" v-else>{{ user.subscription.subscription.name }}, {{ user.subscription.duration_in_days }} дней</td>
              <td>{{ (new Date(user.created_at)).toLocaleString() }}</td>
              <td><span class="text-success" v-if="user.registration_date != null">{{ (new Date(user.registration_date)).toLocaleString() }}</span><span v-else class="text-danger">Не зарегистрирован</span></td>
              <td><router-link class="btn btn-warning" :to="{name: 'UpdateUser', params: {id: user.id}}"><span class="fe fe-edit"></span></router-link></td>
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