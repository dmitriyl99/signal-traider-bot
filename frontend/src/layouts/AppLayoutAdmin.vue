<template>
<div>
  <Sidebar />
  <div class="main-content">
    <Header />
    <slot />
  </div>
</div>
</template>

<script>
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
export default {
  name: "AppLayoutAdmin",
  components: { Sidebar, Header }
}
</script>