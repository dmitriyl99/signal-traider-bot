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
            <Select2 v-model="currency_pair" :options="currencyPairsList" @select="mySelectEvent($event)"/>
            <div class="invalid-feedback" style="display: block" v-if="errorText">
              {{ errorText }}
            </div>
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
            <label for="tr_1" class="form-label">TP 1</label>
            <input type="text" class="form-control" id="tr_1" placeholder="TP 1" v-model="tr_1"/>
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="tr_2" class="form-label">TP 2</label>
            <input type="text" class="form-control" id="tr_2" placeholder="TP 2" v-model="tr_2"/>
          </div>
        </div>
        <div class="row g-3">
          <div class="col-12 col-md-6 mb-3">
            <label for="price" class="form-label">Цена</label>
            <input type="text" class="form-control" id="price" placeholder="Цена" v-model="price"/>
            <span id="emailHelp" class="valid-feedback" style="display: block" v-if="recommendedPrice"
                  @click="copyRecommendedPrice">Цена с tradingview.com: {{ recommendedPrice }}</span>
          </div>
          <div class="col-12 col-md-6 mb-3">
            <label for="sl" class="form-label">SL</label>
            <input type="text" class="form-control" id="sl" placeholder="SL" v-model="sl"/>
          </div>
        </div>

        <!-- Button -->
        <button v-if="sendButtonView" :disabled="isLoading" class="btn btn-primary" type="submit"
                v-html="isLoading ? 'Отправляю, подождите...' : 'Отправить сигнал'"/>
        <span class="text-success ms-3" v-if="successText != null">{{ successText }}</span>

      </form>
      <h3 class="mt-4">Кастомное сообщение</h3>
      <form v-on:submit.prevent="onCustomMessageFormSubmit" action="" class="mt-3">
        <div class="row g-3">
          <div class="col-12 mb-3">
            <textarea id="text" rows="10" class="form-control" v-model="customMessage.text"></textarea>
          </div>
        </div>
        <DropZone @drop.prevent="drop" @change="drop"/>
        <div v-if="dropzoneFiles !== null">
          <div v-for="dropzoneFile in dropzoneFiles" :key="dropzoneFile.name">{{ dropzoneFile.name }}</div>
        </div>
        <button v-if="customMessage.sendButtonView" :disabled="customMessage.isLoading" class="btn btn-primary mt-3"
                type="submit" v-html="customMessage.isLoading ? 'Отправляю, подождите...' : 'Отправить сообщение'"/>
        <span class="text-success ms-3" v-if="customMessage.successText != null">{{ customMessage.successText }}</span>
      </form>
    </div>
  </div>
</template>

<script>
import signalsApi from "../../api/signalsApi";
import currencyPairsApi from "../../api/currencyPairsApi";
import Select2 from 'vue3-select2-component';
import DropZone from "../../components/DropZone";
import { ref } from 'vue';

export default {
  name: "CreateSignal",
  components: {Select2, DropZone},
  setup() {
    let dropzoneFiles = ref(null);

    const drop = (e) => {
      if (e.dataTransfer == null) {
        const input = document.querySelector('.dropzone input');
        dropzoneFiles.value = input.files
      } else {
        dropzoneFiles.value = e.dataTransfer.files;
      }
    };

    return { dropzoneFiles, drop }
  },
  data: () => ({
    currency_pair: null,
    execution_method: null,
    price: null,
    tr_1: null,
    tr_2: null,
    sl: null,
    isLoading: false,
    successText: null,
    sendButtonView: true,
    currencyPairsList: [],
    errorText: null,
    recommendedPrice: null,
    customMessage: {
      text: null,
      sendButtonView: true,
      isLoading: false,
      successText: null
    }
  }),

  methods: {
    onFormSubmit() {
      this.isLoading = true;
      this.successText = null;
      signalsApi.sendSignal(this.currency_pair, this.execution_method, this.price, this.tr_1, this.tr_2, this.sl).then(() => {
        this.successText = 'Сигнал успешно отправлен';
        this.sendButtonView = false;
        setTimeout(() => {
          this.$router.push({name: 'ListSignals'});
        }, 5000);
      }).finally(() => {
        this.isLoading = false;
      })
    },

    onCustomMessageFormSubmit() {
      this.customMessage.isLoading = true;
      this.customMessage.successText = null;

      console.log(this.dropzoneFiles);
      signalsApi.sendCustomMessage(this.customMessage.text, this.dropzoneFiles).then(() => {
        this.customMessage.successText = 'Сообщение отправлено!'
      }).finally(() => {
        this.customMessage.isLoading = false;
      })
    },

    loadCurrencyPairs() {
      currencyPairsApi.getCurrencyPairs().then(response => {
        this.currencyPairsList = response.data.map(function (i) {
          return i.pair;
        });
      })
    },
    mySelectEvent({id}) {
      this.errorText = null;
      this.execution_method = null;
      this.price = null;
      this.recommendedPrice = null;
      signalsApi.getSuggestion(id).then(response => {
        const suggestionData = response.data;
        this.recommendedPrice = suggestionData.price
        if (suggestionData.recommends < 0) {
          this.execution_method = 'sell';
        } else {
          this.execution_method = 'buy'
        }
      }).catch(error => {
        this.errorText = error.response.data.detail;
      })
    },

    copyRecommendedPrice() {
      this.price = this.recommendedPrice;
    }
  },
  created() {
    this.loadCurrencyPairs();
  }
}
</script>