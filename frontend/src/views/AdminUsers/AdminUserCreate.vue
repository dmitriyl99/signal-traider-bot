<template>
<div class="card">
    <div class="card-header">
      <h3>Добавить нового пользователя административной панели</h3>
    </div>
    <div class="card-body">
      <form v-on:submit.prevent="saveUser">
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="username" class="form-label">Юзернейм</label>
            <input type="text" required id="username" class="form-control" placeholder="Username..." v-model="username">
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="roles" class="form-label">Роль</label>
            <select type="text" class="form-select" id="roles" v-model="selectedRoles">
              <option :value="role.id" v-for="role in roles" :key="role.id">{{ role.name }}</option>
            </select>
          </div>
        </div>
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="password" class="form-label">Пароль</label>
            <input type="password" required id="password" class="form-control" placeholder="Пароль" v-model="password">
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="password_confirmation" class="form-label">Подтвердите пароль</label>
            <input type="password" required id="password_confirmation" class="form-control" placeholder="Подтверждение пароля" v-model="password_confirmation">
          </div>
        </div>
        <button :disabled="isLoading" class="btn btn-primary mt-3" type="submit" v-html="isLoading ? 'Сохраняю, подождите...' : 'Сохранить'"/>
      </form>
    </div>
  </div>
</template>

<script>
import adminUsersApi from "../../api/adminUsersApi";
export default {
  name: "AdminUserCreate",
  data: () => ({
    username: null,
    password: null,
    password_confirmation: null,
    isLoading: false,
    roles: [],
    selectedRoles: []
  }),

  methods: {
    saveUser() {
      if (this.password !== this.password_confirmation) {
        this.$swal({
          icon: 'error',
          text: 'Пароли не совпадают'
        });
        return;
      }
      this.isLoading = true;
      adminUsersApi.createAdminUser(
          this.username,
          this.password,
          this.password_confirmation,
          [this.selectedRoles],
          []
      ).then(() => {
        this.$swal({
          icon: 'success',
          text: 'Пользовтаель добавлен'
        }).then(() => {
          this.$router.push({name: 'admin-users.list'})
        })
      }).finally(() => {
        this.isLoading = false;
      })
    },

    loadRoles() {
      adminUsersApi.getRoles().then(response => {
        this.roles = response.data;
      })
    }
  },
  created() {
    this.loadRoles()
  }
}
</script>

<style scoped>

</style>