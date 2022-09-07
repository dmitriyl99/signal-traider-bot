<template>
<div class="card">
  <div class="card-header">
    <h3>Список сигналов</h3>
  </div>
  <div class="card-body">
    <div class="table-responsive" v-if="signals.length > 0">
      <table class="table table-sm table-hover table-no-wrap card-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Валюта</th>
            <th>Метод исполнения</th>
            <th>Цена</th>
            <th>TP 1</th>
            <th>TP 2</th>
            <th>SL</th>
            <th>Дата</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="signal in signals" :key="signal.id">
            <td>{{ signal.id }}</td>
            <td>{{ signal.currency_pair }}</td>
            <td>{{ signal.execution_method }}</td>
            <td>{{ signal.price }}</td>
            <td>{{ signal.tr_1 }}</td>
            <td>{{ signal.tr_2 }}</td>
            <td>{{ signal.sl }}</td>
            <td>{{ (new Date(signal.created_at)).toLocaleDateString() }}</td>
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
  name: "ListSignals",
  data: () => ({
    signals: []
  }),
  created() {
    signalsApi.getAllSignals().then(response => {
      this.signals = response.data;
    })
  }
}
</script>

<style scoped>

</style>