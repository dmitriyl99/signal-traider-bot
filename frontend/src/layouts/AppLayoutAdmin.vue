<template>
<div>
  <Sidebar />
  <div class="main-content">
    <Header />
    <div class="container-fluid">
      <slot />
    </div>
  </div>
</div>
</template>

<script>
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
export default {
  name: "AppLayoutAdmin",
  components: { Sidebar, Header },
  created() {
    this.$store.dispatch('fetchUser');
  }
}
</script>