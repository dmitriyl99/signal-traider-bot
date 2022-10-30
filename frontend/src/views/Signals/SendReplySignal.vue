<template>
<div class="card">
      <div class="card-body">
        <form v-on:submit.prevent="sendReply">
          <label for="text" class="form-label">Отправить реплай на сигнал</label>
          <input type="text" name="text" id="text" class="form-control" placeholder="Сообщение"
                 v-model="text">
          <button type="submit" class="btn btn-primary mt-2">Отправить</button>
        </form>
      </div>
    </div>
</template>

<script>
import signalsApi from "../../api/signalsApi";
export default {
  name: "SendReplySignal",
  data: () => ({
    text: null
  }),
  methods: {
    sendReply() {
      if (this.text === null || this.text.trim() === '') {
        return
      }
      signalsApi.sendReply(this.$route.params.id, this.text).then(() => {
        this.$swal({
          icon: 'success',
          text: 'Сообщение отправлено'
        })
      }).catch(() => {
        this.$swal({
          icon: 'error',
          text: 'Что-то пошло не так при отправке сообщения...'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>