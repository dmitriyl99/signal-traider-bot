<template>
<div class="card">
  <div class="card-header">
    <h3>Рассылки</h3>
  </div>
  <div class="card-body">
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
            <td>{{ (new Date(distribution.created_at)).toLocaleDateString() }} {{ (new Date(distribution.created_at)).toLocaleTimeString() }}</td>
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