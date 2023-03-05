<template>
  <div>
    <div class="card">
      <div class="card-body">
        <form v-on:submit.prevent="saveCurrencyPair">
          <label for="currency_pair_name" class="form-label">Добавить валютную пару</label>
          <input type="text" name="currency_pair_name" id="currency_pair_name" class="form-control" placeholder="Название"
                    v-model="currency_pair_name" v-maska data-maska="AAA / AAA" data-maska-tokens="A:[A-Z]">
          <button type="submit" class="btn btn-primary mt-2">Сохранить</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <h3 class="mt-4">Рассылка сообщений</h3>
      </div>
      <div class="card-body">
        <form v-on:submit.prevent="onCustomMessageFormSubmit" action="" class="mt-3">
          <div class="row g-3">
            <div class="col-12 mb-3">
              <label for="currency_pair" class="form-label">Валютная пара</label>
              <Select2 v-model="customMessage.currency_pair" :options="currencyPairsList"/>
            </div>
          </div>
          <div class="row g-3">
            <div class="col-12 mb-3">
              <textarea id="text" rows="10" class="form-control" v-model="customMessage.text"></textarea>
            </div>
          </div>
          <div class="row g-3 mb-3">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="1" id="flexCheckDefault"
                     v-model="customMessage.important">
              <label class="form-check-label" for="flexCheckDefault">
                ❗️Важно!
              </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="2" id="flexCheckChecked"
                     v-model="customMessage.veryImportant">
              <label class="form-check-label" for="flexCheckChecked">
                ❗️❗️❗️Очень важно!
              </label>
            </div>
          </div>
          <div class="row">
            <div class="col-6">
              <div class="d-flex flex-column justify-content-center align-items-center">
                <span class="text-center text-muted">Эти файлы будут отправлены как файлы (изображения и видео)</span>
                <DropZone @drop.prevent="dropFile" @change="dropFile" title="Drop Files" accept="*/*"/>
                <div v-if="dropzoneFiles !== null">
                  <div v-for="dropzoneFile in dropzoneFiles" :key="dropzoneFile.name">{{ dropzoneFile.name }}</div>
                </div>
              </div>
            </div>
            <div class="col-6">
              <div class="d-flex flex-column justify-content-center align-items-center">
                <span class="text-center text-muted">Эти файлы будут отправлены как изображения и видео</span>
                <DropZone @drop.prevent="dropImage" @change="dropImage" title="Drop Images" accept=".jpg"/>
                <div v-if="dropzoneImages !== null">
                  <div v-for="dropzoneImage in dropzoneImages" :key="dropzoneImage.name">{{ dropzoneImage.name }}</div>
                </div>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-end flex-column align-items-end mt-5">
            <button v-if="customMessage.sendButtonView" :disabled="customMessage.isLoading" class="btn btn-primary"
                    type="submit" v-html="customMessage.isLoading ? 'Отправляю, подождите...' : 'Отправить сообщение'"/>
            <span class="text-success ms-3" v-if="customMessage.successText != null">{{
                customMessage.successText
              }}</span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import DropZone from "../../components/DropZone";
import {ref} from 'vue';
import signalsApi from "../../api/signalsApi";
import currencyPairsApi from "../../api/currencyPairsApi";
import Select2 from 'vue3-select2-component';

export default {
  name: "CreateDistribution",
  components: {DropZone, Select2},
  setup() {
    let dropzoneFiles = ref(null);
    let dropzoneImages = ref(null);

    const dropFile = (e) => {
      if (e.dataTransfer == null) {
        const input = document.querySelector('.dropzone input');
        dropzoneFiles.value = input.files
      } else {
        dropzoneFiles.value = e.dataTransfer.files;
      }
    };

    const dropImage = (e) => {
      if (e.dataTransfer == null) {
        const input = document.querySelector('.dropzone input');
        dropzoneImages.value = input.files
      } else {
        dropzoneImages.value = e.dataTransfer.files;
      }

    }

    return {dropzoneFiles, dropzoneImages, dropFile, dropImage}
  },
  data: () => ({
    currencyPairsList: [],
    currency_pair_name: null,
    customMessage: {
      text: null,
      sendButtonView: true,
      isLoading: false,
      successText: null,
      important: false,
      veryImportant: false,
      currency_pair: null,
    }
  }),

  methods: {
    loadCurrencyPairs() {
      currencyPairsApi.getCurrencyPairs().then(response => {
        this.currencyPairsList = response.data.map(function (i) {
          return i.pair;
        });
      })
    },
    saveCurrencyPair() {
      currencyPairsApi.saveCurrentPairs(this.currency_pair_name).then(response => {
        if (response.status === 200) {
          this.loadCurrencyPairs();

          this.currency_pair_name = null;
        }
      })
    },
    onCustomMessageFormSubmit() {
      this.customMessage.isLoading = true;
      this.customMessage.successText = null;

      let importance = '0';
      if (this.customMessage.important && !this.customMessage.veryImportant) {
        importance = '1';
      } else if (this.customMessage.veryImportant) {
        importance = '2';
      }
      signalsApi.sendCustomMessage(this.customMessage.text, this.dropzoneFiles, this.dropzoneImages, importance, this.customMessage.currency_pair).then(() => {
        this.customMessage.successText = 'Сообщение отправлено!'
        this.customMessage.text = null;
        this.dropzoneFiles = null;
        this.dropzoneImages = null;
      }).finally(() => {
        this.customMessage.isLoading = false;
      }).catch(e => {
        this.$swal({
          icon: 'error',
          title: 'Ошибка',
          text: e.response.data.detail
        }).then(() => {
          this.dropzoneFiles = null;
          this.dropzoneImages = null;
        })
      })
    },
  },
  created() {
    this.loadCurrencyPairs();
  }
}
</script>

<style scoped>

</style>