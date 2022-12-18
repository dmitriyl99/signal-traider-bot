<template>
  <div class="card">
    <div class="card-header">
      <div class="row align-items-center">
        <div class="d-flex justify-content-end">
          <router-link :to="{name: 'CreateDistribution'}" class="btn btn-primary lift">
              Отправить сообщение
            </router-link>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title">Рассылки</div>
      <div class="table-responsive" v-if="distributions.length > 0">
        <table class="table table-sm table-hover table-no-wrap card-table">
          <thead>
          <tr>
            <th>Текст</th>
            <th>Отправитель</th>
            <th>Дата</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="distribution in distributions" :key="distribution.id">
            <td>{{ distribution.text }}</td>
            <td>{{ distribution.admin_user }}</td>
            <td>{{ (new Date(distribution.created_at)).toLocaleDateString() }}
              {{ (new Date(distribution.created_at)).toLocaleTimeString() }}
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import signalsApi from "../../api/signalsApi";

export default {
  name: "DistributionsList",
  data: () => ({
    distributions: []
  }),

  methods: {
    loadDistributions() {
      signalsApi.loadCustomMessages().then(response => {
        this.distributions = response.data
      })
    }
  },

  created() {
    this.loadDistributions()
  }
}
</script>