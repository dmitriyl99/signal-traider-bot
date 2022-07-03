<template>
  <div class="card">
    <div class="card-header">
      <h3>Отправить новый сигнал</h3>
    </div>
    <div class="card-body">
      <form v-on:submit.prevent="onFormSubmit">
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="currency_pair" class="form-label">Валютная пара</label>
            <input type="text" class="form-control" id="currency_pair" placeholder="Валютная пара" v-model="currency_pair"/>
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="execution_method" class="form-label">Метод исполнения</label>
            <select type="text" class="form-select" id="execution_method" v-model="execution_method">
              <option value="sell">Sell</option>
              <option value="buy">Buy</option>
              <option value="sell_limit">Sell Limit</option>
              <option value="buy_limit">Buy Limit</option>
              <option value="sell_stop">Sell Stop</option>
              <option value="buy_stop">Buy Stop</option>
            </select>
          </div>
        </div>
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="tr_1" class="form-label">TR 1</label>
            <input type="text" class="form-control" id="tr_1" placeholder="TR 1" v-model="tr_1"/>
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="tr_2" class="form-label">TR 2</label>
            <input type="text" class="form-control" id="tr_2" placeholder="TR 2" v-model="tr_2"/>
          </div>
        </div>
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="price" class="form-label">Цена</label>
            <input type="number" class="form-control" id="price" placeholder="Цена" v-model="price"/>
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="sl" class="form-label">SL</label>
            <input type="text" class="form-control" id="sl" placeholder="SL" v-model="sl"/>
          </div>
        </div>

        <!-- Button -->
        <button class="btn btn-primary" type="submit" v-html="isLoading ? 'Отправляю, подождите...' : 'Отправить сигнал'"/>
        <span class="text-success ms-3" v-if="successText != null">{{ successText }}</span>

      </form>
    </div>
  </div>
</template>

<script>
import signalsApi from "../../api/signalsApi";

export default {
  name: "CreateSignal",
  data: () => ({
    currency_pair: null,
    execution_method: null,
    price: null,
    tr_1: null,
    tr_2: null,
    sl: null,
    isLoading: false,
    successText: null
  }),

  methods: {
    onFormSubmit() {
      this.isLoading = true;
      this.successText = null;
      signalsApi.sendSignal(this.currency_pair, this.execution_method, this.price, this.tr_1, this.tr_2, this.sl).then(() => {
        this.successText = 'Сигнал успешно отправлен';
      }).finally(() => {
        this.isLoading = false;
      })
    }
  }
}
</script>