<template>
  <div>
    <div class="card">
      <div class="card-body">
        <form v-on:submit.prevent="saveCurrencyPair">
          <label for="currency_pair_name" class="form-label">Добавить валютную пару</label>
          <input type="text" name="currency_pair_name" id="currency_pair_name" class="form-control" placeholder="Название"
                 v-model="currency_pair_name">
          <button type="submit" class="btn btn-primary mt-2">Сохранить</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <div class="card-title">Валютные пары</div>
        <ul class="list-group mb-4">
          <li class="list-group-item" v-for="currency_pair in currency_pairs" :key="currency_pair.id">
            {{ currency_pair.pair }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import currencyPairsApi from "../../api/currencyPairsApi";

export default {
  name: "CurrencyPairsList",
  data: () => ({
    currency_pairs: [],
    modalDialogOpened: false,
    currency_pair_name: null
  }),

  methods: {
    getCurrencyPairs() {
      currencyPairsApi.getCurrencyPairs().then(response => {
        this.currency_pairs = response.data
      })
    },

    saveCurrencyPair() {
      currencyPairsApi.saveCurrentPairs(this.currency_pair_name).then(response => {
        if (response.status === 200) {
          this.currency_pairs.push({
            pair: this.currency_pair_name
          });

          this.currency_pair_name = null;
        }
      })
    }
  },
  created() {
    this.getCurrencyPairs();
  }
}
</script>