<template>
  <div class="card">
    <div class="card-header">
      <div class="row align-items-center">
        <div class="col-8">
          <div class="search-group">
            <input type="text" class="form-control form-control-flush" v-model="searchQuery" placeholder="Search">
          </div>
        </div>
        <div class="col-4">
          <div class="d-flex justify-content-end align-items-center">
            <router-link :to="{name: 'CreateUser'}" class="btn btn-primary me-4">
              Добавить пользователя
            </router-link>
            <button class="btn btn-primary" @click="excelDownload">Скачать Excel</button>
          </div>
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
          <tr v-for="user in users.items" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.phone }}</td>
            <td v-if="user.subscription == null">-</td>
            <td :class="{'text-success': user.subscription.active, 'text-danger': !user.subscription.active}" v-else>
              {{ user.subscription.subscription.name }}, {{ user.subscription.duration_in_days }} дней
            </td>
            <td>{{ (new Date(user.created_at)).toLocaleString() }}</td>
            <td><span class="text-success" v-if="user.registration_date != null">{{
                (new Date(user.registration_date)).toLocaleString()
              }}</span><span v-else class="text-danger">Не зарегистрирован</span></td>
            <td>
              <div class="d-flex justify-content-around">
                <router-link class="btn btn-warning" :to="{name: 'UpdateUser', params: {id: user.id}}"><span
                    class="fe fe-edit"></span></router-link>
                <button class="btn btn-danger" v-on:click="deleteUser(user.id)"><span class="fe fe-trash"></span>
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
      <vue-awesome-paginate
          :total-items=users.total
          :items-per-page=25
          :max-pages-shown="5"
          v-model="page"
          :on-click="onClickHandler"
      />
    </div>
  </div>
</template>

<script>
import usersApi from "../../api/usersApi";
import {debounce} from "lodash";

export default {
  name: "UsersList",
  data: () => ({
    users: [],
    page: 1,
    searchQuery: "",
    isTyping: false,
    isLoading: false
  }),
  watch: {
    searchQuery: debounce(function () {
      console.log(this.searchQuery)
      this.fetchUsers()
    }, 1000),
  },
  methods: {
    excelDownload() {
      usersApi.downloadExcel().then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.style.display = 'none';
        link.setAttribute('download', 'Пользователи.xlsx');
        document.body.appendChild(link);
        link.click()
      })
    },
    onClickHandler(page) {
      usersApi.getUsersList(page).then(response => {
        this.users = response.data
      })
    },
    fetchUsers() {
      usersApi.getUsersList(this.page, this.searchQuery).then(response => {
        this.users = response.data
      })
    },
    deleteUser(user_id) {
      this.$swal({
        icon: 'warning',
        title: 'Вы уверены?',
        text: 'Вы уверены что хотите удалить пользователя? Это так же удалит его подписку и все его платежи. Эти данные нельзя будет вернуть',
        showCancelButton: true,
        confirmButtonText: "Удалить пользователя",
        cancelButtonText: "Отмена",
        dangerMode: true
      })
        .then(({isConfirmed}) => {
          console.log(isConfirmed);
          if (isConfirmed) {
            usersApi.deleteUser(user_id).then(() => {
              this.$swal({
                icon: 'success',
                text: 'Пользователь удалён'
              })
              this.fetchUsers()
            }).catch(e => {
              this.$swal({
                icon: 'error',
                title: 'Ошика',
                text: e.response.data.detail
              })
            })
          }
        })
    }
  },
  created() {
    this.fetchUsers()
  }
}
</script>

<style>
.pagination-container {
  display: flex;
  column-gap: 10px;
}

.paginate-buttons {
  height: 40px;
  width: 40px;
  border-radius: 20px;
  cursor: pointer;
  background-color: rgb(242, 242, 242);
  border: 1px solid rgb(217, 217, 217);
  color: black;
}

.paginate-buttons:hover {
  background-color: #d8d8d8;
}

.active-page {
  background-color: #3498db;
  border: 1px solid #3498db;
  color: white;
}

.active-page:hover {
  background-color: #2988c8;
}
</style>