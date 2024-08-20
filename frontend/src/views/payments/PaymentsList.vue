<template>
  <div class="card">
    <div class="card-header">
      <div class="row align-items-center">
        <div class="col-2">Фильтры</div>
        <div class="col-2">
          <select class="form-select" v-model="filter_status">
            <option value="" selected>Статус</option>
            <option value="NEW">Неоплаченный</option>
            <option value="CONFIRMED">Подтвержденный</option>
            <option value="REJECTED">Отклоненный</option>
            <option value="WAITING">В обработке</option>
          </select>
        </div>
        <div class="col-2">
          <select class="form-select" v-model="filter_sum">
            <option value="0" selected>Сумма</option>
            <option value="500000">500 000</option>
            <option value="1000000">1 000 000</option>
          </select>
        </div>
        <div class="col-2">
          <select class="form-select" v-model="filter_provider">
            <option value="">Провайдер</option>
            <option value="Click">Click</option>
            <option value="Payme">Payme</option>
          </select>
        </div>
        <div class="col-2">
          <select class="form-select" v-model="filter_duration">
            <option value="0">Длительность</option>
            <option value="1">1 месяц</option>
            <option value="2">2 месяца</option>
          </select>
        </div>
        <div class="col-2">
          <flat-pickr v-model="filter_date" class="form-control" placeholder="Дата" :config="{
            'mode': 'range',
            maxDate: new Date()
          }"/>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title">Транзакции Telegram-бота</div>
      <div class="table-responsive">
        <table class="table table-sm table-hover table-no-wrap card-table">
          <thead>
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Номер телефона</th>
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
            <td><span v-if="payment.user">{{ payment.user.name }}</span><span></span></td>
            <td><span v-if="payment.user">{{ payment.user.phone }}</span><span></span></td>
            <td>{{ payment.amount.toLocaleString() }}</td>
            <td>{{ payment.provider }}</td>
            <td :style="'color:'+statusMapper[payment.status].color">{{ statusMapper[payment.status].title }}</td>
            <td>{{ payment.subscription.name }}</td>
            <td>{{ payment.subscription_condition.duration_in_month }} мес.</td>
            <td>{{ addHours(new Date(payment.created_at), 5).toLocaleDateString() }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import paymentsApi from "../../api/paymentsApi";
import date_helper from "../../helpers/date"
import flatPickr from 'vue-flatpickr-component';

export default {
  name: "PaymentsList",
  components: {
    flatPickr
  },
  data: () => ({
    payments: [],
    filter_sum: 0,
    filter_provider: "",
    filter_status: "",
    filter_duration: 0,
    filter_date: null,
    filter_date_from: null,
    filter_date_to: null,
    statusMapper: {
      "NEW": {
        title: "Неоплаченный",
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
    this.loadPayments()
  },
  methods: {
    addHours(date, hours) {
      return date_helper.addHours(date, hours)
    },
    loadPayments() {
      paymentsApi.getPayments(
          this.filter_status,
          this.filter_sum,
          this.filter_provider,
          this.filter_duration,
          this.filter_date_from,
          this.filter_date_to
      ).then(response => {
        this.payments = response.data
      })
    }
  },
  watch: {
    filter_status: function () {
      this.loadPayments()
    },
    filter_sum: function () {
      this.loadPayments()
    },
    filter_provider: function () {
      this.loadPayments()
    },
    filter_duration: function () {
      this.loadPayments()
    },
    filter_date: function (val) {
      if (val && val !== '') {
        if (val.includes('to')) {
          let splittedValues = val.split(' to ')
          this.filter_date_from = splittedValues[0]
          this.filter_date_to = splittedValues[1]
          this.loadPayments()
        }
      }
    }
  }
}
</script>

<style scoped>

</style>