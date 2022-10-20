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
      <div class="card-title">Пользовтаели административной панели</div>
      <div class="table-responsive">
        <table class="table table-sm table-hover table-no-wrap card-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Имя пользователя</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in admin_users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td><div class="d-flex">
                <router-link class="btn btn-warning" :to="{name: 'UpdateUser', params: {id: user.id}}"><span class="fe fe-edit"></span></router-link>
                <span class="fe fe-trash"></span>
              </div></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import adminUsersApi from "../../api/adminUsersApi";
export default {
  name: "AdminUsersList",

  data: () => ({
    admin_users: []
  }),

  methods: {
    loadAdminUsers() {
      adminUsersApi.getAdminUsersList().then(response => {
        this.admin_users = response.data;
      })
    }
  },

  created() {
    this.loadAdminUsers()
  }
}
</script>

<style scoped>

</style>