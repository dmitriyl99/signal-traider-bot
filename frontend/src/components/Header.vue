<template>
  <div class="header">
    <div class="container-fluid">

      <!-- Body -->
      <div class="header-body">
        <div class="row align-items-end">
          <div class="col">

            <!-- Pretitle -->
            <h6 class="header-pretitle">
              Signal Trader Bot
            </h6>

            <!-- Title -->
            <h1 class="header-title">
              Dashboard
            </h1>

          </div>
          <div class="col-auto">
            <!-- Button -->
            <router-link :to="{name: 'CreateSignal'}" class="btn btn-primary lift">
              Отправить сигнал
            </router-link>

          </div>
        </div> <!-- / .row -->
      </div> <!-- / .header-body -->

    </div>
  </div>
</template>

<script>
export default {
  name: "Header"
}
</script>

<style scoped>

</style>