<template>
  <div class="card">
    <div class="card-body">
      <div class="card-title">Транзакции Telegram-бота</div>
      <div class="table-responsive">
        <table class="table table-sm table-hover table-no-wrap card-table">
          <thead>
          <tr>
            <th>ID</th>
            <th>Сумма</th>
            <th>Провайдер</th>
            <th>Статус</th>
            <th>Подписка</th>
            <th>Длительность</th>
            <th>Дата</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="payment in payments" :key="payment.id">
            <td>{{ payment.id }}</td>
            <td>{{ payment.amount.toLocaleString() }}</td>
            <td>{{ payment.provider }}</td>
            <td :style="'color:'+statusMapper[payment.status].color">{{ statusMapper[payment.status].title }}</td>
            <td>{{ payment.subscription.name }}</td>
            <td>{{ payment.subscription_condition.duration_in_month }} мес.</td>
            <td>{{ (new Date(payment.created_at)).toLocaleDateString() }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import paymentsApi from "../../api/paymentsApi";
export default {
  name: "PaymentsList",
  data: () => ({
    payments: [],
    statusMapper: {
      "NEW": {
        title: "Новый",
        color: "#686363"
      },
      "CONFIRMED": {
        title: "Подтвержденный",
        color: "#3db71e"
      },
      "REJECTED": {
        title: "Отклоненный",
        color: "#de0f0f"
      },
      "WAITING": {
        title: "В обработке",
        color: "#e8900c"
      }
    }
  }),
  created() {
    paymentsApi.getPayments().then(response => {
      this.payments = response.data
    })
  }
}
</script>

<style scoped>

</style>