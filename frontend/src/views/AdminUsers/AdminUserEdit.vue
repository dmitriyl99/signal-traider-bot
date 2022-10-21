<template>
  <div class="card">
    <div class="card-header">
      <h3>Добавить нового пользователя административной панели</h3>
    </div>
    <div class="card-body">
      <div class="row g-3">
        <div class="col-12 mb-3">
          <label for="username" class="form-label">Юзернейм</label>
          <input type="text" required id="username" class="form-control" placeholder="Username..." v-model="username">
        </div>
      </div>
      <form v-on:submit.prevent="changePassword">
        <h3>Сменить пароль</h3>
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="password" class="form-label">Пароль</label>
            <input type="password" required id="password" class="form-control" placeholder="Пароль"
                   v-model="new_password">
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="password_confirmation" class="form-label">Подтвердите пароль</label>
            <input type="password" required id="password_confirmation" class="form-control"
                   placeholder="Подтверждение пароля" v-model="new_password_confirmation">
          </div>
        </div>
        <button :disabled="isLoading" class="btn btn-primary mt-3" type="submit"
                v-html="isLoading ? 'Меняю, подождите...' : 'Сменить пароль'"/>
      </form>
    </div>
  </div>
</template>

<script>
import adminUsersApi from "../../api/adminUsersApi";

export default {
  name: "AdminUserEdit",
  data: () => ({
    username: null,
    new_password: null,
    new_password_confirmation: null,
    isLoading: false,

    roles: [],
    permissions: []
  }),

  methods: {
    loadUser() {
      adminUsersApi.getAdminUserById(this.$route.params.id).then(response => {
        this.username = response.data.username
      })
    },

    changePassword() {
      if (this.new_password !== this.new_password_confirmation) {
        this.$swal({
          icon: 'error',
          text: 'Пароли не совпадают'
        })
        return
      }
      this.isLoading = true;
      adminUsersApi.changePassword(this.$route.params.id, this.new_password, this.new_password_confirmation).then(() => {
        this.$swal({
          icon: 'success',
          text: 'Пароль успешно изменён'
        })
      }).finally(() => {
        this.isLoading = false;
      })
    }
  },
  created() {
    this.loadUser()
  }
}
</script>

<style scoped>

</style>