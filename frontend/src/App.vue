<template>
  <AppLayout>
    <router-view></router-view>
  </AppLayout>
</template>

<script>
import AppLayout from "./layouts/AppLayout";

export default {
  name: 'App',
  components: { AppLayout }
}
</script>
