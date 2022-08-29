<template>
  <div class="card">
    <div class="card-header">
      <h3>Изменить пользователя Telegram бота</h3>
    </div>
    <div class="card-body">
      <form v-on:submit.prevent="saveUser">
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="user_name" class="form-label">Имя</label>
            <input type="text" name="name" id="user_name" class="form-control" placeholder="Имя пользователя" v-model="name">
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="user_phone" class="form-label">Номер телефона</label>
            <input type="text" name="phone" id="user_phone" class="form-control" placeholder="Номер телефона" v-model="phone">
          </div>
        </div>
        <div class="row g-3">
          <div class="col-12 col-md-4 nb-3">
            <label class="form-label">Подписка</label>
            <select class="form-select" id="user_subscription" v-model="selectedSubscriptionId">
              <option v-for="subscription in subscriptions" :key="subscription.id" :value="subscription.id">
                {{ subscription.name }}
              </option>
            </select>
          </div>
          <div class="col-12 col-md-4 nb-3" v-if="selectedSubscription != null">
            <label class="form-label">Условие подписки</label>
            <select id="user_subscription_condition" class="form-select" v-model="selectedSubscriptionConditionId">
              <option v-for="condition in selectedSubscription.conditions" :key="condition.id" :value="condition.id">
                {{ condition.duration_in_month }} мес.
              </option>
            </select>
          </div>
          <div class="col-12 col-md-4 mb-3" v-if="selectedSubscription != null" >
            <label for="subscription_duration_in_days" class="form-label">Дней подписки</label>
            <input type="number" name="subscription_duration_in_days" id="subscription_duration_in_days" class="form-control" placeholder="Количество дней подписки" v-model="subscriptionDurationInDays">
          </div>
        </div>
        <button :disabled="isLoading" class="btn btn-primary mt-3" type="submit" v-html="isLoading ? 'Сохраняю, подождите...' : 'Сохранить'"/>
      </form>
    </div>
  </div>
</template>

<script>
import subscriptionsApi from "../../api/subscriptionsApi";
import usersApi from "../../api/usersApi";

export default {
  name: "UpdateUser",
  data: () => ({
    name: null,
    phone: '998',
    subscriptions: [],
    selectedSubscriptionId: null,
    selectedSubscriptionConditionId: null,
    subscriptionDurationInDays: null,
    isLoading: false
  }),

  computed: {
    selectedSubscription() {
      if (this.selectedSubscriptionId == null) {
        return null;
      }
      return this.subscriptions.find(subscription => subscription.id === this.selectedSubscriptionId);
    }
  },

  methods: {
    loadData() {
      subscriptionsApi.getSubscriptions().then(response => {
        this.subscriptions = response.data;
        this.loadUser();
      })
    },

    loadUser() {
      usersApi.getUserById(this.$route.params.id).then(response => {
        let user = response.data
        this.name = user.name;
        this.phone = user.phone;
        this.selectedSubscriptionId = user.subscription.subscription_id;
        this.selectedSubscriptionConditionId = user.subscription.subscription_condition_id
      }).catch(error => {
        if (error.response.status === 404) {
          this.$router.push({name: 'UsersList'})
        }
      })
    },

    saveUser() {
      this.isLoading = true;
      usersApi.updateUser(
          this.$route.params.id,
          this.name,
          this.phone,
          this.selectedSubscriptionId,
          this.selectedSubscriptionConditionId,
          this.subscriptionDurationInDays
      ).then(() => {
        this.$router.push({name: 'UsersList'})
      }).finally(() => {
        this.isLoading = false;
      })
    }
  },

  created() {
    this.loadData()
  }
}
</script>

<style scoped>

</style>