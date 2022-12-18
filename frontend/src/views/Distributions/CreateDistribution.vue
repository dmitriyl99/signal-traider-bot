<template>
<div class="card">
  <div class="card-header">
    <h3 class="mt-4">Рассылка сообщений</h3>
  </div>
  <div class="card-body">
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
import DropZone from "../../components/DropZone";
import {ref} from 'vue';
import signalsApi from "../../api/signalsApi";
export default {
  name: "CreateDistribution",
  components: {DropZone},
  setup() {
    let dropzoneFiles = ref(null);

    const drop = (e) => {
      if (e.dataTransfer == null) {
        const input = document.querySelector('.dropzone input');
        console.log(input.files)
        dropzoneFiles.value = input.files
      } else {
        dropzoneFiles.value = e.dataTransfer.files;
      }
    };

    return {dropzoneFiles, drop}
  },
  data: () => ({
    customMessage: {
      text: null,
      sendButtonView: true,
      isLoading: false,
      successText: null
    }
  }),

  methods: {
    onCustomMessageFormSubmit() {
      this.customMessage.isLoading = true;
      this.customMessage.successText = null;

      console.log(this.dropzoneFiles);
      signalsApi.sendCustomMessage(this.customMessage.text, this.dropzoneFiles).then(() => {
        this.customMessage.successText = 'Сообщение отправлено!'
        this.customMessage.text = null;
        this.dropzoneFiles = null;
      }).finally(() => {
        this.customMessage.isLoading = false;
      })
    },
  }
}
</script>

<style scoped>

</style>