<template>
  <div>
    <div class="card">
      <div class="card-body">
        <form v-on:submit.prevent="saveUtmCommand">
          <label for="utm_command_name" class="form-label">Добавить UTM</label>
          <input type="text" name="utm_command_name" id="utm_command_name" class="form-control" placeholder="Название"
                 v-model="utmCommandName">
          <button type="submit" class="btn btn-primary mt-2">Сохранить</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <div class="card-title">UTM команды</div>
        <ul class="list-group mb-4">
          <li class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
              v-for="utm_command in utm_commands" :key="utm_command.id">
            {{ utm_command.name }}
            <div>
              <span class="badge bg-primary rounded-pill p-3 me-2" @click="generateLink(utm_command.name)"><i
                  class="fe fe-link"></i></span>
              <span class="badge bg-danger rounded-pill p-3"
                    @click="deleteUtmCommand(utm_command.id, utm_command.name)"><i class="fe fe-trash"></i></span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import utmApi from "../../api/utmApi";

export default {
  name: "UtmList",
  data: () => ({
    utm_commands: [],
    modalDialogOpened: false,
    utmCommandName: ''
  }),

  methods: {
    getUtmCommands() {
      utmApi.getUtmCommands().then(response => {
        this.utm_commands = response.data
      })
    },

    generateLink(utm_name) {
      const botUrl = `https://t.me/https://t.me/masspower_vipbot?start=utm_${utm_name}`
      navigator.clipboard.writeText(botUrl);
      this.$swal({
        icon: 'success',
        html: `<a href="${botUrl}">Ссылка на бот</a> вместе с UTM меткой была скопирована в буфер обмена`
      })
    },

    saveUtmCommand() {
      if (this.utmCommandName != null && this.utmCommandName.trim() !== '') {
        utmApi.saveUtmCommand(this.utmCommandName).then(response => {
          if (response.status === 200) {
            this.utm_commands.push({
              id: response.data.id,
              name: response.data.name
            });
            this.$swal({
              icon: 'success',
              text: 'UTM-метка добавлена'
            })
          }
        }).catch(error => {
          this.$swal({
            icon: 'error',
            text: error.response.data.detail
          })
        }).finally(() => {
          this.utmCommandName = '';
        })
      }
    },

    deleteUtmCommand(utm_id, utm_name) {
      this.$swal({
        icon: 'question',
        title: 'Подумайте',
        text: `Вы уверены, что хотите удалить метку ${utm_name}? При этом её данные сохраняться`,
        showCancelButton: true,
        confirmButtonText: 'Я подумал',
        cancelButtonText: 'Я передумал'
      }).then((result) => {
        if (result.isConfirmed) {
          utmApi.deleteUtmCommand(utm_id).then(() => {
            this.getUtmCommands();
            this.$swal({
              icon: 'success',
              text: 'UTM-метка удалена'
            })
          })
        }
      })
    }
  },

  created() {
    this.getUtmCommands();
  }
}
</script>

<style scoped>

</style>